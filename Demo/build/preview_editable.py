"""Create contact sheets from actual PowerPoint screenshots (not final artwork)."""
from pathlib import Path
import json
from PIL import Image, ImageDraw

root = Path(__file__).resolve().parent / 'editable'
slides = json.loads((root/'elements.json').read_text(encoding='utf-8'))['slides']
last = {}
for number, record in enumerate(slides, 1):
    last[record['frame']] = number
items = list(last.items())
for start in range(0, len(items), 4):
    canvas = Image.new('RGB', (1280, 1010), '#dddddd')
    draw = ImageDraw.Draw(canvas)
    for index, (frame, number) in enumerate(items[start:start+4]):
        x, y = (index % 2)*640, (index // 2)*505
        screenshot = Image.open(root/'preview'/f'Slide{number}.PNG').convert('RGB')
        screenshot.thumbnail((640, 480))
        canvas.paste(screenshot, (x,y+25))
        draw.text((x+8,y+5), f'Frame {frame}; final reveal (slide {number})', fill='black')
    canvas.save(root/f'contact-{start//4+1}.png')
print(last)
