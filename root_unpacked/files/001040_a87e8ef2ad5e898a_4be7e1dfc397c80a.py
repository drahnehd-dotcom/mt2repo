# -*- coding: utf-8 -*-
# Whisper Ignore (klient-side) — lista nazw postaci, od ktorych NIE chcemy dostawac
# whisperow. Zapis lokalny per-postac w _cfg/wignore_<owner>.cfg (jedna nazwa na linie).
# Zero udzialu serwera: filtrowanie odbywa sie w game.OnRecvWhisper.

import player

_owner = None
_ignored = set()

def _Path(owner):
	return "_cfg/wignore_%s.cfg" % owner

def _CurrentOwner():
	try:
		return player.GetName()
	except Exception:
		return ""

def EnsureLoaded():
	# Przeladuj liste jesli zmienila sie aktywna postac (np. relog na innego chara).
	global _owner, _ignored
	owner = _CurrentOwner()
	if owner == _owner:
		return
	_owner = owner
	_ignored = set()
	if not owner:
		return
	try:
		with open(_Path(owner), "r") as f:
			for line in f:
				n = line.strip()
				if n:
					_ignored.add(n)
	except IOError:
		pass

def _Save():
	if not _owner:
		return
	try:
		with open(_Path(_owner), "w") as f:
			for n in sorted(_ignored):
				f.write(n + "\n")
	except IOError:
		pass

def IsIgnored(name):
	EnsureLoaded()
	return name in _ignored

def Toggle(name):
	# Zwraca True jesli po przelaczeniu nazwa jest zablokowana, False jesli odblokowana.
	EnsureLoaded()
	if not name:
		return False
	if name in _ignored:
		_ignored.discard(name)
		_Save()
		return False
	_ignored.add(name)
	_Save()
	return True

def Block(name):
	EnsureLoaded()
	if name and name not in _ignored:
		_ignored.add(name)
		_Save()

def Unblock(name):
	EnsureLoaded()
	if name in _ignored:
		_ignored.discard(name)
		_Save()
