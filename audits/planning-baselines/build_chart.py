"""Render the approved-application chart. Requires Pillow and Arial fonts on macOS."""
from pathlib import Path
import csv
from PIL import Image,ImageDraw,ImageFont
BACK=Path(__file__).resolve().parent
rows=list(csv.DictReader((BACK/"derived/regional_approval_baselines.csv").open()))
regions=rows[1:]
# A single shared scale keeps the two comparison periods directly comparable.
W,H=1800,1230
im=Image.new('RGB',(W,H),'#f8f7f2');d=ImageDraw.Draw(im)
INK,TEAL,ORANGE,GRID='#19333c','#087c77','#b35b2b','#d7dfdb'
def text(x,y,s,size=28,color=INK,bold=False):
    font='/System/Library/Fonts/Supplemental/Arial Bold.ttf' if bold else '/System/Library/Fonts/Supplemental/Arial.ttf'
    d.text((x,y),s,font=ImageFont.truetype(font,size),fill=color)
text(70,45,'CONSTRUCTION CAPITAL / DEVELOPMENT FINANCE',27,TEAL,True)
text(70,105,'Three quarterly increases, seven annual falls',53,bold=True)
text(70,184,'Approved applications indexed to Q3 2025 = 100',32)
text(70,230,'253-authority panel. Seven custom groups. Frozen 5 October 2026 edition.',27)
d.ellipse((500,305,520,325),fill='#84919a');text(536,294,'Q2 2026',27)
d.ellipse((760,305,780,325),fill=TEAL);text(797,294,'Q3 2026',27)
left,right=600,1530
def xpos(v):return left+(float(v)-60)/45*(right-left)
for tick in [60,70,80,90,100]:
    x=xpos(tick);d.line((x,370,x,1040),fill=GRID,width=2)
    text(x-20,1054,str(tick),25)
text(xpos(100)-78,345,'Q3 2025',23,bold=True)
text(1560,345,'Q3 vs Q2',25,bold=True)
for i,r in enumerate(regions):
    y=420+i*91
    name=r['geography'];delta=float(r['quarterly_change_pct'])
    text(70,y-14,name,28,bold=delta>0)
    a,b=xpos(r['index_2026_q2']),xpos(r['index_2026_q3'])
    d.line((min(a,b),y,max(a,b),y),fill=TEAL if delta>0 else ORANGE,width=6)
    d.ellipse((a-9,y-9,a+9,y+9),fill='#84919a')
    d.ellipse((b-11,y-11,b+11,y+11),fill=TEAL)
    text(1560,y-15,f'{delta:+.1f}%',28,TEAL if delta>0 else ORANGE,True)
text(70,1120,'Quarterly counts are not seasonally adjusted. These are applications, not homes or funded schemes.',26)
text(70,1166,'Source: CC-DF-2026Q3-01. Author: Matt Lenzie / Construction Capital.',25)
im.save(BACK/'derived/approval-baselines.png')

