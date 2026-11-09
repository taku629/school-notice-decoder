# School Notice Decoder

**Turn a school notice into reviewed, evidence-linked next steps.**

A student hackathon prototype for multilingual families: image → browser OCR → editable text → local masking → a source-linked action plan → user-confirmed calendar download.

**Live app:** https://taku629.github.io/school-notice-decoder/  
**Source:** https://github.com/taku629/school-notice-decoder
**Demo:** [58-second English narration + captioned screencast](https://taku629.github.io/school-notice-decoder/demo/school-notice-decoder-demo.mp4)  
**Checks:** [Automated workflow test results](demo/test-results.json)

## Try it

1. Open the live app and choose **Try the synthetic sample**.
2. Click **Read text in browser**. This runs real Tesseract.js OCR on the bundled fictional notice image.
3. Correct OCR text and review the masked outgoing preview. The fictional student's name is masked locally.
4. Choose Spanish, English or Japanese and create an action plan. The no-key sample uses a clearly labeled, reviewed translation fixture, not an LLM call.
5. Open **See original words** on any action. Check or edit calendar dates, confirm them and download the `.ics` file. Importing it into a calendar is a separate user action.

## What works

- Browser image OCR with Tesseract.js (English, Japanese and Spanish language selections).
- Editable OCR text, local masking of `Student:`/`Child:`/`Pupil:` lines, user-supplied names/phrases, common emails and phone patterns.
- Exact outgoing-text preview before optional external analysis.
- Clearly labeled, no-key synthetic-sample translations in English, Spanish and Japanese.
- A basic local fallback that extracts common English action-word sentences without translation or date inference.
- Optional real on-device English → Spanish neural translation with Transformers.js and the OPUS-MT model. It translates synthetic English text without an API key or sending notice text to a translation server; local rules extract actions. Calendar extraction outside the included sample is not supported by these local rules.
- Optional experimental Gemini 2.5 Flash-Lite translation/extraction using a user-provided key. No shared or embedded API key.
- Exact-source evidence checks on AI outputs. Unverified event evidence and invalid dates are excluded.
- Editable, confirmed all-day `.ics` reminders. No missing year or timezone is guessed; calendar text is escaped and RFC-style folded.
- Responsive layout, keyboard controls, status announcements and reduced-motion support.

## Honest limitations

This is a prototype, not a validated school communication service. OCR, translation, masking and extraction can be wrong. Masking is incomplete and is not a guarantee of anonymization. The local demo's translations are reviewed fixtures for the included notice; it does not translate arbitrary text. The generic local fallback does not infer dates. The optional Gemini connector requires a compatible, restricted user key and available quota; its live API response has not been verified with a production credential. No user study, measured accuracy or demonstrated real-world impact is claimed.

Only synthetic, non-sensitive notices should be used. **Do not send real school notices, personal information or confidential material to Gemini.** Check every action with the original notice and, when necessary, with the school.

## Privacy and costs

- No app server, database, analytics or notice history. The app does not save text or keys to cookies, local storage or session storage.
- Image recognition and optional English → Spanish translation occur in the browser, but scripts, workers and model files load from third-party CDNs and Hugging Face. Google Fonts also loads remotely. This is **not a fully offline app**; network providers receive normal network metadata. Large translation-model files may be browser-cached, but notice text and API keys are not saved by the app.
- The local sample sends no notice text to an AI. The optional Gemini route sends only the reviewed masked text to Google. Free-tier inputs and outputs can be used to improve Google's products and may be subject to human review.
- A browser-entered key remains accessible to the browser environment. Do not deploy a shared key. Use a dedicated restricted key for experiments only; a production service needs a secure backend and stronger privacy safeguards.
- Default demo and GitHub Pages hosting have $0 cash cost. This project does not enable billing, buy services or use a paid API. The app cannot verify a user's API billing tier: never enter a paid key. Free-tier availability and quotas can change.

## Run locally

No build step or package installation is required for the app:

```sh
cd school-notice-decoder
python3 -m http.server 8080
```

Visit http://localhost:8080. Network access is needed for OCR software/model downloads. Basic text review and the local fixture engine do not require an API key.

## Stack and credits

- HTML, CSS and vanilla JavaScript; deployed on GitHub Pages.
- [Tesseract.js](https://github.com/naptha/tesseract.js) v5.1.1, Apache-2.0, with Tesseract OCR language data. Loaded via [jsDelivr](https://www.jsdelivr.com/).
- [Transformers.js](https://github.com/huggingface/transformers.js) v2.17.2, Apache-2.0, and [Xenova/opus-mt-en-es](https://huggingface.co/Xenova/opus-mt-en-es), ONNX conversion of the Apache-2.0 [Helsinki-NLP OPUS-MT English → Spanish model](https://huggingface.co/Helsinki-NLP/opus-mt-en-es). Model files load from Hugging Face on demand.
- Optional [Gemini API](https://aistudio.google.com/docs) using `gemini-2.5-flash-lite`; [pricing/data-use information](https://aistudio.google.com/docs/pricing) and [key security guidance](https://aistudio.google.com/docs/api-key).
- DM Sans and Manrope from Google Fonts (SIL Open Font License).
- All notice content, school and student identities in the bundled example are fictional; no external notice dataset was used.
- AI assistance was used for planning, coding, review and submission drafting. The demo narration is AI-generated English speech. The no-key in-app demo is deterministic; it is not presented as a live AI output.

## Design goal

The differentiator is a **traceable action layer**, not a claim to replace a translator: parents can inspect the exact words behind a task, correct the text and dates, and decide what to share or export.

Built by Takumu Hata for the Hackathon pathway of STEMergent Hacks 2026. Final competition submission is subject to owner review and approval.
