# ============================================================
# 1. SECTION: Generate and Save icon.ico
# ============================================================

# 1.1 Import Pillow
from PIL import Image, ImageDraw

# 1.2 Create the icon image
def make_ico():

    # 1.2.1 Create base image at 256x256
    img = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # 1.2.2 Draw background circle
    draw.ellipse([8, 8, 248, 248], fill=(80, 140, 255, 255))

    # 1.2.3 Draw bell body
    draw.rounded_rectangle([72, 80, 184, 176], radius=24, fill=(255, 255, 255, 255))

    # 1.2.4 Draw bell top arc
    draw.ellipse([80, 56, 176, 120], fill=(255, 255, 255, 255))

    # 1.2.5 Draw bell clapper
    draw.ellipse([108, 168, 148, 208], fill=(255, 255, 255, 255))

    # 1.2.6 Return image
    return img

# end of 1.2

# 1.3 Save as multi-resolution .ico
img = make_ico()
img.save("icon.ico", format="ICO", sizes=[(16,16),(32,32),(48,48),(64,64),(128,128),(256,256)])
print("icon.ico created.")

# end of 1.3
# end of 1. SECTION: Generate and Save icon.ico