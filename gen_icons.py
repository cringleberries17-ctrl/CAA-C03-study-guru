from PIL import Image, ImageDraw, ImageFont

NAVY = (35, 47, 62, 255)
ACCENT = (228, 131, 18, 255)
WHITE = (255, 255, 255, 255)
FONT_PATH = r"C:\Windows\Fonts\segoeuib.ttf"

def rounded_bg(size, radius_ratio=0.22, color=NAVY):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, size - 1, size - 1], radius=int(size * radius_ratio), fill=color)
    return img, d

def draw_mark(size, pad_ratio=0.0):
    img, d = rounded_bg(size)
    # underline accent bar near bottom
    bar_h = max(2, int(size * 0.07))
    margin = int(size * 0.16)
    d.rounded_rectangle(
        [margin, size - margin - bar_h, size - margin, size - margin],
        radius=bar_h // 2, fill=ACCENT
    )
    # "SAA" monogram
    font_size = int(size * 0.40)
    font = ImageFont.truetype(FONT_PATH, font_size)
    text = "SAA"
    bbox = d.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    tx = (size - tw) / 2 - bbox[0]
    ty = (size - th) / 2 - bbox[1] - size * 0.06
    d.text((tx, ty), text, font=font, fill=WHITE)
    return img

def draw_maskable(size):
    # maskable icons need extra safe-zone padding (~20%) since OS may crop to a circle
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, size, size], fill=NAVY)
    inner = draw_mark(int(size * 0.7))
    img.paste(inner, (int(size * 0.15), int(size * 0.15)), inner)
    return img

sizes = [16, 32, 180, 192, 512]
for s in sizes:
    draw_mark(s).save(f"icon-{s}.png")

draw_maskable(512).save("icon-512-maskable.png")

print("done")
