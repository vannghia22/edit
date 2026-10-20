import json, pathlib
p=pathlib.Path(__file__).resolve().parent
caps=[
 (0.10,2.12,'Em hai lẻ bảy,','đang sinh viên.'),
 (2.12,3.36,'Em đang cần v*y khoảng','10 triệu.'),
 (3.36,4.32,'Bên anh có hỗ trợ','không ạ?'),
 (4.90,5.42,'OK bạn.',''),
 (6.70,7.30,'Chỉ cần các bạn có',''),
 (7.30,8.16,'Căn cước công dân,',''),
 (8.16,8.80,'Không n* x*u;',''),
 (9.52,10.35,'Thì mình đều có thể',''),
 (10.35,11.10,'Hỗ trợ được','cho các bạn.'),
 (11.30,12.98,'Bên mình không cần','chứng minh tài chính,'),
 (12.98,13.98,'Không thẩm định','người thân.'),
 (14.10,15.98,'Hồ sơ đậu sẽ được','giải ngân ngay trong ngày.'),
 (16.15,17.15,'Nếu như các bạn','có nhu cầu'),
 (17.15,17.73,'Cần v*y thì hãy',''),
 (17.73,18.38,'Nhắn tin cho mình',''),
 (18.38,18.98,'Ở phía bên dưới.',''),
]
heads=[
 (0.05,4.55,'SINH VIÊN','CẦN 10 TRIỆU?'),
 (5.7,9.14,'ĐIỀU KIỆN','HỖ TRỢ'),
 (9.15,13.92,'THÔNG TIN','HỒ SƠ'),
 (13.92,16.05,'HỒ SƠ ĐẬU','NGAY TRONG NGÀY'),
 (16.12,19.1,'NHẮN TIN','ĐỂ ĐƯỢC TƯ VẤN'),
]
icons={
'money':'<circle cx="85" cy="75" r="50"/><path d="M85 43v64M101 52c-22-16-47 5-24 19l18 10c24 16-2 38-23 18"/><path d="M138 111l31 17-29 16"/>',
'id':'<rect x="21" y="30" width="150" height="108" rx="12"/><circle cx="61" cy="68" r="15"/><path d="M38 113q22-30 45 0M105 64h43M105 85h34M105 106h43"/>',
'doc':'<path d="M48 15h72l29 29v106H48zM120 15v30h29M70 72h55M70 94h40"/><path d="M83 122l14 13 30-35"/>',
'chat':'<path d="M26 30h139v94H88l-34 29v-29H26zM55 62h82M55 86h56"/>',
}
foots=[(0.15,4.55,'money','10 TRIỆU','CÂU HỎI TỪ NGƯỜI XEM'),(7.30,8.80,'id','CĂN CƯỚC','CÔNG DÂN'),(11.08,13.92,'doc','THÔNG TIN HỒ SƠ','THEO NỘI DUNG NGƯỜI NÓI'),(14.10,15.98,'doc','HỒ SƠ ĐẬU','ĐIỀU KIỆN TRƯỚC GIẢI NGÂN'),(16.12,19.1,'chat','NHẮN TIN BÊN DƯỚI','ĐỂ ĐƯỢC TƯ VẤN')]
timings=[]
parts=[]
def clip(id,cl,a,b,body,track):
 timings.append((id,cl,a,b))
 return f'<div id="{id}" class="clip {cl}" data-start="{a}" data-duration="{b-a:.3f}" data-track-index="{track}">{body}</div>'
for i,(a,b,l1,l2) in enumerate(caps):
 body=f'<div class="caption-inner">{l1.upper()}' + (f'<span class="line accent">{l2.upper()}</span>' if l2 else '')+'</div>'
 parts.append(clip(f'cap{i}','caption',a,b,body,3))
for i,(a,b,l1,l2) in enumerate(heads):
 parts.append(clip(f'head{i}','headline',a,b,f'<div class="eyebrow">{l1}</div><div class="main-title">{l2}</div><div class="underline"></div>',4))
for i,(a,b,key,t1,t2) in enumerate(foots):
 body=f'<div class="foot-inner"><svg viewBox="0 0 190 170" aria-hidden="true">{icons[key]}</svg><div class="foot-copy"><div class="foot-title">{t1}</div><div class="foot-sub">{t2}</div></div></div>'
 parts.append(clip(f'foot{i}','foot',a,b,body,5))
