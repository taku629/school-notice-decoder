# Devpost entry — owner review required

**Status:** Prepared only. The final project submission has not been sent. This file is the exact proposed entry; update the owner-approved version if any field changes.

## Project title
School Notice Decoder

## Elevator pitch
Turn a school notice into reviewed, evidence-linked next steps for multilingual families.

## Pathway
Hackathon

## Team
Takumu Hata — solo participant (GitHub: taku629)

## Project story

### Inspiration
A school notice is not just a paragraph to translate. It can contain a permission-slip deadline, a packing list and an event date—all of which a parent needs to act on. For multilingual families, an unfamiliar language or a photo-only message can add another layer of uncertainty. The goal is to turn “What does this say?” into “What should I do next?”

### What it does
School Notice Decoder is a static web prototype that reads a notice image with browser-based OCR and lets the parent correct the text. It provides a visible local masking step and an exact preview of the text that an optional AI connector would receive.

The resulting plan pairs each proposed action with original source words. A parent can check off tasks, review or edit explicit calendar dates, and confirm them before downloading an all-day `.ics` reminder file. The app does not add events to a calendar automatically or guess an unknown timezone.

The included fictional field-day notice demonstrates a signed permission-slip deadline, supplies to bring, and an event date. Its no-key Spanish, English and Japanese outputs are clearly labeled reviewed sample fixtures—not live LLM responses. A basic local rules fallback finds common English action sentences without translating arbitrary notices or inventing dates. An optional experimental Gemini connector supports translation and extraction with a user-provided key.

For arbitrary synthetic English text, an additional on-device neural model can produce Spanish translation without an API key or sending notice text to a translation server. Local rules extract actions; local calendar extraction beyond the bundled sample is not supported. The first model download takes time and memory, and translations still require review.

### How it was built
The project uses HTML, CSS and vanilla JavaScript, Tesseract.js for browser OCR, Transformers.js with the OPUS-MT English-to-Spanish model for optional local translation, and GitHub Pages for hosting. Local code masks labeled student-name lines, user-specified phrases and common contact patterns. AI output is treated as untrusted: source evidence is checked, invalid or unsupported dates are omitted, and calendar export requires human confirmation. The default demo has no API key or cash cost.

### Challenges and design choices
A confident-looking summary can still be wrong. OCR can damage dates, masking can miss identities, and a calendar entry can imply more certainty than the notice supports. The response was to make evidence and uncertainty visible, keep dates editable, and require an intentional export. The distinctive feature is the traceable action layer—not a claim that an AI can replace a school or a translator.

### What’s next
Next steps are to test comprehension and task completion with multilingual parents and school staff, strengthen redaction and date handling, and evaluate translations before any real-world deployment. A production AI service would need a secure backend and stronger privacy controls.

This is a prototype. We do not claim measured accuracy, user-tested impact or complete anonymization. Only synthetic, non-sensitive content should be used; real school notices and personal or confidential data must not be sent to Gemini. OCR scripts and language data load remotely, so the app is not fully offline. Optional Gemini free-tier content may be used for product improvement and human review.

## Built with
HTML, CSS, JavaScript, Tesseract.js, Transformers.js, OPUS-MT, Gemini API (optional), GitHub Pages

## Links
- Live application: https://taku629.github.io/school-notice-decoder/
- Public source: https://github.com/taku629/school-notice-decoder
- English TTS + captioned demo: https://taku629.github.io/school-notice-decoder/demo/school-notice-decoder-demo.mp4

## Visuals
- Homepage screenshot: https://taku629.github.io/school-notice-decoder/demo/homepage.png
- Demo uses the bundled fictional Pine Ridge Elementary notice and fictional student Mia Rivera. No real notice, school or student data is used.

## AI and third-party disclosure
AI assistance was used for planning, coding, critical review and drafting. Demo narration is AI-generated English speech; it is not the participant’s voice. Tesseract.js performs image OCR in the browser while downloading scripts and language data from third-party CDNs. The default no-key sample plan uses deterministic rules and reviewed translation fixtures. Optional on-device translation uses Transformers.js and Xenova’s ONNX conversion of Helsinki-NLP’s OPUS-MT English-to-Spanish model, downloaded from Hugging Face. The optional Gemini API connector requires the user’s own restricted key; the app does not embed or save a key. Google Fonts supplies DM Sans and Manrope. All fictional sample content was created for this project; no external school-notice dataset was used.

## Verification note for owner review (not part of the project story)
The optional Gemini request path is tested with a mocked response, not a live production credential. Actual browser OCR and the on-device neural translation model are tested with synthetic content. The default sample workflow, masking, source checks and calendar export are tested without sending notice text to an external AI. Review the entry and video before authorizing final Devpost submission.
