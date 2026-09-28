from __future__ import annotations

import argparse
import hashlib
import json
import os
import struct
import sys
from pathlib import Path

import xxhash
import zstandard as zstd

MAGIC = b"ZARC"
HEADER_SIZE = 0x68
A_SIZE = 0x30
B_SIZE = 0x20  # 32 bytes: Q Q I I Q
MASK32 = 0xFFFFFFFF
MASK64 = 0xFFFFFFFFFFFFFFFF

# Exact tables recovered from KowalMT2.exe.
T1 = [0x6081E9F9, 0x359BB7E1, 0xB9D2E7B1, 0x3BCE9A95,
      0x2B21BB27, 0x0A7F3D6F, 0xC30347DC, 0x89F2893E]
T2 = [0x8BD05A32, 0xFA65525B, 0x0FB51A0B, 0xC4B89472,
      0xF22C5C6D, 0x274527FC, 0x0A1C538E, 0x63BDA92F]
T3 = [0xDB771D82, 0xD04772D5, 0xFBBB6ED5, 0x728FFAD6,
      0x1B2B8645, 0x2AB37361, 0x08B53BAA, 0xAB0B996C]
ROT = [8, 13, 18, 23, 28, 2, 7, 12]

def rol32(x, n):
    return ((x << n) | (x >> (32 - n))) & MASK32

CHACHA_KEY = [
    (T3[i] ^ T2[i] ^ rol32(T1[i], ROT[i])) & MASK32
    for i in range(8)
]
CHACHA_CONST = [0x61707865, 0x3320646E, 0x79622D32, 0x6B206574]

def chacha_qr(a, b, c, d):
    a = (a + b) & MASK32
    d = rol32(d ^ a, 16)
    c = (c + d) & MASK32
    b = rol32(b ^ c, 12)
    a = (a + b) & MASK32
    d = rol32(d ^ a, 8)
    c = (c + d) & MASK32
    b = rol32(b ^ c, 7)
    return a, b, c, d

def chacha_block(counter, nonce3):
    state = CHACHA_CONST + CHACHA_KEY + [counter & MASK32] + nonce3
    work = state.copy()

    for _ in range(10):
        for q in ((0,4,8,12), (1,5,9,13), (2,6,10,14), (3,7,11,15)):
            work[q[0]], work[q[1]], work[q[2]], work[q[3]] = chacha_qr(
                work[q[0]], work[q[1]], work[q[2]], work[q[3]]
            )
        for q in ((0,5,10,15), (1,6,11,12), (2,7,8,13), (3,4,9,14)):
            work[q[0]], work[q[1]], work[q[2]], work[q[3]] = chacha_qr(
                work[q[0]], work[q[1]], work[q[2]], work[q[3]]
            )

    return b"".join(
        struct.pack("<I", (work[i] + state[i]) & MASK32)
        for i in range(16)
    )

def payload_nonce(file_offset, archive_seed):
    # Exact variant confirmed against the original root:
    # XXH3-128(le64(offset), seed=archive_seed)
    # nonce = low64 little-endian + first 4 bytes of high64 little-endian.
    h = xxhash.xxh3_128_intdigest(
        struct.pack("<Q", file_offset),
        seed=archive_seed & MASK64,
    )
    low = h & MASK64
    high = (h >> 64) & MASK64
    return [
        low & MASK32,
        (low >> 32) & MASK32,
        high & MASK32,
    ]

