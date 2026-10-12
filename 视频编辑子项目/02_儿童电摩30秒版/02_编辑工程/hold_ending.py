import cv2,subprocess,imageio_ffmpeg
src='/Users/jayden/Downloads/30秒儿童电摩版本_英文字幕版.mp4';out='/Users/jayden/Downloads/30秒儿童电摩版本_英文字幕_定格结尾版.mp4'
c=cv2.VideoCapture(src)
cmd=[imageio_ffmpeg.get_ffmpeg_exe(),'-v','error','-y','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','24','-i','-','-i',src,'-map','0:v','-map','1:a','-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p','-af','atrim=duration=30,asetpts=PTS-STARTPTS','-c:a','aac','-b:a','192k','-t','30','-movflags','+faststart','-map_metadata','-1',out]
w=subprocess.Popen(cmd,stdin=subprocess.PIPE)
for i in range(720):
 if i<684:
  ok,frame=c.read();assert ok
 w.stdin.write(frame.tobytes())
w.stdin.close();assert w.wait()==0;c.release()
c=cv2.VideoCapture(out);n=int(c.get(cv2.CAP_PROP_FRAME_COUNT));print('Frames',n,'FPS',c.get(cv2.CAP_PROP_FPS));assert n==720
c.set(cv2.CAP_PROP_POS_FRAMES,719);ok,frame=c.read();assert ok and frame.mean()>80;cv2.imwrite('outputs/video_review/30s/final_hold.jpg',frame);print('Last frame visible',float(frame.mean()));c.release()
subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-v','error','-i',out,'-f','null','-'],check=True)
