from pathlib import Path
import json,html,re
from PIL import ImageFont
P=Path(__file__).resolve().parent
D=46.8
# Compared independent Vietnamese Zipformer and multilingual Whisper turbo outputs;
# clear phonetic errors corrected; wording simplified only in repeated filler.
CAPS=[
(.15,2.05,'Em muốn góp 15 triệu'),
(2.25,3.75,'mà không thẩm định người thân,'),
(3.9,5.12,'nhưng năm nay em chỉ mới'),
(5.13,5.98,'18 tuổi,'),
(6.0,7.95,'thì bên em có hỗ trợ được không ạ?'),
(8.15,9.28,'OK em.'),
(9.3,11.0,'Hiện tại bên em chỉ cần có'),
(11.01,11.87,'căn cước công dân,'),
(11.88,13.5,'đủ từ 18 tuổi trở lên,'),
(13.82,15.24,'không cần chứng minh thu nhập,'),
(15.25,16.65,'không thẩm định người thân.'),
(16.83,18.66,'Hạn mức bên em hỗ trợ lên đến từ'),
(18.68,20.55,'15–50 triệu đồng,'),
(20.55,21.06,'em ạ.'),
(21.38,23.14,'Đó là con số khá là lớn'),
(23.15,24.75,'đối với những bạn ở tầm tuổi này.'),
(24.94,26.19,'Nhưng mà bên em hiện tại'),
(26.2,27.32,'có thể hỗ trợ được.'),
(27.42,28.4,'Hiện tại,'),
(28.41,29.87,'anh chỉ có thể hỗ trợ được tại'),
(29.88,31.3,'TP Đà Nẵng'),
(31.31,32.99,'và TP Quy Nhơn mà thôi.'),
(33.22,34.74,'Nên là bạn nào mà'),
(34.75,36.7,'đang ở trong 2 thành phố này,'),
(36.75,37.89,'mà có nhu cầu thì cứ'),
(37.9,39.17,'liên hệ cho bên em'),
(39.23,40.76,'để được hỗ trợ tư vấn'),
(40.78,42.43,'và hỗ trợ lên hồ sơ trực tiếp'),
(42.44,43.57,'tại tỉnh, thành phố'),
(43.58,45.15,'mình đang ở luôn em nhé.'),
]
HEADS=[
(.15,7.95,'CÂU HỎI THƯỜNG GẶP','18 TUỔI','GÓP 15 TRIỆU?',68,'question'),
(9.3,11.87,'GIẤY TỜ','CĂN CƯỚC','CÔNG DÂN',62,'id'),
(11.88,13.55,'ĐỘ TUỔI','TỪ 18 TUỔI','TRỞ LÊN',62,'age'),
(13.82,15.24,'THU NHẬP','KHÔNG CẦN','CHỨNG MINH THU NHẬP',56,'id'),
(15.25,16.66,'NGƯỜI THÂN','KHÔNG','THẨM ĐỊNH NGƯỜI THÂN',60,'people'),
(16.83,24.8,'HẠN MỨC CÓ THỂ HỖ TRỢ','15–50 TRIỆU','',67,'range'),
(29.88,33.02,'HIỆN CHỈ HỖ TRỢ','ĐÀ NẴNG','& QUY NHƠN',67,'pin'),
(34.75,37.89,'KHU VỰC HỖ TRỢ','2 THÀNH PHỐ','ĐÀ NẴNG • QUY NHƠN',54,'pin'),
(37.9,40.77,'ĐANG CÓ NHU CẦU?','LIÊN HỆ','ĐỂ ĐƯỢC TƯ VẤN',68,'message'),
(40.78,D,'HỖ TRỢ HỒ SƠ','TRỰC TIẾP','TẠI THÀNH PHỐ BẠN ĐANG Ở',62,'pin'),
]
# Per-video override: only 2 punch-ins, each followed by a return; no zoom on hook/CTA.
ZOOMS=[]
ILLUSTRATIONS=[(11.0,13.55,0,'Giấy tờ'),(13.82,16.65,1,'Hồ sơ'),(29.9,33.05,2,'Địa điểm'),(37.9,40.76,3,'Liên hệ'),(41.0,45.2,1,'Hồ sơ trực tiếp')]
ICONS={
'question':'<path d="M18 17h44v31H42L28 60V48H18z"/><path d="M34 27c0-9 17-10 17 0 0 6-8 6-8 12M43 44v1"/>',
'people':'<circle cx="28" cy="25" r="10"/><path d="M10 59v-8c0-17 36-17 36 0v8M52 15a10 10 0 010 20M56 43c12 0 17 7 17 16"/>',
'id':'<rect x="8" y="15" width="64" height="46" rx="6"/><circle cx="26" cy="32" r="7"/><path d="M15 51q11-15 22 0M46 29h16M46 39h16M46 49h11"/>',
'age':'<circle cx="40" cy="38" r="27"/><path d="M30 25v26M49 25c-12 0-12 13 0 13 12 0 12 13 0 13-12 0-12-13 0-13 12 0 12-13 0-13z"/>',
'range':'<path d="M9 52h61M15 47V34M31 47V27M47 47V18M63 47V10M10 21l17-5 14 2 23-13"/>',
'pin':'<path d="M40 67S17 43 17 28a23 23 0 1146 0c0 15-23 39-23 39z"/><circle cx="40" cy="28" r="8"/>',
'message':'<path d="M10 13h60v41H41L24 68V54H10zM23 27h34M23 39h24"/>'
}
font=P/'BeVietnamPro-ExtraBold.ttf'
def width(t,s):return ImageFont.truetype(str(font),s).getlength(t)
def fit(t,s,mw):
 while s>22 and width(t,s)>mw:s-=1
 return s
