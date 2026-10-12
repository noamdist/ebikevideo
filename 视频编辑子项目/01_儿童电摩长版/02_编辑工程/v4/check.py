from PIL import Image, ImageDraw
from pathlib import Path
import json, subprocess,imageio_ffmpeg
p=Path('outputs/video_review/v4');f=imageio_ffmpeg.get_ffmpeg_exe()
files=sorted(p.glob('fixed_*.jpg'));sheet=Image.new('RGB',(1280,((len(files)+3)//4)*270),'#151515');d=ImageDraw.Draw(sheet)
tracks=json.loads((p/'tracking.json').read_text())
for i,path in enumerate(files):
 frame=int(path.stem.split('_')[1]);poly=tracks[frame]['poly'];x=sum(q[0] for q in poly)/4;y=sum(q[1] for q in poly)/4
 crop=Image.open(path).crop((int(x)-130,int(y)-100,int(x)+130,int(y)+100)).resize((320,246))
 xx=i%4*320;yy=i//4*270;sheet.paste(crop,(xx,yy));d.text((xx+8,yy+250),f'Source {6.5+frame/24:.2f}s',fill='white')
sheet.save(p/'repair_review.jpg')
print('Tracking coverage:',min(q['mask_pixels'] for q in tracks),max(q['mask_pixels'] for q in tracks))
