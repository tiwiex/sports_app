# Story review in Sports Development Tools

Open Sports → Development Tools → User Stories as a System Manager or Sports Academy Administrator. Other roles retain their existing restrictions.

- Change **Status** or **MoSCoW** in a story row: each selection saves automatically. There is no Save button. MoSCoW choices are Must, Should, Could and Won’t. A previously unclassified/custom priority remains visible until explicitly replaced.
- **Open** the story to read its acceptance and evidence. The same autosaving controls appear at the top, with an optional review note (enter it before selecting a change). **Mark Done** saves Done directly; it becomes Already Done after success. This is your review decision, not automatic implementation or test verification.
- Existing qualified status text is preserved when changing only priority. Withdrawn stories remain visible and can be explicitly reclassified; review their withdrawal evidence first.
- Each actual edit updates the Markdown story and applicable epic/master inventory rows, refreshes the delivery-state snapshot and adds a dated indexed review build log with reviewer, time, before/after and note. Unchanged saves create no duplicate audit.
- If another reviewer or repository edit changes the story, reopen it to load the latest version before retrying. Failed autosaves restore the last confirmed selection and do not display success; handled write failures restore the affected files.

Changes write to the Sports App checkout and remain Git changes for normal review/commit. They do not implement features, deploy code, change accounting or grant roles. Other documents and story narrative remain read-only in the console. Runtime writes require a writable Sports documentation directory; a read-only deployment must use repository edits instead. File updates are serialized with a local worker lock; process/power-loss recovery across multiple files remains an operational backup/reconciliation responsibility.

## Colours and layout

The story table follows Boost’s separate Story, Epic, Title, Origin, Status, MoSCoW and Action columns. Status colours tint the entire row: green Done, amber In progress, blue In review, teal Ready, red Blocked/Backlog, orange Proposed/Deferred, yellow Analysis/Retrospective, violet UAT and slate Withdrawn/unclassified. Labels remain visible so colour is not the only cue.

MoSCoW is independent of status: Must red, Should amber, Could blue and Won’t slate. The coloured priority dropdown saves immediately when changed; the column heading identifies MoSCoW without a repeated label or badge above each dropdown. An unclassified/custom priority retains its text and a neutral badge until changed.

The reader separates review controls from document content. Headings, paragraphs, lists and tables have clear spacing. On phones, controls stack; the story table scrolls horizontally rather than squeezing columns. Text and explicit statuses remain the source of truth.

Status also uses only its dropdown and table heading, without repeated text above it. Accessible names are retained for both selectors. In each row, **Open** and **Mark Done** sit side by side; error/save feedback appears beneath the actions. Autosave and the reader’s Mark Done action remain available.

The document/story table scroll viewport can extend to 110% of the browser height (previously 70%), beyond the navigation area. Short lists keep their natural height; long lists scroll internally with sticky column headers and horizontal scrolling retained.

Dropdown stability: autosaves update metadata and row colours in place without replacing the table or reader. Selectors stay available while a save runs; consecutive edits queue against the confirmed revision. Opening another dropdown is not interrupted by the prior response. Mark Done is temporarily disabled during a save; failed writes still restore confirmed values and show guidance.
