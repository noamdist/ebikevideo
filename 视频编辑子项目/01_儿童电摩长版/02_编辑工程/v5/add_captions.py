from pathlib import Path
import subprocess, imageio_ffmpeg, json
p=Path('outputs/video_review/v5')
base=Path('/Users/jayden/Downloads/Little_Rider_Big_Adventures_Jayden_Edit_v5_EN')
captions=[
(0.20,2.87,'LITTLE RIDER. BIG ADVENTURES.','Title'),
(3.30,11.85,"A SURPRISE THEY’LL REMEMBER.",'Caption'),
(12.10,16.75,'SMALL BIKE. BIG PERSONALITY.','Caption'),
(17.20,22.00,'GEAR UP. LET’S GO.','Caption'),
(22.25,31.20,'ONE RIDE. ONE BIG SMILE.','Caption'),
(31.45,40.40,'MAKE WEEKENDS AN ADVENTURE.','Caption'),
(40.90,45.30,'THEIR ADVENTURE. YOUR SHARED MEMORIES.','Caption'),
(45.95,48.70,'BIG DREAMS START HERE.\nEXPLORE THE BIKE.','End')]
def timestamp(t,srt=False):
 units=1000 if srt else 100;n=round(t*units);h,n=divmod(n,3600*units);m,n=divmod(n,60*units);sec,frac=divmod(n,units)
 return f'{h:02d}:{m:02d}:{sec:02d},{frac:03d}' if srt else f'{h}:{m:02d}:{sec:02d}.{frac:02d}'
header='''[Script Info]
Title: Little Rider. Big Adventures.
ScriptType: v4.00+
PlayResX: 1280
PlayResY: 720
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Caption,Arial,32,&H00FFFFFF,&H00FFFFFF,&H80101010,&H80000000,-1,0,0,0,100,100,0.4,0,1,1.7,1.2,2,64,64,48,1
Style: Title,Arial,39,&H00FFFFFF,&H00FFFFFF,&H80101010,&H80000000,-1,0,0,0,100,100,0.7,0,1,1.7,1.2,2,64,64,48,1
Style: End,Arial,34,&H00FFFFFF,&H00FFFFFF,&H80101010,&H80000000,-1,0,0,0,100,100,0.6,0,1,1.7,1.2,2,64,64,48,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''
events=[];srts=[]
for i,(a,b,text,style) in enumerate(captions,1):
 at=text.replace('\n',r'\N')
 events.append(f'Dialogue: 0,{timestamp(a)},{timestamp(b)},{style},,0,0,0,,{{\\fad(120,160)}}{at}')
 srts.append(f'{i}\n{timestamp(a,True)} --> {timestamp(b,True)}\n{text}\n')
ass=base.with_suffix('.ass');srt=base.with_suffix('.srt');ass.write_text(header+'\n'.join(events)+'\n');srt.write_text('\n'.join(srts))
(p/'captions.json').write_text(json.dumps(captions,indent=2,ensure_ascii=False))
f=imageio_ffmpeg.get_ffmpeg_exe();out=base.with_suffix('.mp4')
cmd=[f,'-v','warning','-y','-i','/Users/jayden/Downloads/Little_Rider_Big_Adventures_Jayden_Edit_v4.mp4','-vf',f"ass=filename='{ass}':fontsdir='/System/Library/Fonts/Supplemental'",'-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart','-map_metadata','-1',str(out)]
with (p/'render.log').open('w') as log:subprocess.run(cmd,stdout=log,stderr=log,check=True)
print(out)
