from pathlib import Path
import re, subprocess, json
ROOT=Path(__file__).resolve().parents[1];D=ROOT/'demo'
srt=(D/'English-captions.srt').read_text()
def ass_time(s):
 h,m,rest=s.split(':');sec,ms=rest.split(',');return f'{int(h)}:{m}:{sec}.{int(ms)//10:02d}'
header='''[Script Info]
ScriptType: v4.00+
PlayResX: 1440
PlayResY: 1050
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,DejaVu Sans,28,&H00FFFFFF,&H00FFFFFF,&H90000000,&H90000000,-1,0,0,0,100,100,0,0,3,1,0,2,70,70,28,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''
events=[]
for block in srt.strip().split('\n\n'):
 lines=block.splitlines();start,end=lines[1].split(' --> ');text='\\N'.join(lines[2:]);events.append(f'Dialogue: 0,{ass_time(start)},{ass_time(end)},Default,,0,0,0,,{text}')
(D/'English-captions.ass').write_text(header+'\n'.join(events)+'\n')
def duration(f):return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','json',str(f)]).decode() and json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','json',str(f)]))['format']['duration'])
raw_duration=duration(D/'raw-screen.webm');audio_duration=duration(D/'narration.wav');offset=max(0,raw_duration-59.0)
cmd=['ffmpeg','-y','-ss',str(offset),'-i',str(D/'raw-screen.webm'),'-i',str(D/'narration.wav'),'-map','0:v:0','-map','1:a:0','-vf',f'ass={D}/English-captions.ass','-af','loudnorm=I=-16:TP=-1.5:LRA=11','-t',str(audio_duration),'-r','30','-c:v','libx264','-preset','fast','-crf','22','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-movflags','+faststart',str(D/'school-notice-decoder-demo.mp4')]
subprocess.run(cmd,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
print(json.dumps({'raw_duration':raw_duration,'trimmed_lead':offset,'final_duration':duration(D/'school-notice-decoder-demo.mp4'),'output':str(D/'school-notice-decoder-demo.mp4')},indent=2),flush=True)