def wrap(t,maxsize=38,mw=562):
 for size in range(maxsize,29,-1):
  lines=[];line=''
  for word in t.split():
   nxt=(line+' '+word).strip()
   if width(nxt,size)>mw and line:lines.append(line);line=word
   else:line=nxt
  if line:lines.append(line)
  if len(lines)<=2:return lines,size
 raise ValueError(t)
HOT=re.compile(r'18 tuổi|15–50 triệu|15 triệu|căn cước công dân|Đà Nẵng|Quy Nhơn|không cần|liên hệ|trực tiếp',re.I)
def styled(t):return HOT.sub(lambda m:'<strong class="hot">'+m[0]+'</strong>',html.escape(t))
clips=[]
for i,(a,b,t) in enumerate(CAPS):
 ll,sz=wrap(t)
 body=''.join('<span class="caption-line">'+styled(z)+'</span>' for z in ll)
 clips.append(f'<div id="cap{i}" class="clip caption" data-start="{a}" data-duration="{b-a:.3f}" data-track-index="3"><div class="caption-inner" style="font-size:{sz}px">{body}</div></div>')
for i,(a,b,tag,main,sub,sz,icon) in enumerate(HEADS):
 sz=fit(main,sz,550);ss=fit(sub,32,548);ts=fit(tag,17,480)
 body=f'<div class="title-content"><div class="eyebrow"><svg viewBox="0 0 80 80">{ICONS[icon]}</svg><span style="font-size:{ts}px">{tag}</span></div><div class="main-title" style="font-size:{sz}px">{main}</div>'
 if sub:body+=f'<div class="sub-title" style="font-size:{ss}px">{sub}</div>'
 body+='<div class="rule"><i class="rule-line"></i><i class="rule-dot"></i></div></div>'
 clips.append(f'<div id="head{i}" class="clip headline" data-start="{a}" data-duration="{b-a:.3f}" data-track-index="4">{body}</div>')
