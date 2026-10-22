from pathlib import Path
import json,html
from PIL import ImageFont
P=Path(__file__).resolve().parent;D=28
SCENES=[
{'at':0,'end':4.35,'label':'TRƯỚC KHI QUYẾT ĐỊNH','title':'KÝ HỢP ĐỒNG?','body':'Đừng chỉ nhìn vào số tiền được nhận.','detail':'Có 3 điều cần kiểm tra trước.','num':'','icon':'document'},
{'at':4,'end':10.35,'label':'01 / CHI PHÍ','title':'TỔNG TIỀN PHẢI TRẢ','body':'Đọc lãi suất, các khoản phí và lịch thanh toán.','detail':'Xem cả điều kiện trả chậm và trả trước hạn.','num':'01','icon':'cost'},
{'at':10,'end':17.35,'label':'02 / ĐƠN VỊ CUNG CẤP','title':'XÁC MINH THÔNG TIN','body':'Tên pháp nhân, thông tin liên hệ và giấy phép phù hợp.','detail':'Đọc hợp đồng trước khi đồng ý.','num':'02','icon':'check'},
{'at':17,'end':24.35,'label':'03 / THÔNG TIN CÁ NHÂN','title':'GIỮ AN TOÀN GIẤY TỜ','body':'Chỉ gửi qua kênh đã xác minh.','detail':'Không đăng công khai ảnh căn cước hoặc mã OTP.','num':'03','icon':'shield'},
{'at':24,'end':28,'label':'TRƯỚC KHI KÝ','title':'ĐỌC KỸ. HỎI RÕ.','body':'Lưu 3 điều này để đối chiếu.','detail':'Thông tin chung, không phải lời mời đăng ký dịch vụ.','num':'','icon':'bookmark'}
]
ICONS={
'document':'<path d="M75 38h107l43 45v198H75zM182 38v47h43M106 135h89M106 170h89M106 205h60"/><path class="accent" d="M215 194l20 20 40-48"/>',
'cost':'<rect x="63" y="42" width="173" height="232" rx="18"/><path d="M91 84h117M93 132h17M144 132h17M195 132h17M93 175h17M144 175h17M195 175h17M93 220h17M144 220h17"/>',
'check':'<path d="M150 29l105 40v84c0 70-105 128-105 128S45 223 45 153V69z"/><path class="accent" d="M95 151l36 35 76-81"/>',
'shield':'<path d="M150 29l105 40v84c0 70-105 128-105 128S45 223 45 153V69z"/><rect class="accent" x="105" y="129" width="90" height="70" rx="9"/><path d="M120 126v-20a30 30 0 0160 0v20M150 153v24"/>',
'bookmark':'<path d="M79 36h142v246l-71-44-71 44z"/><path class="accent" d="M113 135l25 25 52-61"/>'}
font=P/'BeVietnamPro-ExtraBold.ttf'
def fit(t,size,width):
 while ImageFont.truetype(str(font),size).getlength(t)>width and size>60:size-=1
 return size
