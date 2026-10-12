from pathlib import Path
import subprocess,json,imageio_ffmpeg
p=Path('outputs/video_review/v4');src='/Users/jayden/Downloads/Little_Rider_Big_Adventures_80s_v2.mp4';out='/Users/jayden/Downloads/Little_Rider_Big_Adventures_Jayden_Edit_v4.mp4'
# Endpoints use integer source frames, keeping the previous character corrections.
segments=[(0,3.5,1.08),(10.15,25.55,1.08),(30.5,34.85,1.06),(38.5,60.2,1.08),(60.55,66.2,1.06),(6.5,9.85,1)]
transitions=[.36,.25,.28,.20,.42]
filters=[];durations=[]
for i,(a,b,s) in enumerate(segments):
 n=round((b-a)/s*24);dur=n/24;durations.append(dur)
 v=f'[0:v]trim=start={a}:end={b},setpts=(PTS-STARTPTS)/{s}' if i<5 else '[1:v]setpts=PTS-STARTPTS'
 filters.append(v+f',fps=24,trim=end_frame={n},settb=AVTB,setsar=1,format=yuv420p[v{i}]')
 filters.append(f'[0:a]atrim=start={a}:end={b},asetpts=PTS-STARTPTS,atempo={s},apad,atrim=duration={dur}[a{i}]')
prevv='v0';preva='a0';total=durations[0]
for i in range(1,len(segments)):
 overlap=round(transitions[i-1]*24)/24;offset=total-overlap
 filters.append(f'[{prevv}][v{i}]xfade=transition=fade:duration={overlap}:offset={offset}[x{i}]')
 filters.append(f'[{preva}][a{i}]acrossfade=d={overlap}:c1=tri:c2=tri[y{i}]')
 prevv=f'x{i}';preva=f'y{i}';total+=durations[i]-overlap
filters.extend([f'[{prevv}]fade=t=out:st={total-.65}:d=0.65[v]',f'[{preva}]afade=t=in:d=0.08,afade=t=out:st={total-1.25}:d=1.25[a]'])
(p/'v4_decisions.json').write_text(json.dumps({'source':src,'output':out,'segments':segments,'transition_seconds':transitions,'duration':total},indent=2))
cmd=[imageio_ffmpeg.get_ffmpeg_exe(),'-v','warning','-y','-i',src,'-i',str(p/'studio_fixed.mkv'),'-filter_complex_threads','2','-filter_complex',';'.join(filters),'-map','[v]','-map','[a]','-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart','-map_metadata','-1',out]
with (p/'render.log').open('w') as log:subprocess.run(cmd,stderr=log,stdout=log,check=True)
print(json.dumps({'output':out,'duration':total,'bytes':Path(out).stat().st_size}))
