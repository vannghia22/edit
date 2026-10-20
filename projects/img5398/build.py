from pathlib import Path
import json,re,html
from PIL import ImageFont

P=Path(__file__).resolve().parent
D=50.3
# Wording corrected from two local ASR passes; filler/pronouns shortened without changing conditions.
CAPS=[
(.28,1.55,'Em mới 18 tuổi,'),
(1.55,3.14,'em muốn góp 15 triệu'),
(3.14,4.90,'mà không thẩm định người thân,'),
(4.90,6.76,'thì có hỗ trợ được không ạ?'),
(7.72,8.30,'OK em,'),
(8.30,10.18,'xin phép trả lời thắc mắc của em.'),
(10.92,12.02,'Thì hiện tại,'),
(12.02,14.10,'chỉ cần có căn cước công dân,'),
(14.10,16.16,'đủ từ 18 tuổi trở lên,'),
(16.16,18.18,'không cần chứng minh thu nhập,'),
(18.18,19.54,'không cần thẩm định người thân'),
(19.54,21.96,'thì đã có thể hỗ trợ được rồi nha em.'),
(21.96,24.10,'Hiện tại hạn mức có thể hỗ trợ'),
(24.10,26.60,'không thẩm định có thể lên đến'),
(26.60,29.64,'15–50 triệu đồng.'),

(29.64,31.56,'Còn nếu như có thể thẩm định'),
(31.56,33.72,'thì sẽ có nhiều lựa chọn hơn.'),
(33.72,35.40,'Nhưng mà hiện tại,'),
(35.40,38.00,'chỉ hỗ trợ tại Đà Nẵng mà thôi.'),
(38.00,40.12,'Bạn nào đang có nhu cầu'),
(40.12,42.50,'thì cứ inbox để được hỗ trợ.'),
(42.50,44.52,'Hỗ trợ tư vấn và lên hồ sơ'),
(44.52,47.92,'trực tiếp tại Đà Nẵng.'),
]
HEADS=[
(.12,7.10,'GIẢI ĐÁP','18 TUỔI','CẦN 15 TRIỆU?',108),
(7.72,12.02,'ĐIỀU KIỆN','HỖ TRỢ','CẦN NHỮNG GÌ?',98),
(12.02,14.10,'GIẤY TỜ','CĂN CƯỚC','CÔNG DÂN',100),
(14.10,16.16,'ĐỘ TUỔI','TỪ 18 TUỔI','TRỞ LÊN',102),
(16.16,18.18,'THỦ TỤC','KHÔNG CẦN','CHỨNG MINH THU NHẬP',94),
(18.18,21.96,'THỦ TỤC','KHÔNG CẦN','THẨM ĐỊNH NGƯỜI THÂN',94),
(21.96,29.64,'HẠN MỨC CÓ THỂ HỖ TRỢ','15–50 TRIỆU','KHÔNG THẨM ĐỊNH',105),
(29.64,33.72,'NẾU CÓ THẨM ĐỊNH','THÊM LỰA CHỌN','',74),
(33.72,38.00,'HIỆN CHỈ HỖ TRỢ','ĐÀ NẴNG','KHU VỰC HỖ TRỢ',112),
(38.00,42.50,'ĐANG CÓ NHU CẦU?','INBOX','ĐỂ ĐƯỢC TƯ VẤN',110),
(42.50,D,'TƯ VẤN & HỒ SƠ','TRỰC TIẾP','TẠI ĐÀ NẴNG',98),
]
# Clear punch-ins with deliberate return to the wide shot. No overlapping zoom tweens.
ZOOMS=[(.15,1.14,.30),(3.00,1.0,.35),(4.90,1.18,.28),(7.05,1.0,.38),
 (12.02,1.12,.30),(13.55,1.0,.30),(14.13,1.18,.28),(15.75,1.0,.30),
 (16.23,1.12,.28),(18.22,1.18,.24),(20.60,1.0,.40),
 (26.60,1.18,.30),(28.90,1.0,.40),(29.80,1.12,.30),(32.95,1.0,.38),
 (35.40,1.17,.28),(38.00,1.0,.35),(40.12,1.14,.28),(42.15,1.02,.30),
 (44.52,1.17,.30),(48.35,1.0,.40)]
ICONS={
 'id':'<rect x="18" y="27" width="150" height="108" rx="12"/><circle cx="58" cy="65" r="15"/><path d="M35 110q23-30 46 0M101 61h44M101 82h35M101 103h44"/>',
 'doc':'<path d="M45 15h72l29 29v106H45zM117 15v30h29M67 72h55M67 94h40"/><path d="M80 122l14 13 30-35"/>',
 'pin':'<path d="M95 151S40 92 40 62a55 48 0 01110 0c0 30-55 89-55 89z"/><circle cx="95" cy="62" r="19"/>',
 'chat':'<path d="M24 27h139v94H86l-34 29v-29H24zM53 59h82M53 83h56"/>',
 'choice':'<path d="M40 140V85h90M85 40l40 40-40 40M40 85V35"/>',
}
FOOTS=[(12.02,16.16,'id','CĂN CƯỚC CÔNG DÂN'),(16.16,21.96,'doc','THỦ TỤC HỖ TRỢ'),
 (29.64,33.72,'choice','CÓ THẨM ĐỊNH → THÊM LỰA CHỌN'),(35.40,38.00,'pin','ĐÀ NẴNG'),
 (40.12,D,'chat','INBOX ĐỂ ĐƯỢC TƯ VẤN')]

