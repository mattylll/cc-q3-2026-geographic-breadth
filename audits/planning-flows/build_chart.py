from pathlib import Path
import csv
from PIL import Image, ImageDraw, ImageFont

BASE = Path(__file__).parent
rows = [r for r in csv.DictReader((BASE / 'derived/flow_comparison.csv').open()) if r['geography'] == 'Panel']
im = Image.new('RGB', (1500, 1120), '#f7f5ef'); d = ImageDraw.Draw(im)
regular = '/System/Library/Fonts/Supplemental/Arial.ttf'
bold = '/System/Library/Fonts/Supplemental/Arial Bold.ttf'
ink, blue, orange = '#18313b', '#187879', '#b26832'
def text(x, y, s, size=30, color=ink, heavy=False):
    d.text((x, y), s, font=ImageFont.truetype(bold if heavy else regular, size), fill=color)

d.rectangle((0, 0, 1500, 14), fill=blue)
text(70, 52, 'CONSTRUCTION CAPITAL  /  Q3 PLANNING EVIDENCE', 25, blue, True)
text(70, 110, 'More decisions per receipt.', 58, heavy=True)
text(70, 184, 'Fewer decisions in total.', 58, heavy=True)
text(70, 274, 'Matched 253-authority panel. Separate flows, not the same cases.', 30)
d.rectangle((70, 345, 96, 371), fill=blue); text(111, 338, 'Applications received', 28)
d.rectangle((505, 345, 531, 371), fill=orange); text(546, 338, 'Known decisions', 28)
text(1150, 332, 'Decisions per', 26, heavy=True); text(1150, 365, '100 receipts', 26, heavy=True)
scale = 730 / 12000
for y, r in zip([420, 590, 760], rows):
    label = r['quarter'].replace('-', ' ')
    text(70, y+27, label, 31, heavy=True)
    for off, key, col in [(0, 'received', blue), (54, 'known_decisions', orange)]:
        n = int(r[key]); x0 = 290; x1 = x0 + n * scale
        d.rectangle((x0, y+off, x1, y+off+35), fill=col)
        text(x1+13, y+off-1, f'{n:,}', 29, col, True)
    text(1170, y+16, f"{float(r['known_decisions_per_100_receipts']):.1f}", 48, heavy=True)
d.line((70, 931, 1420, 931), fill='#c8ceca', width=2)
text(70, 962, 'Q3 2025 to Q3 2026: receipts -26.2%; known decisions -9.4%.', 30, heavy=True)
text(70, 1013, 'Known decisions = approvals + refusals. No backlog or speed estimate.', 27)
text(70, 1060, 'Source: CC-DF-2026Q3-01, fixed 5 October 2026 edition. Three selected quarters.', 23)
im.save(BASE / 'planning-flows.png')
