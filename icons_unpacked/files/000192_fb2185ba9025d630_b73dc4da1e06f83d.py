#martysama0134's script - quick emoji converter 72x72 to 18x18 with backup
## REQUIRED: pip install Pillow
from PIL import Image
import os
workpath = "."
outpath = "conv/"
emojilist = os.listdir(workpath)

# make output folder
if not os.path.exists(outpath):
    os.makedirs(outpath)

for fn in emojilist:
    # skip not images
    if not fn.endswith(".png"):
        continue
    image = Image.open(fn)
    # convert 72x72
    if image.size == (72, 72):
        print("processing %s" % fn)
        new_image = image.resize((18,18))
        new_image.save(os.path.join(outpath, fn))
    else:
        print("skipping %s" % fn)
#