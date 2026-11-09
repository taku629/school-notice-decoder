from pathlib import Path
from playwright.sync_api import sync_playwright
import time, shutil, sys
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'demo'; RAW=OUT/'raw';RAW.mkdir(exist_ok=True)
base=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8080'
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 c=b.new_context(viewport={'width':1440,'height':1050},record_video_dir=str(RAW),record_video_size={'width':1440,'height':1050},ignore_https_errors=True,accept_downloads=True)
 warm=c.new_page();warm.goto(base,wait_until='networkidle');warm.locator('#heroSample').click();warm.locator('#ocrButton').click();warm.wait_for_function("document.querySelector('#noticeText').value.length>50",timeout=90000);warm.close()
 page=c.new_page();page.goto(base,wait_until='networkidle');start=time.monotonic()
 def at(seconds):
  time.sleep(max(0,seconds-(time.monotonic()-start)))
 at(8.8);page.locator('#heroSample').click()
 at(10.2);page.locator('#ocrButton').click();page.wait_for_function("document.querySelector('#noticeText').value.length>50",timeout=90000)
 at(16.5);page.locator('#namesInput').focus()
 at(21.0);page.locator('#outgoingPreview').scroll_into_view_if_needed()
 at(24.0);page.locator('#analyzeButton').click();page.locator('#results').wait_for(state='visible')
 at(29.6);page.locator('#action-0').check()
 at(33.3);page.locator('.evidence summary').first.click()
 at(35.7);page.locator('#dateList').scroll_into_view_if_needed()
 at(38.3);page.locator('#dateConfirm').check()
 at(40.3)
 with page.expect_download() as d:page.locator('#calendarButton').click()
 d.value.save_as(str(OUT/'demo-reminders.ics'))
 at(43.2);page.locator('#engine').select_option('gemini');page.locator('#aiSettings').scroll_into_view_if_needed()
 at(51.0);page.evaluate('window.scrollTo({top:0,behavior:"smooth"})')
 at(59.0);video=page.video;page.close();path=video.path();shutil.copyfile(path,OUT/'raw-screen.webm');c.close();b.close()
for f in RAW.glob('*.webm'):f.unlink()
RAW.rmdir()
print('Saved real interaction screen recording:',OUT/'raw-screen.webm',flush=True)