for i,(a,b,q,label) in enumerate(ILLUSTRATIONS):
 x=-(q%2)*100;y=-(q//2)*100
 body=f'<div class="sticker-window" data-layout-ignore><img src="illustrations.png" alt="" style="left:{x}%;top:{y}%"></div>'
 clips.append(f'<div id="ill{i}" class="clip illustration" data-start="{a}" data-duration="{b-a:.3f}" data-track-index="5" aria-label="{label}">{body}</div>')
css='''@font-face{font-family:BeVietnam;src:url('BeVietnamPro-ExtraBold.ttf');font-weight:800}
*{box-sizing:border-box;margin:0}html,body{width:720px;height:1280px;overflow:hidden;background:#151a20;color:#fff;font-family:BeVietnam,sans-serif}
#main{position:relative;width:720px;height:1280px;overflow:hidden}
#footage{position:absolute;inset:0;z-index:0;transform-origin:48% 51%;will-change:transform}video{width:720px;height:1280px;object-fit:cover}
.vignette{position:absolute;inset:0;z-index:1;pointer-events:none;background:radial-gradient(ellipse at center,transparent 64%,rgba(0,0,0,.12) 100%)}
.headline{position:absolute;inset:0;width:100%;height:100%;padding:55px 98px 0 58px;display:flex;align-items:flex-start;justify-content:center;z-index:3;pointer-events:none}
.title-content{width:100%;height:190px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:7px;text-align:center}
.eyebrow{display:flex;align-items:center;justify-content:center;gap:7px;color:#fff;line-height:1.35;letter-spacing:.8px;-webkit-text-stroke:1.8px #0b1013;paint-order:stroke fill;text-shadow:0 2px 4px #151a20}
.eyebrow svg{width:28px;height:28px;stroke:#85e9de;stroke-width:4;fill:none;stroke-linecap:round;stroke-linejoin:round;filter:drop-shadow(0 2px 2px #151a20)}
.main-title{line-height:1.18;letter-spacing:-1.7px;max-width:560px;white-space:nowrap;-webkit-text-stroke:3px #151a20;paint-order:stroke fill;text-shadow:0 4px 5px #151a20;font-variant-numeric:tabular-nums}
.sub-title{line-height:1.22;letter-spacing:-.3px;color:#85e9de;max-width:555px;-webkit-text-stroke:2.5px #151a20;paint-order:stroke fill;text-shadow:0 3px 4px #151a20}
.rule{width:116px;height:6px;margin-top:3px;position:relative}.rule-line{display:block;width:100%;height:3px;border-radius:2px;background:#85e9de;box-shadow:0 1px 3px #151a20;transform-origin:0 50%}.rule-dot{position:absolute;right:-5px;top:-2px;width:7px;height:7px;border-radius:50%;background:#fff;box-shadow:0 0 6px #85e9de}
.caption{position:absolute;left:0;top:908px;width:100%;height:136px;padding:0 98px 0 52px;display:flex;align-items:center;justify-content:center;text-align:center;z-index:3;pointer-events:none}
.illustration{position:absolute;right:70px;top:245px;width:165px;height:165px;z-index:4;pointer-events:none}.sticker-window{position:relative;width:100%;height:100%;overflow:hidden}.sticker-window img{position:absolute;display:block;width:200%;height:200%;max-width:none;object-fit:contain;filter:drop-shadow(0 3px 3px rgba(0,0,0,.22))}.caption-inner{max-width:570px;line-height:1.28;letter-spacing:-.5px;-webkit-text-stroke:3.8px #151a20;paint-order:stroke fill;text-shadow:0 3px 4px #151a20}.caption-line{display:block}.hot{font-weight:800;color:#123e3a;-webkit-text-stroke:1.1px #fff;text-shadow:0 1px 1px rgba(255,255,255,.4);text-decoration:underline;text-decoration-color:#123e3a;text-decoration-thickness:2px;text-underline-offset:6px}
'''
js=['const tl=gsap.timeline({paused:true});window.__timelines=window.__timelines||{};']
for a,s,d in ZOOMS:js.append(f"tl.to('#footage',{{scale:{s},duration:{d},ease:'power2.inOut'}},{a});")
for i,(a,b,t) in enumerate(CAPS):
 js.append(f"tl.from('#cap{i} .caption-inner',{{y:10,scale:.97,opacity:0,duration:.16,ease:'power3.out'}},{a});tl.set('#cap{i}',{{opacity:0}},{b});")
for i,(a,b,tag,main,sub,sz,icon) in enumerate(HEADS):
 js.append(f"tl.from('#head{i} .eyebrow',{{x:-14,opacity:0,duration:.22,ease:'power3.out'}},{a});")
 js.append(f"tl.from('#head{i} .main-title',{{y:16,scale:.91,opacity:0,duration:.3,ease:'back.out(1.3)'}},{a+.05:.3f});")
 if sub:js.append(f"tl.from('#head{i} .sub-title',{{y:12,opacity:0,duration:.25,ease:'sine.out'}},{a+.12:.3f});")
 js.append(f"tl.from('#head{i} .rule-line',{{scaleX:0,duration:.35,ease:'expo.out'}},{a+.15:.3f});tl.from('#head{i} .rule-dot',{{scale:0,opacity:0,duration:.22,ease:'power2.out'}},{a+.23:.3f});tl.set('#head{i}',{{opacity:0}},{b});")
# Chromatic micro-glitch on 2 emphases, never sustained over the whole clip.
for i,t in []:
 js.extend([f"tl.to('#head{i} .main-title',{{x:3,textShadow:'-3px 0 #85e9de,3px 0 #e4eeee',duration:.04,ease:'none'}},{t});",f"tl.to('#head{i} .main-title',{{x:-2,duration:.04,ease:'none'}},{t+.04});",f"tl.to('#head{i} .main-title',{{x:0,textShadow:'0 4px 5px #151a20',duration:.07,ease:'power1.out'}},{t+.08});"])
for i,(a,b,q,label) in enumerate(ILLUSTRATIONS):
 js.append(f"tl.from('#ill{i}',{{x:14,y:8,scale:.86,opacity:0,duration:.3,ease:'back.out(1.2)'}},{a});tl.set('#ill{i}',{{opacity:0}},{b});")
js.append("window.__timelines['main']=tl;")
(P/'index.html').write_text(f'''<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=720,height=1280"><script src="gsap.min.js"></script><style>{css}</style></head><body><div id="main" data-composition-id="main" data-start="0" data-duration="{D}" data-width="720" data-height="1280" data-fps="30"><div id="footage"><video id="source-video" class="clip" src="source.mp4" muted playsinline data-start="0" data-duration="{D}" data-track-index="0"></video></div><audio id="mix" src="mix.wav" data-start="0" data-duration="{D}" data-track-index="2" data-volume="1"></audio><div class="vignette" data-layout-ignore></div>{''.join(clips)}</div><script>{''.join(js)}</script></body></html>''')
(P/'captions.json').write_text(json.dumps(CAPS,ensure_ascii=False,indent=2))
(P/'edit-plan.json').write_text(json.dumps({'duration':D,'headlines':HEADS,'illustrations':ILLUSTRATIONS,'source_range':[0,46.8],'zoom_tweens':ZOOMS,'censor_intervals':[],'censor_note':'Both recognizers identify góp; vay and nợ xấu were not detected. No unrelated words muted.','per_video_override':'Latest correction: preserve the full original talking-head video and speech. No footage zoom/crop, no content replacement or trimming. Add small illustrative photos and synchronized effects; prior educational replacement is not the requested edit.','asset_note':'New transparent illustrative atlas: generic anonymous card, forms, abstract map pins and blank smartphone chat. No real identity data, government insignia, real provider details or approval claims.','transcript_review':'Zipformer timestamped transcription compared to Whisper turbo in 2 chunks; obvious phonetic errors corrected (người thân, căn cước công dân, Đà Nẵng, Quy Nhơn). Redundant filler shortened in captions. No direct auditory review claimed.'},ensure_ascii=False,indent=2))
print(f'Built {len(CAPS)} caption groups, {len(HEADS)} titles, {len(ZOOMS)} zoom/return tweens; {D}s')
