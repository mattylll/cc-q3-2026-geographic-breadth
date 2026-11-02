"""Render the chart from reproduced values. Requires Pillow; no external assets."""
from pathlib import Path
import csv
from PIL import Image, ImageDraw, ImageFont

BASE = Path(__file__).resolve().parent
rows = [r for r in csv.DictReader((BASE / 'derived/rate_volume_comparison.csv').open()) if r['geography'] != 'Panel']
W, H = 1800, 1300
im = Image.new('RGB', (W, H), '#f6f5ef')
d = ImageDraw.Draw(im)
INK, TEAL, ORANGE, GRID = '#18333d', '#087b78', '#b35d2d', '#d5dcd7'
def text(x, y, s, size=28, color=INK, bold=False):
    font = '/System/Library/Fonts/Supplemental/Arial Bold.ttf' if bold else '/System/Library/Fonts/Supplemental/Arial.ttf'
    d.text((x,y),s,font=ImageFont.truetype(font,size),fill=color)
d.rectangle((0,0,W,14), fill=TEAL)
text(70,55,'CONSTRUCTION CAPITAL / DEVELOPMENT FINANCE RESEARCH',26,TEAL,True)
text(70,115,'A higher approval rate can hide fewer approvals',54,bold=True)
text(70,195,'Q3 2025 versus provisional Q3 2026. Same 253-authority panel.',30)
text(70,245,'South West: 75.8% to 79.1% approved, while approvals fell 12.9%.',32,bold=True)
text(510,335,'APPROVAL RATE CHANGE',27,TEAL,True)
text(510,375,'Percentage points',24)
text(1140,335,'APPROVED APPLICATIONS',27,ORANGE,True)
text(1140,375,'Percentage change',24)
# Different units are kept in separate, labelled panels.
x1, scale1, x2, scale2 = 925, 23, 1575, 10
for y,r in zip(range(470,1100,90),rows):
    if r['geography']=='South West':d.rounded_rectangle((50,y-16,1745,y+63),radius=8,fill='#e0eee8')
    name = r['geography']
    text(70,y+1,name,28,bold=name=='South West')
    rate=float(r['approval_rate_change_pp']);count=float(r['approved_change_pct'])
    d.line((x1-370,y+21,x1+90,y+21),fill=GRID,width=2)
    d.line((x1,y-7,x1,y+49),fill=INK,width=2)
    end=x1+rate*scale1
    d.line((min(x1,end),y+21,max(x1,end),y+21),fill=TEAL,width=13)
    d.ellipse((end-8,y+13,end+8,y+29),fill=TEAL)
    text(1012,y+1,f'{rate:+.2f}',25,TEAL,True)
    d.line((x2-360,y+21,x2,y+21),fill=GRID,width=2)
    end2=x2+count*scale2
    d.line((end2,y+21,x2,y+21),fill=ORANGE,width=13)
    d.line((x2,y-7,x2,y+49),fill=INK,width=2)
    text(1600,y+1,f'{count:.1f}%',25,ORANGE,True)
d.line((70,1140,1730,1140),fill=GRID,width=2)
text(70,1170,'Approval rate = approvals / (approvals + refusals). Withdrawn and unknown excluded.',25)
text(70,1210,'Application counts are not unique developments, homes, construction starts or funded schemes.',25)
text(70,1250,'Source: CC-DF-2026Q3-01, frozen 5 October 2026 edition. Seven custom regional groups.',23)
im.save(BASE / 'derived/rate-volume.png')
