# require:
# pip install pillow numpy
import argparse
from PIL import Image, ImageDraw, ImageFont

def generate_bitmap(text, fn="STHeiti Medium", fs=64, x=2, y=2,width=64, height=64, preview=False):
    image = Image.new("1", (width, height), 0)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(fn, fs)
    draw.text((10, 5), text, font=font, fill=1)
    if preview:
        image.show()
    bytes_per_row = (width + 7) // 8
    bitmap = []
    for y in range(height):
        for x in range(0, width, 8):
            byte = 0
            for bit in range(8):
                if x + bit < width and image.getpixel((x + bit, y)):
                    byte |= (1 << (7 - bit))
            bitmap.append(byte)
    return bitmap

parser = argparse.ArgumentParser(
    prog="chargen", 
    description="Generate charactors bitmap for MCU",
    epilog="Thank for using WindTools-%(prog)s!"
)
parser.add_argument(dest="chars", metavar="charaters")
parser.add_argument("-f", dest="font", help="font type", default="STHeiti Medium")   # macOS font
parser.add_argument("-fs", dest="fontsize", help="font size", type=int, default=60)
parser.add_argument("-bs", dest="bitmapsize", help="bitmap size", type=int, default=64)
parser.add_argument("-ox", dest="offsetx", help="start point in x", type=int, default=5)
parser.add_argument("-oy", dest="offsety", help="start point in y", type=int, default=2)
parser.add_argument("-p", dest="preview", help="show the output bitmap in preview", action="store_true")
args = parser.parse_args()

for ch in args.chars:
    bitmap = generate_bitmap(ch, args.font, args.fontsize, args.offsetx, args.offsety, args.bitmapsize, args.bitmapsize, args.preview)
    print(f"const uint8_t char_{args.bitmapsize}x{args.bitmapsize}_{ch}[{(args.bitmapsize*((args.bitmapsize+7)//8))}] = {{")
    for i in range(0, args.bitmapsize*((args.bitmapsize+7)//8), (args.bitmapsize+7)//8):
        print("    " + ", ".join(f"0x{b:02X}" for b in bitmap[i:i+(args.bitmapsize+7)//8]) + ",")
    print("};")

