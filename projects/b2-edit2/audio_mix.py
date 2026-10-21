from pathlib import Path
import json,wave,subprocess,re
import numpy as np
P=Path(__file__).resolve().parent;R=48000;D=45.5;N=round(D*R)
with wave.open(str(P/'source-stereo.wav')) as w:
 assert w.getframerate()==R and w.getnchannels()==2
 voice=np.frombuffer(w.readframes(w.getnframes()),np.int16).reshape(-1,2).astype(float)/32768
voice=voice[:N];N=len(voice);times=np.arange(N)/R
music=np.zeros(N);fx=np.zeros(N);rng=np.random.default_rng(211027)
def pluck(at,hz,amp,dur=.65):
 i=round(at*R);m=min(round(dur*R),N-i)
 if m<=0:return
 t=np.arange(m)/R;env=(1-np.exp(-t*120))*np.exp(-t*5)*np.minimum(1,(dur-t)/.035)
 music[i:i+m]+=amp*(np.sin(2*np.pi*hz*t)+.18*np.sin(2*np.pi*2*hz*t)+.06*np.sin(2*np.pi*3*hz*t))*env
beat=60/88
melody=[261.626,329.628,391.995,493.883,261.626,349.228,440,391.995]
for k,at in enumerate(np.arange(.14,D,beat)):
 pluck(at,melody[k%8],.009,.7)
 if k%4==0:pluck(at,130.813,.009,1.2)
# Gentle, widely spaced pulses under the dialogue.
for at in np.arange(.14,D,beat*2):
 i=round(at*R);m=min(round(.16*R),N-i);t=np.arange(m)/R
 music[i:i+m]+=.004*np.sin(2*np.pi*(60*t+1.5*(1-np.exp(-t*18))))*np.exp(-t*28)
music*=np.minimum(1,times/.8)*np.minimum(1,(D-times)/.8)
plan=json.loads((P/'edit-plan.json').read_text());events=[]
for at,scale,dur in plan['zoom_tweens']:
 if scale<1.08:continue
 i=round(at*R);length=.18;m=min(round(length*R),N-i);t=np.arange(m)/R
 noise=rng.normal(0,1,m);noise=np.convolve(noise,np.ones(12)/12,mode='same')
 fx[i:i+m]+=.030*noise*np.sin(np.pi*t/length)**2
 events.append({'time':at,'type':'soft-whoosh','scale':scale})
for at in [.20,18.98,30.77,38.18]:
 i=round(at*R);m=min(round(.20*R),N-i);t=np.arange(m)/R
 fx[i:i+m]+=.016*(np.sin(2*np.pi*880*t)+.16*np.sin(2*np.pi*1320*t))*np.exp(-t*24)*np.minimum(1,t/.006)
 events.append({'time':at,'type':'soft-pop'})
# Source contains no detected censor terms, so no intervals are muted.
mix=voice+(music+fx)[:,None];peak=float(abs(mix).max());mix*=min(1,.90/(peak+1e-12))
def save(name,x):
 if x.ndim==1:x=np.column_stack([x,x])
 with wave.open(str(P/name),'wb') as w:w.setnchannels(2);w.setsampwidth(2);w.setframerate(R);w.writeframes((np.clip(x,-1,1)*32767).astype(np.int16).tobytes())
save('mix-premaster.wav',mix);save('music-original.wav',music);save('sfx-original.wav',fx)
cmd=['ffmpeg','-hide_banner','-nostats','-y','-i',str(P/'mix-premaster.wav'),'-af','loudnorm=I=-16:TP=-1.5:LRA=9:print_format=json','-ar','48000','-c:a','pcm_s16le',str(P/'mix.wav')]
r=subprocess.run(cmd,capture_output=True,text=True,check=True);z=re.findall(r'\{[^{}]*"input_i"[^{}]*\}',r.stderr,re.S);norm=json.loads(z[-1])
with wave.open(str(P/'mix.wav')) as w:master=np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(float)/32768
out={'duration':D,'sample_rate':R,'voice_rms':float(np.sqrt(np.mean(voice**2))),'music_rms':float(np.sqrt(np.mean(music**2))),'fx_peak':float(abs(fx).max()),'master_peak_dbfs':float(20*np.log10(abs(master).max()+1e-12)),'loudnorm':norm,'music':'Original synthesized soft pluck/bass bed, 88 BPM; not copied from reference','sfx':events,'censor_intervals':[],'censor_note':plan['censor_note'],'review_limit':'Signal, transcript and timing checks performed; direct auditory review not available in this session.'}
(P/'audio-audit.json').write_text(json.dumps(out,ensure_ascii=False,indent=2));print(json.dumps(out,ensure_ascii=False))
