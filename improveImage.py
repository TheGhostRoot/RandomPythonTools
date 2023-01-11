from PIL import Image, ImageFilter

img = input("Image path: ")
betterImg = input("Where the image should be saved: ")

with Image.open(img) as im:

    im = im.filter(ImageFilter.UnsharpMask)

    im = im.convert("RGB")

    im.save(betterImg, quality=100)