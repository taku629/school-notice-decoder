from pathlib import Path
from playwright.sync_api import sync_playwright
import json,time
ROOT=Path(__file__).resolve().parents[1]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 page=b.new_page(ignore_https_errors=True);page.set_default_timeout(300000)
 page.on('console',lambda m:print(m.text[:250],flush=True) if 'MODEL' in m.text else None)
 page.goto('http://127.0.0.1:8080',wait_until='domcontentloaded')
 start=time.monotonic()
 try:
  result=page.evaluate('''async()=>{const {pipeline,env}=await import('https://cdn.jsdelivr.net/npm/@xenova/transformers@2.17.2/dist/transformers.min.js');env.allowLocalModels=false;env.backends.onnx.wasm.numThreads=1;const translator=await pipeline('translation','Xenova/opus-mt-en-es',{quantized:true,progress_callback:p=>{if(p.status==='done'||p.status==='ready')console.log('MODEL '+p.status+' '+(p.file||''));}});return await translator('Please return the signed permission slip by February 9, 2027.',{max_new_tokens:128});}''')
  output={'success':True,'seconds':time.monotonic()-start,'result':result}
 except Exception as e: output={'success':False,'seconds':time.monotonic()-start,'error':str(e)}
 print(json.dumps(output),flush=True);(ROOT/'demo/translation-model-test.json').write_text(json.dumps(output,indent=2)+'\n');b.close()
