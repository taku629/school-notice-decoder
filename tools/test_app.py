from pathlib import Path
from playwright.sync_api import sync_playwright
import json, sys, datetime
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'demo'; OUT.mkdir(exist_ok=True)
base=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8080'
checks=[]
def check(name,condition):
    if not condition: raise AssertionError(name)
    checks.append(name); print('PASS:',name,flush=True)
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
    context=browser.new_context(viewport={'width':1440,'height':1050},device_scale_factor=1,ignore_https_errors=True,accept_downloads=True)
    asset=context.new_page();asset.goto((ROOT/'assets/synthetic-notice.html').as_uri());asset.locator('.notice').screenshot(path=str(ROOT/'assets/synthetic-notice.png'));asset.close()
    page=context.new_page(); errors=[];page.on('pageerror',lambda e: errors.append(str(e)))
    page.goto(base,wait_until='networkidle');page.screenshot(path=str(OUT/'homepage.png'),full_page=False)
    check('desktop has no horizontal overflow',page.evaluate('document.documentElement.scrollWidth<=innerWidth'))
    page.locator('#heroSample').click();page.locator('#ocrButton').click()
    page.wait_for_function("document.querySelector('#noticeText').value.length>50 || document.querySelector('#ocrStatus').classList.contains('error')",timeout=120000)
    check('browser OCR completes', 'OCR complete' in page.locator('#ocrStatus').inner_text())
    ocr=page.locator('#noticeText').input_value(); (OUT/'ocr-output.txt').write_text(ocr+'\n')
    check('real browser OCR reads sample student', 'Mia Rivera' in ocr)
    masked=page.locator('#outgoingPreview').inner_text()
    check('local outgoing preview masks student name','Mia Rivera' not in masked and '[STUDENT]' in masked)
    page.locator('#analyzeButton').click();page.locator('#results').wait_for(state='visible')
    check('sample engine creates 3 source-linked actions',page.locator('.action-card').count()==3)
    check('sample engine is explicitly labeled','Local sample' in page.locator('#engineBadge').inner_text())
    check('all action evidence matches source',page.locator('.evidence summary').all_text_contents()==['See original words']*3)
    check('two explicit dates survive source validation',page.locator('#dateList input').count()==2)
    check('calendar blocked before date confirmation',page.locator('#calendarButton').is_disabled())
    page.locator('#dateConfirm').check();
    with page.expect_download() as d: page.locator('#calendarButton').click()
    d.value.save_as(str(OUT/'sample-reminders.ics')); ics=(OUT/'sample-reminders.ics').read_text()
    check('ICS contains two all-day events',ics.count('BEGIN:VEVENT')==2 and 'DTSTART;VALUE=DATE:20270209' in ics and 'DTSTART;VALUE=DATE:20270212' in ics)
    check('ICS end dates are exclusive','DTEND;VALUE=DATE:20270210' in ics and 'DTEND;VALUE=DATE:20270213' in ics)
    check('no timezone inferred in calendar','TZID' not in ics)
    page.locator('#date-0').fill('2027-02-10');check('date edits require reconfirmation',not page.locator('#dateConfirm').is_checked() and page.locator('#calendarButton').is_disabled())
    unit=page.evaluate('''() => {
      const r=Decoder.redact('Student: Ada Example\\nEmail: synthetic@example.org\\nPhone: +1 (202) 555-0123','Ada Example');
      const invalid=Decoder.validatePlan({title:'test',translation:'test',actions:[],events:[{title:'invented',date:'2027-02-09',evidence:''},{title:'wrong',date:'2027-02-09',evidence:'No date here'},{title:'invalid',date:'2027-02-30',evidence:'February 30, 2027'}]},'No date here February 30, 2027');
      return {redacted:r.text,valid:Decoder.validDate('2027-02-09'),invalid:Decoder.validDate('2027-02-30'),events:invalid.events.length,storage:localStorage.length+sessionStorage.length};
    }''')
    check('contact patterns masked','Ada Example' not in unit['redacted'] and 'synthetic@example.org' not in unit['redacted'] and '555' not in unit['redacted'])
    check('impossible or ungrounded dates excluded',unit['valid'] and not unit['invalid'] and unit['events']==0)
    check('app does not persist notice/key in web storage',unit['storage']==0)
    page.locator('#engine').select_option('browser');page.locator('#analyzeButton').click()
    page.wait_for_function("document.querySelector('#planTitle').textContent==='Tu plan escolar' && !document.querySelector('#results').hidden",timeout=180000)
    check('real on-device neural Spanish translation works','Browser model' in page.locator('#engineBadge').inner_text() and len(page.locator('#translationText').inner_text())>50)
    check('browser-model actions preserve source evidence',page.locator('.evidence summary').all_text_contents()==['See original words']*3)
    # Exercise optional network path with a stub, not a live credential or billable request.
    payload=[]
    def mock(route):
        payload.append(route.request.post_data_json)
        body={'title':'Mock connector test','translation':'Synthetic connector response.','actions':[{'text':'Return form','category':'RETURN','evidence':'signed permission slip'}],'events':[],'warning':'Mocked integration test; not a live API result.'}
        route.fulfill(status=200,content_type='application/json',body=json.dumps({'candidates':[{'content':{'parts':[{'text':json.dumps(body)}]}}]}))
    page.route('https://generativelanguage.googleapis.com/**',mock)
    page.locator('#engine').select_option('gemini');page.locator('#apiKey').fill('TEST-KEY-NOT-REAL');page.locator('#aiConsent').check();page.locator('#analyzeButton').click();page.wait_for_function("document.querySelector('#planTitle').textContent==='Mock connector test'")
    serialized=json.dumps(payload)
    check('optional connector transmits masked text only',len(payload)==1 and 'Mia Rivera' not in serialized and '[STUDENT]' in serialized)
    page.locator('#namesInput').fill('Mia Rivera, another synthetic name');check('outgoing edits revoke external-send consent',not page.locator('#aiConsent').is_checked())
    page.locator('#apiKey').fill('');page.locator('#engine').select_option('local')
    page.set_viewport_size({'width':390,'height':844});page.goto(base,wait_until='networkidle');
    check('mobile has no horizontal overflow',page.evaluate('document.documentElement.scrollWidth<=innerWidth'))
    page.screenshot(path=str(OUT/'mobile-preview.png'),full_page=False)
    check('no uncaught JavaScript errors',not errors)
    browser.close()
checks.append('sample date weekdays verified: '+datetime.date(2027,2,9).strftime('%A')+' / '+datetime.date(2027,2,12).strftime('%A'))
(OUT/'test-results.json').write_text(json.dumps({'checks':checks,'browserTranslationTested':True,'liveGeminiTested':False,'note':'Gemini connector path tested with a mocked response only; no API key or real notice used.'},indent=2)+'\n')
print(f'{len(checks)} checks completed.')
