#martysama0134's script - quick emoji rename from https://emojipedia.org/apple/ ctrl+s 72x72 shit
import os
workpath = "."
emojilist = os.listdir(workpath)

for fn in emojilist:
    if not fn.endswith(".png"):
        continue
    old_fn = new_fn = fn
    # sanatize shit in the end
    if fn.count("_") >= 1:
        if "_emoji-modifier-fitzpatrick-type-" in fn:
            new_fn = new_fn.replace("_emoji-modifier-fitzpatrick-type-", "-tone").replace("tone1-2", "tone2")
        new_fn = new_fn[:new_fn.find("_")]+".png"
    if old_fn == new_fn:
        print("skipping %s" % (fn))
    else:
        print("renaming %s to %s" % (old_fn, new_fn))
        os.rename(old_fn, new_fn)
    # move tone/type
    mv_paths = ("tone", "type")
    for mv_path in mv_paths:
        if mv_path in new_fn:
            if not os.path.exists(mv_path): #and not os.path.isdir(mv_path):
                os.makedirs(mv_path)
            os.rename(new_fn, mv_path+"/"+new_fn)
#