def payload_crypt(data, file_offset, archive_seed):
    nonce3 = payload_nonce(file_offset, archive_seed)
    out = bytearray(len(data))

    for block_index in range((len(data) + 63) // 64):
        ks = chacha_block(block_index, nonce3)
        start = block_index * 64
        end = min(start + 64, len(data))
        for i in range(start, end):
            out[i] = data[i] ^ ks[i - start]

    return bytes(out)

def metadata_crypt(data, key):
    if len(data) % 8:
        raise ValueError("Metadata must be divisible by 8.")
    out = bytearray(len(data))
    for off in range(0, len(data), 8):
        block_index = off // 8
        mixed = (block_index ^ key) & MASK64
        mask = xxhash.xxh3_64_intdigest(
            struct.pack("<Q", mixed),
            seed=key & MASK64,
        )
        struct.pack_into(
            "<Q", out, off,
            struct.unpack_from("<Q", data, off)[0] ^ mask
        )
    return bytes(out)

def parse_header(raw):
    if len(raw) < HEADER_SIZE or raw[:4] != MAGIC:
        raise ValueError("Not a ZARC archive.")
    return {
        "version": struct.unpack_from("<I", raw, 4)[0],
        "meta_key": struct.unpack_from("<Q", raw, 0x10)[0],
        "meta_size": struct.unpack_from("<Q", raw, 0x20)[0],
        "data_start": struct.unpack_from("<Q", raw, 0x28)[0],
        "count_a": struct.unpack_from("<Q", raw, 0x30)[0],
        "count_b": struct.unpack_from("<Q", raw, 0x38)[0],
        "meta_hash": struct.unpack_from("<Q", raw, 0x40)[0],
        "seed": struct.unpack_from("<Q", raw, 0x48)[0],
    }

def read_zarc(path):
    raw = path.read_bytes()
    header_raw = raw[:HEADER_SIZE]
    h = parse_header(header_raw)

    meta_cipher = raw[HEADER_SIZE:HEADER_SIZE + h["meta_size"]]
    if len(meta_cipher) != h["meta_size"]:
        raise ValueError("Truncated metadata.")

    meta = metadata_crypt(meta_cipher, h["meta_key"])
    meta_hash = xxhash.xxh3_64_intdigest(meta)
    if meta_hash != h["meta_hash"]:
        raise ValueError(
            f"Metadata hash mismatch: {meta_hash:016x} != {h['meta_hash']:016x}"
        )

    expected = h["count_a"] * A_SIZE + h["count_b"] * B_SIZE
    if len(meta) != expected:
        raise ValueError(
            f"Metadata size mismatch: {len(meta)} != {expected}. "
            f"This is the key v4 check."
        )

    A = []
    pos = 0
    for i in range(h["count_a"]):
        h0, h1, size, first_chunk, packed_info, reserved = struct.unpack_from(
            "<QQQQQQ", meta, pos
        )
        A.append({
            "index": i,
            "hash0": h0,
            "hash1": h1,
            "size": size,
            "first_chunk": first_chunk,
            "packed_info": packed_info,
            "chunk_count": packed_info & MASK32,
            "file_flags": (packed_info >> 32) & MASK32,
            "reserved": reserved,
        })
        pos += A_SIZE

    B = []
    for i in range(h["count_b"]):
        # IMPORTANT: original B record is exactly 32 bytes.
        off, packed_info, flags, reserved, cipher_hash = struct.unpack_from(
            "<QQIIQ", meta, pos
        )
        B.append({
            "index": i,
            "offset": off,
            "packed_size": packed_info & MASK32,
            "unpacked_size": (packed_info >> 32) & MASK32,
            "flags": flags,
            "reserved": reserved,
            "cipher_hash": cipher_hash,
        })
        pos += B_SIZE

    return raw, header_raw, h, meta, A, B

def zstd_decompress_frame(cipher_after_crypto, expected_size):
    dctx = zstd.ZstdDecompressor()
    # stream_reader supports frames without content-size in the header.
    import io
    with dctx.stream_reader(io.BytesIO(cipher_after_crypto)) as reader:
        data = reader.read()
    if len(data) != expected_size:
        raise ValueError(
            f"ZSTD size mismatch: got {len(data)}, expected {expected_size}"
        )
    return data

def decode_logical_file(raw, h, b_list, a):
    result = bytearray()
    chunks = []
    for bindex in range(a["first_chunk"], a["first_chunk"] + a["chunk_count"]):
        b = b_list[bindex]
        ciphertext = raw[
            b["offset"]: b["offset"] + b["packed_size"]
        ]
        if len(ciphertext) != b["packed_size"]:
            raise ValueError(f"Short chunk {bindex}")

        expected_hash = xxhash.xxh3_64_intdigest(ciphertext)
        if expected_hash != b["cipher_hash"]:
            raise ValueError(
                f"Cipher hash mismatch for chunk {bindex}: "
                f"{expected_hash:016x} != {b['cipher_hash']:016x}"
            )

        plain_or_zstd = (
            payload_crypt(ciphertext, b["offset"], h["seed"])
            if (b["flags"] & 0x02)
            else ciphertext
        )

        if b["flags"] & 0x01:
            try:
                plain = zstd_decompress_frame(
                    plain_or_zstd, b["unpacked_size"]
                )
            except Exception as exc:
                raise ValueError(
                    f"ZSTD failure at A[{a['index']}] B[{bindex}] "
                    f"offset={b['offset']} packed={b['packed_size']} "
                    f"unpacked={b['unpacked_size']} flags=0x{b['flags']:08x}: {exc}"
                ) from exc
        else:
            plain = plain_or_zstd

        if len(plain) != b["unpacked_size"]:
            raise ValueError(
                f"Chunk {bindex} logical size mismatch."
            )

        result.extend(plain)
        chunks.append({**b})

    if len(result) != a["size"]:
        raise ValueError(
            f"A[{a['index']}] logical size mismatch: "
            f"{len(result)} != {a['size']}"
        )

    return bytes(result), chunks

def detect_extension(data):
    if data.startswith(b"\x89PNG\r\n\x1a\n"): return ".png"
    if data.startswith(b"\xff\xd8\xff"): return ".jpg"
    if data.startswith(b"DDS "): return ".dds"
    if len(data) >= 18 and data[1] in (0,1) and data[2] in (2,10) and data[16] in (8,15,16,24,32):
        return ".tga"
    if data.startswith(b"PK\x03\x04"): return ".zip"
    if data.startswith(b"ZARC"): return ".zarc"
    stripped = data.lstrip()
    if stripped.startswith((b"{", b"[")):
        try:
            json.loads(data.decode("utf-8"))
            return ".json"
        except Exception:
            pass
    try:
        text = data.decode("utf-8")
        sample = text[:65536]
        printable = sum(c.isprintable() or c in "\r\n\t" for c in sample)
        if sample and printable / len(sample) > 0.92:
            low = sample.lower()
            if "import " in low or "from " in low or "def " in low or "class " in low:
                return ".py"
            return ".txt"
    except UnicodeDecodeError:
        pass
    return ".bin"

def manifest_for_archive(path, output_dir):
    raw, header_raw, h, meta, A, B = read_zarc(path)

    files = []
    for a in A:
        logical, chunks = decode_logical_file(raw, h, B, a)
        base = f'{a["index"]:06d}_{a["hash0"]:016x}_{a["hash1"]:016x}'
        name = base + detect_extension(logical)
        rel = Path("files") / name
        (output_dir / rel).write_bytes(logical)
        files.append({
            **a,
            "output_path": rel.as_posix(),
            "sha256": hashlib.sha256(logical).hexdigest(),
            "chunks": chunks,
        })

    manifest = {
        "format": "KowalMT2-ZARC-v4",
        "source_path": str(path.resolve()),
        "source_name": path.name,
        "header_file": "header.bin",
        "header": h,
        "files": files,
    }
    (output_dir / "header.bin").write_bytes(header_raw)
    (output_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return manifest

def unpack(path, out_dir):
    out_dir.mkdir(parents=True, exist_ok=True)
    files_dir = out_dir / "files"
    files_dir.mkdir(exist_ok=True)
    manifest = manifest_for_archive(path, out_dir)
    print(f"OK unpack: {path}")
    print(f"  files: {len(manifest['files'])}")
    print(f"  A: {manifest['header']['count_a']}")
    print(f"  B: {manifest['header']['count_b']}")
    print(f"  -> {out_dir}")

def find_original(root):
    source = root.parent / root.name.removesuffix("_unpacked")
    if source.is_file():
        return source
    manifest = root / "manifest.json"
    if manifest.is_file():
        m = json.loads(manifest.read_text(encoding="utf-8"))
        p = Path(m.get("source_path", ""))
        if p.is_file():
            return p
    return None

def split_for_chunks(data, original_chunks):
    if not original_chunks:
        return [data]

    sizes = [int(c["unpacked_size"]) for c in original_chunks]
    if len(sizes) == 1:
        return [data]

    fixed = sum(sizes[:-1])
    if len(data) < fixed:
        raise ValueError(
            f"Edited file is too small for its original {len(sizes)}-chunk layout."
        )

    pieces = []
    pos = 0
    for size in sizes[:-1]:
        pieces.append(data[pos:pos+size])
        pos += size
    pieces.append(data[pos:])
    return pieces

def build_changed(root, original_path, output_path):
    raw0, header_raw, h0, meta0, A0, B0 = read_zarc(original_path)

    mpath = root / "manifest.json"
    if not mpath.is_file():
        raise ValueError("manifest.json missing")
    manifest = json.loads(mpath.read_text(encoding="utf-8"))

    if len(manifest["files"]) != len(A0):
        raise ValueError(
            f"Manifest file count {len(manifest['files'])} != original A count {len(A0)}"
        )

    # Load all current logical files.
    current = []
    changed_any = False
    for rec in sorted(manifest["files"], key=lambda x: x["index"]):
        path = root / rec["output_path"]
        if not path.is_file():
            raise ValueError(f"Missing extracted file: {path}")
        data = path.read_bytes()
        old_sha = rec["sha256"]
        changed = hashlib.sha256(data).hexdigest() != old_sha
        changed_any |= changed
        current.append((rec, data, changed))

    if not changed_any:
        output_path.write_bytes(original_path.read_bytes())
        print("OK: no logical files changed, exact byte-for-byte copy created.")
        print(f" -> {output_path}")
        return

    # Keep exact original chunk graph: same A.first_chunk, same chunk counts,
    # same B count, same per-chunk flags/reserved fields.
    encoded_chunks = [None] * len(B0)
    new_A = []

    data_start = HEADER_SIZE + len(A0) * A_SIZE + len(B0) * B_SIZE
    cursor = data_start

    for rec, logical, changed in current:
        a = A0[rec["index"]]
        orig_chunk_count = a["chunk_count"]
        orig_chunks = B0[a["first_chunk"]:a["first_chunk"] + orig_chunk_count]

        pieces = split_for_chunks(logical, orig_chunks)
        if len(pieces) != orig_chunk_count:
            raise ValueError(
                f"A[{a['index']}] chunk count changed from "
                f"{orig_chunk_count} to {len(pieces)}."
            )

        new_A.append({
            **a,
            "size": len(logical),
        })

        for j, (piece, orig_b) in enumerate(zip(pieces, orig_chunks)):
            stored = piece
            if orig_b["flags"] & 0x01:
                stored = zstd.ZstdCompressor(
                    level=15,
                    write_checksum=False,
                ).compress(stored)

            if orig_b["flags"] & 0x02:
                stored = payload_crypt(
                    stored,
                    cursor,
                    h0["seed"],
                )

            cipher_hash = xxhash.xxh3_64_intdigest(stored)

            encoded_chunks[orig_b["index"]] = {
                **orig_b,
                "offset": cursor,
                "packed_size": len(stored),
                "unpacked_size": len(piece),
                "cipher_hash": cipher_hash,
                "_stored": stored,
            }
            cursor += len(stored)

    # All B records must have been filled.
    if any(x is None for x in encoded_chunks):
        raise ValueError("Internal chunk mapping error.")

    meta = bytearray()
    for a in new_A:
        packed_info = (
            ((a["file_flags"] & MASK32) << 32)
            | (a["chunk_count"] & MASK32)
        )
        meta += struct.pack(
            "<QQQQQQ",
            a["hash0"],
            a["hash1"],
            a["size"],
            a["first_chunk"],
            packed_info,
            a["reserved"],
        )

    for b in encoded_chunks:
        packed_info = (
            ((b["unpacked_size"] & MASK32) << 32)
            | (b["packed_size"] & MASK32)
        )
        meta += struct.pack(
            "<QQIIQ",
            b["offset"],
            packed_info,
            b["flags"] & MASK32,
            b["reserved"] & MASK32,
            b["cipher_hash"] & MASK64,
        )

    meta_hash = xxhash.xxh3_64_intdigest(bytes(meta))
    meta_cipher = metadata_crypt(bytes(meta), h0["meta_key"])

    header = bytearray(header_raw)
    struct.pack_into("<Q", header, 0x20, len(meta_cipher))
    struct.pack_into("<Q", header, 0x28, data_start)
    struct.pack_into("<Q", header, 0x30, len(new_A))
    struct.pack_into("<Q", header, 0x38, len(encoded_chunks))
    struct.pack_into("<Q", header, 0x40, meta_hash)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("wb") as f:
        f.write(header)
        f.write(meta_cipher)
        for b in encoded_chunks:
            f.write(b["_stored"])

    print("OK: modified ZARC packed.")
    print(f"  A={len(new_A)} B={len(encoded_chunks)}")
    print(f"  metadata={len(meta)} bytes")
    print(f"  data_start=0x{data_start:x}")
    print(f"  output={output_path}")

def pack(root, output):
    original = find_original(root)
    if not original:
        raise ValueError(
            "Nie znaleziono oryginalnego archiwum obok katalogu *_unpacked. "
            "Umieść np. root oraz root_unpacked obok siebie."
        )
    build_changed(root, original, output)

def verify(path):
    raw, _, h, _, A, B = read_zarc(path)
    for i, b in enumerate(B):
        c = raw[b["offset"]:b["offset"] + b["packed_size"]]
        if xxhash.xxh3_64_intdigest(c) != b["cipher_hash"]:
            raise ValueError(f"B hash mismatch: {i}")
        if b["offset"] < h["data_start"] or b["offset"] + b["packed_size"] > len(raw):
            raise ValueError(f"B range mismatch: {i}")
    for a in A:
        if a["first_chunk"] + a["chunk_count"] > len(B):
            raise ValueError(f"A chunk range mismatch: {a['index']}")
    print("VERIFY OK")
    print(f"A={len(A)} B={len(B)} size={len(raw)} metadata={h['meta_size']}")

def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("unpack")
    p.add_argument("input")
    p.add_argument("-o", "--out")

    p = sub.add_parser("pack")
    p.add_argument("input")
    p.add_argument("-o", "--out")

    p = sub.add_parser("verify")
    p.add_argument("input")

    args = ap.parse_args()

    if args.cmd == "unpack":
        src = Path(args.input)
        out = Path(args.out) if args.out else src.with_name(src.name + "_unpacked")
        unpack(src, out)
    elif args.cmd == "pack":
        root = Path(args.input)
        out = Path(args.out) if args.out else root.with_name(
            root.name.removesuffix("_unpacked") + ".new"
        )
        pack(root, out)
    elif args.cmd == "verify":
        verify(Path(args.input))

if __name__ == "__main__":
    main()
