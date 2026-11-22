"""G1-pending geometry probe, not an animatic or character design."""
import argparse, json, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
S=3; W=1080; H=1920; FPS=24; N=840
WALL=(222,216,207); FRAME=(77,66,60); STORE=(185,65,57); HAND=(89,155,163)
MSGS=[('M01',0,2.4,'今日、飲み来る？',0),('M02',.9,3,'行けたら行く',1),('M03',4.5,8,'ちょっと遠いし',1),('M04',14,17,'部屋着だし',1),('M05',24,27,'ごめん、今日は行かない',1),('M06',29,32.1,'助かる。俺も今、布団',0)]
def box(r): return tuple(round(v*S) for v in r)
def rect(d,r,c): d.rectangle(box(r),fill=c)
def ease(t,a,b):
    u=max(0,min(1,(t-a)/(b-a))); return u*u*(3-2*u)
def frame(t,font,small):
    im=Image.new('RGB',(W,H),WALL); d=ImageDraw.Draw(im)
    rect(d,(0,0,359,64),(42,48,57)); d.text((54,36),'EP001 | TECH ONLY / NO ART',font=small,fill='white')
    d.text((54,108),f'G1 PENDING  {t:05.2f}s',font=small,fill='white')
    layer=Image.new('RGB',(W,H),(169,186,188)); ld=ImageDraw.Draw(layer)
    ld.polygon([(x*S,y*S) for x,y in [(105,530),(294,530),(237,350),(163,350)]],fill=(209,196,169))
    rect(ld,(174,305,225,375),(113,135,143))
    if t<24.65:
        u=ease(t,5,7.4); y=305-85*u; w=50+150*u; h=55+74*u
        rect(ld,(200-w/2,y,200+w/2,y+h),STORE)
        for dx in (-.32,0,.32):
            x=200+w*dx; rect(ld,(x-1,y+4,x+1,y+h-2),(237,171,131))
        if 17<=t<24.65:
            rect(ld,(156,363,272,398),(255,245,206)); ld.text((495,1107),'部屋着歓迎',font=font,fill=(38,38,38))
    aperture=box((105,220,294,530)); im.paste(layer.crop(aperture),aperture[:2]); d=ImageDraw.Draw(im)
    edge=min(294,105+189*(1-ease(t,1.15,2.05)+.22*ease(t,16.2,17)))
    if edge>106: d.polygon([(round(x*S),round(y*S)) for x,y in [(105,220),(edge,230),(edge,519),(105,530)]],fill=(124,104,89))
    for r in [(97,212,104,538),(294,212,302,538),(97,212,302,219),(97,530,302,538)]: rect(d,r,FRAME)
    rect(d,(88,448,113,465),HAND)
    for mid,a,b,txt,side in MSGS:
        if a<=t<b:
            y=75 if mid=='M01' else 119; width=font.getlength(txt)/S+16; left=286-width if side else 16
            assert left>=12 and left+width<=306
            d.rounded_rectangle(box((left,y,left+width,y+34)),radius=18,fill=(198,228,206) if side else (250,250,247)); d.text((round((left+8)*S),(y+4)*S),txt,font=font,fill=(31,36,40))
    rect(d,(306,220,307,538),(130,130,130)); rect(d,(12,550,300,551),(130,130,130)); d.text((48,1695),'MASK / DEPTH / TEXT ONLY',font=small,fill=(50,50,50))
    return im
def main():
    p=argparse.ArgumentParser(); p.add_argument('--font',required=True); p.add_argument('--out',type=Path,required=True); a=p.parse_args(); a.out.mkdir(parents=True,exist_ok=True)
    font=ImageFont.truetype(a.font,48,index=0); small=ImageFont.truetype(a.font,33,index=0)
    widths={mid:round(font.getlength(txt),2) for mid,_,_,txt,_ in MSGS}; widths['S01']=round(font.getlength('部屋着歓迎'),2); assert max(widths.values())<=660
    checks=[]; previous=None
    for name,t in [('closed',.5),('far',2.2),('mid',6.2),('near',8.5),('sign',18),('before',24.5),('gone',25),('reply',30)]:
        im=frame(t,font,small); im.resize((360,640),Image.Resampling.LANCZOS).save(a.out/f'{name}.png')
        def px(x,y): return im.getpixel((x*S,y*S))
        assert px(95,300)==WALL and px(99,300)==FRAME and px(100,455)==HAND and px(110,455)==HAND
        if name=='far': assert px(210,335)==STORE
        if name=='near': assert px(285,260)==STORE and px(303,260)==WALL
        if name=='gone':
            assert px(285,260)!=STORE and px(200,335)!=STORE
            for x,y in [(100,455),(110,455),(99,300),(125,300),(298,300)]: assert px(x,y)==previous.getpixel((x*S,y*S))
        if name=='before': previous=im
        checks.append(name)
    cmd=['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-an','-c:v','libx264','-threads','4','-preset','ultrafast','-crf','20','-pix_fmt','yuv420p','-movflags','+faststart',str(a.out/'probe.mp4')]
    with subprocess.Popen(cmd,stdin=subprocess.PIPE) as proc:
        for i in range(N): proc.stdin.write(frame(i/FPS,font,small).tobytes())
        proc.stdin.close(); assert proc.wait()==0
    subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(a.out/'probe.mp4'),'-f','null','-'],check=True)
    probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(a.out/'probe.mp4')]))
    v=probe['streams'][0]; assert (v['width'],v['height'],v['codec_name'],v['nb_read_frames'])==(W,H,'h264',str(N)); assert v['r_frame_rate']=='24/1' and len(probe['streams'])==1
    report={'frames':N,'fps':FPS,'duration':probe['format']['duration'],'pixel_checks':checks,'widths_px':widths,'audio':'intentionally absent','decode':'PASS'}
    (a.out/'qa.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8'); print(json.dumps(report,ensure_ascii=False))
if __name__=='__main__': main()
