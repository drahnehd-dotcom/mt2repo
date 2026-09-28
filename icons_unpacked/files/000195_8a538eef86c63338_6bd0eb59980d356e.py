#martysama0134's script - generate emoji_table.txt
import os

rootDir = 'chat'
with open("emoji_table.txt", "w") as f:
    for dirName, subdirList, fileList in os.walk(rootDir, topdown=False):
        for fname in fileList:
            if not fname.endswith(".png"):
                continue
            emojiname = ":%s:" % fname[:-4]
            emojifile = "/".join(os.path.join(dirName, fname).split("\\"))#[1:])
            f.write("%s\t%s\n"%(emojiname, emojifile))

#