def font(sz):return ImageFont.truetype(str(P/'BeVietnamPro-ExtraBold.ttf'),sz)
def fit(s,size,width):
 while font(size).getlength(s)>width and size>36:size-=1
 return size
def lines(s):
 s=s.upper()
 s=re.sub(r'(\d+) (TUỔI|TRIỆU)',lambda m:m[1]+'\u00a0'+m[2],s)
 words=s.split(' ')
 for size in range(63,49,-1):
  f=font(size)
  if f.getlength(s)<=820:return [s],size
  candidates=[]
  for i in range(1,len(words)):
   left=' '.join(words[:i]);right=' '.join(words[i:]);wl=f.getlength(left);wr=f.getlength(right)
   if max(wl,wr)<=820:candidates.append((abs(wl-wr),left,right))
  if candidates:
   _,left,right=min(candidates)
   return [left,right],size
 raise ValueError('Caption too long: '+s)
HOT=re.compile(r'18[\s\u00a0]+TUỔI|15–50[\s\u00a0]+TRIỆU|15[\s\u00a0]+TRIỆU|50[\s\u00a0]+TRIỆU|CĂN CƯỚC|CÔNG DÂN|KHÔNG CẦN|THU NHẬP|NGƯỜI THÂN|ĐÀ NẴNG|INBOX|TRỰC TIẾP|THẨM ĐỊNH')
def hot(s):return HOT.sub(lambda m:'<strong class="hot">'+m[0]+'</strong>',html.escape(s))
clips=[];timed=[]
def clip(id,cls,a,b,body,track):
 timed.append((id,cls,a,b));return f'<div id="{id}" class="clip {cls}" data-start="{a}" data-duration="{b-a:.3f}" data-track-index="{track}">{body}</div>'
for i,(a,b,t) in enumerate(CAPS):
 if not t:continue
 ll,size=lines(t)
 assert len(ll)<=2,(i,t)
 body='<div class="caption-inner" style="font-size:'+str(size)+'px">'+''.join('<span class="caption-line">'+hot(l)+'</span>' for l in ll)+'</div>'
 clips.append(clip('cap'+str(i),'caption',a,b,body,3))
for i,(a,b,tag,main,sub,size) in enumerate(HEADS):
 size=fit(main,size,790);ss=fit(sub,51,800)
 body=f'<div class="title-panel"><span class="chapter">{tag}</span><div class="title-main" style="font-size:{size}px">{main}</div><div class="title-sub" style="font-size:{ss}px">{sub}</div><div class="title-rule"></div><i class="corner corner-a"></i><i class="corner corner-b"></i></div>'
 clips.append(clip('head'+str(i),'headline',a,b,body,4))
for i,(a,b,icon,t) in enumerate(FOOTS):
 fs=fit(t,36,650)
 body=f'<div class="foot-inner"><svg viewBox="0 0 190 170" aria-hidden="true">{ICONS[icon]}</svg><span class="foot-text" style="font-size:{fs}px">{t}</span></div>'
 clips.append(clip('foot'+str(i),'foot',a,b,body,5))
