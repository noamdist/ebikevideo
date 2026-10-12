from pathlib import Path
import subprocess, json
import imageio_ffmpeg
src='/Users/jayden/Downloads/Little_Rider_Big_Adventures_80s_v2.mp4'
out=Path('/Users/jayden/Downloads/Little_Rider_Big_Adventures_Jayden_Edit_v3.mp4')
segments=[(0,5.7,1.12),(10.15,25.55,1.08),(30.5,34.85,1.06),(38.5,49.5,1.08),(50,58.8,1.08),(60.55,65.2,1.06),(69.4,70.2,1),(6.5,9.85,1)]
filters=[]
for i,(a,b,s) in enumerate(segments):
 dur=(b-a)/s
 filters += [f'[0:v]trim=start={a}:end={b},setpts=(PTS-STARTPTS)/{s},fps=24,setsar=1[v{i}]',f'[0:a]atrim=start={a}:end={b},asetpts=PTS-STARTPTS,atempo={s},afade=t=in:d=0.025,afade=t=out:st={dur-0.025}:d=0.025[a{i}]']
n=len(segments);duration=sum((b-a)/s for a,b,s in segments)
filters += [''.join(f'[v{i}][a{i}]' for i in range(n))+f'concat=n={n}:v=1:a=1[vc][ac]',f'[vc]fade=t=out:st={duration-0.6}:d=0.6[v]',f'[ac]afade=t=out:st={duration-1.2}:d=1.2[a]']
Path('outputs/video_review/edit_decisions.json').write_text(json.dumps({'source':src,'output':str(out),'duration':duration,'segments':segments},indent=2))
cmd=[imageio_ffmpeg.get_ffmpeg_exe(),'-hide_banner','-y','-i',src,'-filter_complex',';'.join(filters),'-map','[v]','-map','[a]','-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart','-map_metadata','-1',str(out)]
with open('outputs/video_review/render.log','w') as log: subprocess.run(cmd,stdout=log,stderr=log,check=True)
print(json.dumps({'output':str(out),'duration':duration,'bytes':out.stat().st_size}))