html='''<!doctype html><html lang="vi"><head><meta charset="UTF-8"><meta name="viewport" content="width=1080,height=1920"><script src="gsap.min.js"></script><style>
@font-face{font-family:BeVietnam;src:url('BeVietnamPro-ExtraBold.ttf');font-weight:800}
*{box-sizing:border-box;margin:0}html,body{width:1080px;height:1920px;overflow:hidden;background:#101116;font-family:BeVietnam,sans-serif;color:#fff}
#main{position:relative;width:1080px;height:1920px;overflow:hidden}
#footage{position:absolute;inset:0;transform-origin:48% 48%;z-index:0}video{width:1080px;height:1920px;object-fit:cover}
.matte{position:absolute;left:0;width:1080px;pointer-events:none;z-index:1}
.top-matte{top:0;height:560px;background:linear-gradient(to bottom,#101116 0%,#101116 76%,rgba(16,17,22,0) 100%)}
.bottom-matte{top:1210px;height:710px;background:linear-gradient(to bottom,rgba(16,17,22,0) 0%,#101116 10%,#101116 100%)}
.headline{position:absolute;inset:0;z-index:3;width:100%;height:430px;padding:165px 130px 20px 80px;display:flex;flex-direction:column;align-items:center;gap:18px;text-align:center}
.eyebrow{font-size:37px;line-height:1.2;letter-spacing:3px;color:#fff;text-shadow:0 3px 5px #101116}
.main-title{font-size:69px;line-height:1.13;letter-spacing:-2px;color:#ffe66b;-webkit-text-stroke:1px #101116;paint-order:stroke fill;text-shadow:0 4px 0 #101116;font-variant-numeric:tabular-nums}
.underline{width:130px;height:5px;background:#ffe66b;border-radius:3px;margin-top:5px}
.caption{position:absolute;left:0;top:1290px;width:100%;height:185px;padding:0 140px 0 80px;display:flex;align-items:center;justify-content:center;z-index:3;text-align:center}
.caption-inner{max-width:860px;font-size:57px;line-height:1.22;letter-spacing:-1.4px;-webkit-text-stroke:2px #101116;paint-order:stroke fill;text-shadow:0 4px 0 #101116}
.line{display:block}.accent{color:#ffe66b}#cap11 .line{font-size:49px}
.foot{position:absolute;left:0;top:1520px;width:100%;height:185px;padding:10px 145px 10px 85px;z-index:3}
.foot-inner{width:100%;height:100%;display:flex;align-items:center;justify-content:center;gap:24px}
svg{width:140px;height:150px;flex-shrink:0;fill:none;stroke:#ffe66b;stroke-width:5;stroke-linecap:round;stroke-linejoin:round}
.foot-copy{max-width:590px;display:flex;flex-direction:column;gap:12px}
.foot-title{font-size:37px;line-height:1.2;color:#ffe66b}.foot-sub{font-size:24px;line-height:1.35;color:#c5c7cc;letter-spacing:.5px}
.meter{position:absolute;left:80px;right:140px;top:1755px;height:3px;background:#303238;z-index:3}.meter-fill{height:100%;width:100%;background:#ffe66b;transform-origin:left}
</style></head><body><div id="main" data-composition-id="main" data-start="0" data-duration="19.1" data-width="1080" data-height="1920" data-fps="30">
<div id="footage" data-layout-ignore><video id="video" class="clip" data-start="0" data-duration="19.1" data-track-index="0" src="graded.mp4" muted playsinline></video></div>
<audio id="audio" data-start="0" data-duration="19.1" data-track-index="1" src="mix.wav" data-volume="1"></audio>
<div class="matte top-matte" data-layout-ignore></div><div class="matte bottom-matte" data-layout-ignore></div>
'''+''.join(parts)+'''<div class="meter" data-layout-ignore><div class="meter-fill"></div></div></div><script>
const tl=gsap.timeline({paused:true});window.__timelines=window.__timelines||{};
tl.fromTo('.meter-fill',{scaleX:0},{scaleX:1,duration:19.1,ease:'none'},0);
tl.to('#footage',{scale:1.035,duration:3.6,ease:'sine.inOut'},.2);
tl.to('#footage',{scale:1.008,x:0,duration:.7,ease:'power2.inOut'},4.5);
tl.to('#footage',{scale:1.035,x:-10,duration:3.0,ease:'sine.inOut'},6.0);
tl.to('#footage',{scale:1.015,x:0,duration:.6,ease:'power2.inOut'},10.9);
tl.to('#footage',{scale:1.045,x:-6,duration:2.1,ease:'sine.inOut'},13.85);
tl.to('#footage',{scale:1.015,x:0,duration:.6,ease:'power2.inOut'},16.0);
'''
for id,cl,a,b in timings:
 if cl=='headline':
  html+=f"tl.from('#{id} .eyebrow',{{y:18,opacity:0,duration:.22,ease:'power3.out'}},{a});tl.from('#{id} .main-title',{{scale:.92,y:18,opacity:0,duration:.28,ease:'back.out(1.3)'}},{a+.08});tl.from('#{id} .underline',{{scaleX:0,duration:.3,ease:'sine.out'}},{a+.16});\n"
 elif cl=='caption':
  html+=f"tl.from('#{id} .caption-inner',{{y:14,opacity:0,duration:.14,ease:'power2.out'}},{a});\n"
 else:
  html+=f"tl.from('#{id} svg',{{scale:.75,rotation:-5,opacity:0,duration:.3,ease:'back.out(1.4)'}},{a});tl.from('#{id} .foot-copy',{{x:22,opacity:0,duration:.25,ease:'power3.out'}},{a+.06});\n"
 html+=f"tl.set('#{id}',{{opacity:0}},{b});\n"
html+="window.__timelines['main']=tl;</script></body></html>"
(p/'index.html').write_text(html)
(p/'captions.json').write_text(json.dumps([{'start':a,'end':b,'text':(l1+' '+l2).strip()} for a,b,l1,l2 in caps],ensure_ascii=False,indent=2))
(p/'timing.json').write_text(json.dumps({'captions':caps,'headlines':heads,'footers':foots},ensure_ascii=False,indent=2))
print('Composition authored:',len(caps),'caption groups')