css='''@font-face{font-family:BeVietnam;src:url('BeVietnamPro-ExtraBold.ttf');font-weight:800}
*{box-sizing:border-box;margin:0}html,body{width:1080px;height:1920px;overflow:hidden;background:#101116;color:#fff;font-family:BeVietnam,sans-serif}
#main{position:relative;width:1080px;height:1920px;overflow:hidden}
#footage{position:absolute;inset:0;z-index:0;transform-origin:50% 48%}video{width:1080px;height:1920px;object-fit:cover}
.vignette{position:absolute;inset:0;z-index:1;pointer-events:none;background:radial-gradient(ellipse at center,transparent 60%,rgba(0,0,0,.16) 100%)}
.headline{position:absolute;inset:0;width:100%;height:490px;padding:140px 130px 20px 70px;display:flex;align-items:flex-start;justify-content:center;z-index:3}
.title-panel{position:relative;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:11px;width:880px;height:310px;padding:28px 24px 24px;background:linear-gradient(110deg,rgba(16,17,22,.58),rgba(16,17,22,.27));border-radius:22px;border:1px solid rgba(255,230,107,.5);box-shadow:0 8px 24px rgba(0,0,0,.15)}
.chapter{font-size:26px;line-height:1.25;letter-spacing:2.2px;color:#ffe66b;text-shadow:0 2px 4px #101116}
.title-main{line-height:1.12;letter-spacing:-2.4px;text-align:center;color:#ffe66b;-webkit-text-stroke:2px #101116;paint-order:stroke fill;text-shadow:0 5px 4px #101116;font-variant-numeric:tabular-nums}
.title-sub{line-height:1.15;text-align:center;color:#fff;-webkit-text-stroke:2px #101116;paint-order:stroke fill;text-shadow:0 3px 4px #101116}
.title-rule{width:130px;height:5px;border-radius:4px;background:#ffe66b;margin-top:3px}
.corner{position:absolute;display:block;width:46px;height:46px;pointer-events:none;border-color:#ffe66b;border-style:solid}
.corner-a{top:-2px;left:-2px;border-width:5px 0 0 5px;border-radius:20px 0 0 0}.corner-b{bottom:-2px;right:-2px;border-width:0 5px 5px 0;border-radius:0 0 20px 0}
.caption{position:absolute;left:0;top:1305px;width:100%;height:200px;padding:0 140px 0 80px;display:flex;align-items:center;justify-content:center;text-align:center;z-index:3}
.caption-inner{max-width:840px;line-height:1.22;letter-spacing:-1px;-webkit-text-stroke:5px #101116;paint-order:stroke fill;text-shadow:0 4px 6px #101116}
.caption-line{display:block}.hot{font-weight:800;color:#ffe66b}
.foot{position:absolute;left:0;top:1550px;width:100%;height:150px;padding:10px 145px 10px 85px;z-index:3}
.foot-inner{width:100%;height:100%;display:flex;align-items:center;justify-content:center;gap:18px}
svg{width:105px;height:105px;flex-shrink:0;fill:none;stroke:#ffe66b;stroke-width:5;stroke-linecap:round;stroke-linejoin:round;filter:drop-shadow(0 2px 3px #101116)}
.foot-text{color:#fff;max-width:650px;line-height:1.25;-webkit-text-stroke:2px #101116;paint-order:stroke fill;text-shadow:0 3px 5px #101116}
.progress{position:absolute;left:80px;right:140px;top:1755px;height:4px;z-index:3;background:rgba(16,17,22,.35)}.progress-fill{width:100%;height:100%;background:#ffe66b;transform-origin:left}
'''
js="const tl=gsap.timeline({paused:true});window.__timelines=window.__timelines||{};\n"
js+=f"tl.fromTo('.progress-fill',{{scaleX:0}},{{scaleX:1,duration:{D},ease:'none'}},0);\n"
for a,s,d in ZOOMS:js+=f"tl.to('#footage',{{scale:{s},duration:{d},ease:'power2.inOut'}},{a});\n"
for id,cls,a,b in timed:
 if cls=='headline':
  js+=f"tl.from('#{id} .title-panel',{{y:-20,opacity:0,duration:.25,ease:'power3.out'}},{a});tl.from('#{id} .title-main',{{scale:.88,opacity:0,duration:.32,ease:'back.out(1.4)'}},{a+.05});tl.from('#{id} .title-sub',{{y:12,opacity:0,duration:.25,ease:'sine.out'}},{a+.12});tl.from('#{id} .title-rule',{{scaleX:0,duration:.32,ease:'expo.out'}},{a+.18});\n"
 elif cls=='caption':js+=f"tl.from('#{id} .caption-inner',{{y:14,scale:.97,opacity:0,duration:.15,ease:'power3.out'}},{a});\n"
 else:js+=f"tl.from('#{id} svg',{{scale:.7,rotation:-6,opacity:0,duration:.28,ease:'back.out(1.5)'}},{a});tl.from('#{id} .foot-text',{{x:20,opacity:0,duration:.25,ease:'power2.out'}},{a+.04});\n"
 js+=f"tl.set('#{id}',{{opacity:0}},{b});\n"
js+="window.__timelines['main']=tl;"
doc=f'''<!doctype html><html lang="vi"><head><meta charset="UTF-8"><meta name="viewport" content="width=1080,height=1920"><script src="gsap.min.js"></script><style>{css}</style></head><body><div id="main" data-composition-id="main" data-start="0" data-duration="{D}" data-width="1080" data-height="1920" data-fps="30"><div id="footage" data-layout-ignore><video id="video" class="clip" data-start="0" data-duration="{D}" data-track-index="0" src="graded.mp4" muted playsinline></video></div><audio id="voice-mix" data-start="0" data-duration="{D}" data-track-index="1" src="mix.wav" data-volume="1"></audio><div class="vignette" data-layout-ignore></div>{''.join(clips)}<div class="progress" data-layout-ignore><div class="progress-fill"></div></div></div><script>{js}</script></body></html>'''
(P/'index.html').write_text(doc)
(P/'captions.json').write_text(json.dumps([{'start':a,'end':b,'text':t} for a,b,t in CAPS if t],ensure_ascii=False,indent=2))
(P/'edit-plan.json').write_text(json.dumps({'duration':D,'headers':HEADS,'zoom_tweens':ZOOMS,'illustrations':FOOTS,'censor_intervals':[],'censor_note':'The specified words vay / nợ xấu were not found in the reviewed ASR passes. The opening word is góp in both passes; do not invent a banned-word rule or mute unrelated words.'},ensure_ascii=False,indent=2))
print('Authored',len(clips),'timed overlays;',len(ZOOMS),'zoom tweens')
