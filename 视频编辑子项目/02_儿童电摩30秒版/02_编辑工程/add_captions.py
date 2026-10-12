from pathlib import Path
import subprocess, imageio_ffmpeg, json
p=Path('outputs/video_review/30s')
base=Path('/Users/jayden/Downloads/30秒儿童电摩版本_英文字幕版')
captions=[
(0.12,2.20,'LITTLE RIDER. BIG ADVENTURES.','Title'),
(2.35,4.75,'SMALL BIKE. BIG PERSONALITY.','Caption'),
(5.30,10.15,"A SURPRISE THEY’LL REMEMBER.",'Caption'),
(10.40,15.00,'GEAR UP. LET’S GO.','Caption'),
(15.25,18.10,'ONE RIDE. ONE BIG SMILE.','Caption'),
(18.30,22.20,'MAKE WEEKENDS AN ADVENTURE.','Caption'),
(22.50,26.70,'THEIR ADVENTURE. YOUR SHARED MEMORIES.','Caption'),
(27.00,29.95,'BIG DREAMS START HERE.\nEXPLORE THE BIKE.','End')]
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
cmd=[f,'-v','warning','-y','-i','/Users/jayden/Downloads/30秒儿童电摩版本.mp4','-vf',f"ass=filename='{ass}':fontsdir='/System/Library/Fonts/Supplemental'",'-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p','-fps_mode','passthrough','-c:a','copy','-movflags','+faststart','-map_metadata','-1',str(out)]
with (p/'render.log').open('w') as log:subprocess.run(cmd,stdout=log,stderr=log,check=True)
print(out)