clips=[];js=["const tl=gsap.timeline({paused:true});window.__timelines=window.__timelines||{};"]
for i,s in enumerate(SCENES):
 title_size=fit(s['title'],78,580)
 # Wrap titles naturally into at most 2 lines with roomy static layout.
 body=f'''<div class="scene-content"><div class="eyebrow">{html.escape(s['label'])}</div><svg class="illustration" viewBox="0 0 300 310" aria-hidden="true">{ICONS[s['icon']]}</svg><h1 style="font-size:{title_size}px">{html.escape(s['title'])}</h1><div class="rule"></div><p class="body">{html.escape(s['body'])}</p><p class="detail">{html.escape(s['detail'])}</p><div class="step-dots" aria-hidden="true">{''.join('<i class="'+('active' if j==i else '')+'"></i>' for j in range(5))}</div></div>'''
 clips.append(f'<div id="scene{i}" class="clip scene" data-start="{s["at"]}" data-duration="{s["end"]-s["at"]:.3f}" data-track-index="{1+i%2}" style="z-index:{i+1}">{body}</div>')
 a=s['at'];shift=.18 if i==0 else .38
 if i:js.append(f"tl.from('#scene{i}',{{opacity:0,duration:.35,ease:'sine.inOut'}},{a});")
 js.extend([
 f"tl.from('#scene{i} .eyebrow',{{y:12,opacity:0,duration:.28,ease:'power3.out'}},{a+shift});",
 f"tl.from('#scene{i} .illustration',{{y:16,scale:.94,opacity:0,duration:.45,ease:'sine.out'}},{a+shift+.04});",
 f"tl.from('#scene{i} h1',{{y:20,opacity:0,duration:.35,ease:'power3.out'}},{a+shift+.08});",
 f"tl.from('#scene{i} .rule',{{scaleX:0,duration:.4,ease:'expo.out'}},{a+shift+.17});",
 f"tl.from('#scene{i} .body',{{y:14,opacity:0,duration:.3,ease:'sine.out'}},{a+shift+.23});",
 f"tl.from('#scene{i} .detail',{{y:10,opacity:0,duration:.3,ease:'power2.out'}},{a+shift+.30});",
 f"tl.from('#scene{i} .step-dots',{{opacity:0,duration:.25,ease:'power1.out'}},{a+shift+.36});"
 ])
js.append("window.__timelines['main']=tl;")
css='''@font-face{font-family:BeVietnam;src:url('BeVietnamPro-ExtraBold.ttf');font-weight:800}*{box-sizing:border-box;margin:0}html,body,#main{width:720px;height:1280px;overflow:hidden;background:#102a2d;color:#fff;font-family:BeVietnam,sans-serif}#main{position:relative}.scene{position:absolute;inset:0;width:720px;height:1280px;background:#102a2d}.scene-content{width:100%;height:100%;padding:95px 70px 160px 60px;display:flex;flex-direction:column;align-items:flex-start;justify-content:center;gap:25px}.eyebrow{font-size:23px;line-height:1.3;letter-spacing:1.3px;color:#85e9de}.illustration{width:205px;height:212px;fill:none;stroke:#d2e2df;stroke-width:6;stroke-linecap:round;stroke-linejoin:round;margin-left:-14px;margin-bottom:8px}.illustration .accent{stroke:#85e9de;stroke-width:9}h1{max-width:580px;line-height:1.13;letter-spacing:-1.8px;font-weight:800;text-wrap:balance;text-shadow:0 3px 1px rgba(0,0,0,.15)}.rule{width:125px;height:5px;background:#85e9de;transform-origin:0 50%;border-radius:4px}.body{max-width:580px;font-size:37px;line-height:1.4;color:#fff}.detail{max-width:580px;font-size:29px;line-height:1.4;color:#d2e2df}.step-dots{display:flex;gap:10px;margin-top:14px}.step-dots i{width:9px;height:9px;border-radius:50%;background:#537676}.step-dots i.active{width:33px;border-radius:7px;background:#85e9de}
'''
(P/'index.html').write_text(f'''<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=720,height=1280"><script src="gsap.min.js"></script><style>{css}</style></head><body><div id="main" data-composition-id="main" data-start="0" data-duration="{D}" data-width="720" data-height="1280" data-fps="30">{''.join(clips)}<audio id="music" src="music.wav" data-start="0" data-duration="{D}" data-track-index="4" data-volume="1"></audio></div><script>{''.join(js)}</script></body></html>''')
(P/'edit-plan.json').write_text(json.dumps({'duration':D,'format':'educational replacement, text and original instrumental music; no original speech or presenter footage','scenes':SCENES,'zoom_tweens':[],'removed':['credit solicitation','18-year-old borrowing hook','ID-only / no-income-verification claims','15–50 million promotional range','contact/application CTA'],'limits':'Exact TikTok notice and placement type not yet supplied. No guarantee of moderation approval.'},ensure_ascii=False,indent=2))
print('Built 28-second educational alternative; 5 scenes; no footage or voice substitution.')
