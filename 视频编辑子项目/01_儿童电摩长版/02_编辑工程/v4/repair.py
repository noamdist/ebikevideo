from pathlib import Path
import cv2,numpy as np,subprocess,imageio_ffmpeg,json
p=Path('outputs/video_review/v4');src='/Users/jayden/Downloads/Little_Rider_Big_Adventures_80s_v2.mp4'
f=imageio_ffmpeg.get_ffmpeg_exe()
reader=subprocess.Popen([f,'-v','error','-ss','6.5','-i',src,'-t','3.375','-f','rawvideo','-pix_fmt','bgr24','-'],stdout=subprocess.PIPE)
writer=subprocess.Popen([f,'-v','error','-y','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','24','-i','-','-c:v','ffv1',str(p/'studio_fixed.mkv')],stdin=subprocess.PIPE)
poly=np.array([[408,343],[482,374],[461,437],[389,407]],np.float32)
prev=None; records=[];i=0
while True:
 data=reader.stdout.read(1280*720*3)
 if len(data)<1280*720*3:break
 frame=np.frombuffer(data,np.uint8).reshape(720,1280,3).copy();gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
 if prev is not None:
  area=np.zeros_like(gray);cv2.fillConvexPoly(area,np.int32(prevpoly),255);area=cv2.dilate(area,np.ones((31,31),np.uint8))
  pts=cv2.goodFeaturesToTrack(prev,60,.01,4,mask=area)
  nxt,status,err=cv2.calcOpticalFlowPyrLK(prev,gray,pts,None,winSize=(25,25),maxLevel=3)
  ok=status.ravel()==1
  affine,inliers=cv2.estimateAffinePartial2D(pts[ok],nxt[ok],method=cv2.RANSAC,ransacReprojThreshold=2)
  if affine is None:raise RuntimeError(f'Tracking failed {i}')
  poly=cv2.transform(poly[None],affine)[0]
 mask=np.zeros_like(gray);cv2.fillConvexPoly(mask,np.int32(poly),255)
 mask=cv2.bitwise_and(mask,((gray>55)*255).astype(np.uint8));mask=cv2.dilate(mask,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(7,7)))
 fixed=cv2.inpaint(frame,mask,5,cv2.INPAINT_TELEA)
 writer.stdin.write(fixed.tobytes())
 if i%12==0 or i==80:
  cv2.imwrite(str(p/f'fixed_{i:03d}.jpg'),fixed)
 records.append({'frame':i,'poly':poly.tolist(),'mask_pixels':int((mask>0).sum())})
 prev=gray;prevpoly=poly.copy();i+=1
reader.wait();writer.stdin.close();writer.wait();(p/'tracking.json').write_text(json.dumps(records));print(f'Repaired {i} frames')
