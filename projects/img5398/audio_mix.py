from pathlib import Path
import wave,json,subprocess,re
import numpy as np
P=Path(__file__).resolve().parent;R=48000;D=50.3;N=int(R*D)
w=wave.open(str(P/'source-stereo.wav'));src=np.frombuffer(w.readframes(w.getnframes()),np.int16).reshape(-1,2).astype(float)/32768
src=src[:N];N=len(src);t=np.arange(N)/R
voice_rms=float(np.sqrt(np.mean(src**2)));gain=min(1.6,.105/(voice_rms+1e-9));voice=src*gain
music=np.zeros(N);fx=np.zeros(N)
def note(at,hz,amp,dur=.5):
 i=int(at*R);m=min(int(dur*R),N-i)
 if m<=0:return
 tt=np.arange(m)/R;env=(1-np.exp(-tt*85))*np.exp(-tt*6)*np.minimum(1,(dur-tt)/.03)
 music[i:i+m]+=amp*(np.sin(2*np.pi*hz*tt)+.18*np.sin(2*np.pi*2*hz*tt))*env
notes=[261.626,311.127,391.995,466.164,261.626,349.228,391.995,311.127]
for q,at in enumerate(np.arange(.12,D,.3)):note(at,notes[q%8],.011)
for at in np.arange(.12,D,1.2):note(at,130.813,.012,.75)
music*=np.minimum(1,t/.65)*np.minimum(1,(D-t)/.65)
plan=json.loads((P/'edit-plan.json').read_text());rng=np.random.default_rng(5398)
events=[]
for at,scale,dur in plan['zoom_tweens']:
 if scale<1.08:continue
 i=int(at*R);m=min(int(.19*R),N-i);tt=np.arange(m)/R
 noise=rng.normal(0,1,m);noise=np.convolve(noise,np.ones(10)/10,mode='same')
 fx[i:i+m]+=.032*noise*np.sin(np.pi*tt/.19)**2
 events.append({'time':at,'type':'zoom-whoosh','scale':scale})
for at in [.2,14.16,26.66,35.46,40.18]:
 i=int(at*R);m=min(int(.28*R),N-i);tt=np.arange(m)/R
 fx[i:i+m]+=.025*(np.sin(2*np.pi*1046.5*tt)+.25*np.sin(2*np.pi*1567.98*tt))*np.exp(-tt*17)*np.minimum(1,tt/.006)
 events.append({'time':at,'type':'keyword-chime'})
mix=voice+(music+fx)[:,None];peak=float(abs(mix).max());normal=min(1,.86/(peak+1e-9));mix*=normal
def save(name,x):
 if x.ndim==1:x=np.stack([x,x],axis=1)
 with wave.open(str(P/name),'wb') as f:f.setnchannels(2);f.setsampwidth(2);f.setframerate(R);f.writeframes((np.clip(x,-1,1)*32767).astype(np.int16).tobytes())
save('mix.wav',mix);save('music-original.wav',music);save('sfx-original.wav',fx)
# Master the mix after synthesis: keep dialogue audible, preserve a -1.5 dBTP ceiling.
tmp=P/'mix-master.wav'
proc=subprocess.run(['ffmpeg','-nostdin','-y','-hide_banner','-nostats','-i',str(P/'mix.wav'),'-af','loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json','-ar','48000','-c:a','pcm_s16le',str(tmp)],capture_output=True,text=True,check=True)
matches=re.findall(r'\{[^{}]*"input_i"[^{}]*\}',proc.stderr,re.S)
loudness=json.loads(matches[-1]) if matches else {}
tmp.replace(P/'mix.wav')
with wave.open(str(P/'mix.wav')) as f:master=np.frombuffer(f.readframes(f.getnframes()),np.int16).astype(float)/32768
audit={'duration':D,'source_voice_rms':voice_rms,'voice_gain':gain,'premaster_peak':float(abs(mix).max()),'mix_peak':float(abs(master).max()),'loudness_normalization':loudness,'music_rms':float(np.sqrt(np.mean(music**2))),'music':'Original synthesized instrumental, 100 BPM','sfx_events':events,'censor_intervals':plan['censor_intervals'],'review_note':plan['censor_note']}
(P/'audio-audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2));print(json.dumps({k:v for k,v in audit.items() if k not in ['sfx_events','review_note']},ensure_ascii=False))
