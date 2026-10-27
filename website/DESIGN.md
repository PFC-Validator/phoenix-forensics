---
name: "Phoenix Governance Review"
description: "A calm civic reading system for dated public records."
colors:
  paper: "#fff"
  ink: "#203e35"
  muted: "#526459"
  accent: "#28654f"
  tint: "#e9f1ed"
  rule: "#cddbd3"
  surface: "#f5f8f6"
  accent-hover: "#1e4e3d"
  field-border: "#91a59a"
  diagram-border: "#8ba395"
  source-focus: "#d6e9df"
  forest: "#173d32"
  on-forest: "#f1f7f3"
  on-forest-muted: "#c4d9cb"
  mint: "#b8dfbd"
  focal-node: "#d9ecdf"
  forest-edge: "#87aa95"
  focal-muted: "#345b48"
  forest-rule: "#577f68"
  forest-hover: "#2a5443"
  sequence-connector: "#729a83"
typography:
  display:
    fontFamily: "Public Sans, sans-serif"
    fontSize: "clamp(2.7rem, 5.5vw, 5.3rem)"
    fontWeight: 600
    lineHeight: 1.08
    letterSpacing: "-.025em"
  feature-display:
    fontFamily: "Public Sans, sans-serif"
    fontSize: "clamp(2.9rem, 5.3vw, 4.8rem)"
    fontWeight: 600
    lineHeight: 1.08
    letterSpacing: "-.035em"
  figure-identifier:
    fontFamily: "ui-monospace, monospace"
    fontSize: "9px"
    fontWeight: 400
  headline:
    fontFamily: "Public Sans, sans-serif"
    fontSize: "clamp(1.75rem, 3vw, 2.65rem)"
    fontWeight: 600
    lineHeight: 1.15
    letterSpacing: "-.025em"
  page-title:
    fontFamily: "Public Sans, sans-serif"
    fontSize: "clamp(2.4rem, 4.6vw, 4.4rem)"
    fontWeight: 600
    lineHeight: 1.08
    letterSpacing: "-.025em"
  body:
    fontFamily: "Source Sans 3, sans-serif"
    fontSize: "19px"
    fontWeight: 400
    lineHeight: 1.55
  lead:
    fontFamily: "Source Sans 3, sans-serif"
    fontSize: "clamp(1.25rem, 2.1vw, 1.65rem)"
    fontWeight: 400
    lineHeight: 1.4
  finding-title:
    fontFamily: "Public Sans, sans-serif"
    fontSize: "21px"
    fontWeight: 600
    lineHeight: 1.15
    letterSpacing: "-.01em"
  label:
    fontFamily: "Source Sans 3, sans-serif"
    fontSize: "15px"
    fontWeight: 400
    lineHeight: 1.55
rounded:
  control: "3px"
  button: "4px"
  action: "4px"
  note: "6px"
  figure: "8px"
spacing:
  control: "12px"
  compact: "16px"
  group: "24px"
  section-gap: "32px"
  mobile-section: "48px"
  section: "78px"
components:
  button-primary:
    backgroundColor: "{colors.accent}"
    textColor: "{colors.paper}"
    rounded: "{rounded.button}"
    padding: "13px 21px"
  button-primary-hover:
    backgroundColor: "{colors.accent-hover}"
  button-secondary:
    backgroundColor: "transparent"
    textColor: "{colors.accent}"
    rounded: "{rounded.button}"
    padding: "13px 21px"
  field:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink}"
    rounded: "{rounded.control}"
    padding: "12px"
  context-note:
    backgroundColor: "{colors.tint}"
    textColor: "{colors.muted}"
    rounded: "{rounded.note}"
    padding: "24px 28px"
  figure:
    backgroundColor: "{colors.surface}"
    rounded: "{rounded.figure}"
    padding: "20px 28px 22px"
  category-tag:
    backgroundColor: "{colors.tint}"
    textColor: "{colors.ink}"
    rounded: "{rounded.control}"
    padding: "2px 8px"
  case-control:
    backgroundColor: "transparent"
    textColor: "{colors.on-forest-muted}"
    rounded: "{rounded.control}"
    padding: "9px 21px"
  case-control-selected:
    backgroundColor: "{colors.mint}"
    textColor: "{colors.forest}"
  timeline-control:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink}"
    rounded: "{rounded.button}"
    padding: "10px 16px"
  timeline-control-play:
    backgroundColor: "{colors.accent}"
    textColor: "{colors.paper}"
---
# Design System: Phoenix Governance Review

## Overview

**Creative North Star: "Civic evidence review"**

Holder briefing is a calm civic reading system: white ground, deep forest-green text, open document sections and fine rules. Public Sans supplies clear headings; Source Sans 3 carries readable explanations and evidence. Pale green fields distinguish figures and qualifications without turning the document into a grid of cards. The approved visual extension adds a substantial forest-green feature field, contrasting decision nodes and optional timeline emphasis while keeping the reading sections open and spacious.

This system describes the stakeholder-wide governance review and its shared site stylesheet. The process-first homepage, voting analysis, stakeholder map, treasury review, governance reforms and evidence library all use the same calm reading system. The preserved original presentation under `holder-briefing/dist/record/` is a separate archival surface and does not define these tokens. The user explicitly requested stronger visual appeal, beneficiary-approval diagrams and timeline motion after the first build. This document merges that implemented extension with the confirmed base system. No approved image comp exists.

**Key Characteristics:**
- White reading ground and a single green family with a forest feature field.
- Spacious reading columns separated by fine rules.
- Authored geometric figures with readable mobile counterparts.
- Evidence disclosures, visible focus and optional controlled sequence emphasis.

## Colors

A deep green ink and accent sit on intentional pure white; the supporting greens remain quiet, with reversed text and mint emphasis inside the forest feature field. The frontmatter preserves the source CSS values and is the normative color table.

### Primary

- **Forest Action** (`accent`): links, primary actions, focus outlines, selected votes and meaningful diagram connectors.
- **Forest Action Hover** (`accent-hover`): filled primary action hover.

### Secondary

- **Feature Forest** (`forest`): full-width feature field and ordinary relationship nodes.
- **Feature Ink** (`on-forest`): headings and node labels on forest.
- **Feature Supporting Ink** (`on-forest-muted`): explanations, caveats and ordinary node details on forest.
- **Mint Emphasis** (`mint`): selected case controls, feature links, focal outlines and active timeline rings.
- **Focal Node** (`focal-node`): the participating approval node, with forest ink and **Focal Supporting Ink** (`focal-muted`).
- **Forest Edge** (`forest-edge`), **Forest Rule** (`forest-rule`) and **Forest Hover** (`forest-hover`): outlined controls/nodes, feature separators and case-control hover.
- **Sequence Connector** (`sequence-connector`): broken chronological connectors on white.

### Neutral

- **White Ground** (`paper`): page ground, input fields, white diagram nodes and reversed button lettering.
- **Forest Ink** (`ink`): main text, headings, brand and selected navigation rules.
- **Quiet Green** (`muted`): supporting prose, dates, captions and neutral diagram connectors.
- **Pale Green** (`tint`): context notes, tags, funding milestones and highlighted diagram nodes.
- **Field White** (`surface`): figure fields, footer, empty results and vote-panel backgrounds.
- **Fine Rule** (`rule`): section separators, disclosure boundaries and subdued control borders.
- **Field Edge** (`field-border`): input and select borders.
- **Figure Edge** (`diagram-border`): neutral SVG node borders.
- **Source Emphasis** (`source-focus`): temporary targeted-source highlight, not a persistent surface.

The CSS also contains selection and scrollbar colors. They are browser affordances, not a second accent palette. Sidecar tonal strips are synthesized previews, not additional shipped tokens.

## Typography

**Display Font:** Public Sans, with sans-serif fallback.  
**Body Font:** Source Sans 3, with sans-serif fallback.

Both families have self-hosted regular and semibold font files with `font-display: swap`. The briefing loads four local TTFs from `/fonts/`. The visual extension uses the system monospace stack for compact proposal identifiers and timeline dates inside SVG; it does not add a downloaded mono family.

### Hierarchy

- **Display:** the frontmatter display role remains the shared stylesheet default; its line length is limited to 16ch. At widths at or below 1100px it uses `clamp(2.6rem, 5vw, 3.8rem)`; at or below 780px, `clamp(2.5rem, 9vw, 3.5rem)`.
- **Feature display:** the revised opening uses the frontmatter feature-display role. At 1000px and above it uses `clamp(3rem, 4.6vw, 4.1rem)`; at 780px and below, `clamp(2.7rem, 9.2vw, 3.6rem)` with 1.1 line height. Introductory paragraphs are 22px/20px on desktop and 20px/18px on phones.
- **Page title:** inner-page titles use their own frontmatter clamp and 22ch width; they become 2.5rem on phones.
- **Headline:** section headings use the frontmatter headline role with a 23ch limit. Reading-page headings use 30px, becoming 27px on phones.
- **Finding title:** findings use the recorded title role, becoming 20px on phones. General subordinate headings use 1.2rem.
- **Body:** paragraphs have a 69ch maximum, while the reading column is capped at 780px. Phone body size is 18px. Leads are 21px on desktop and 20px on phones. Supporting labels use the smaller label role; compact receipt metadata reaches 14px and tags 13px.
- **Figures:** current relationship node titles are 16px semibold, details 12px and identifiers 9px in the recorded monospace stack. Timeline titles are 16px on wide figures and 12px on vertical figures; dates use the 9px identifier role, details 12px and caveats 11px. Values are native SVG viewBox sizes and scale with the graphic. The legacy Estima export retains its earlier 14px/12px/11px hierarchy; do not use those legacy dimensions as the current figure pattern.

**The Reading Pair Rule.** Use Public Sans for headings and Source Sans 3 for reading text; keep emphasis within the shipped 400 and 600 weights.

## Layout

The main container is centered, capped at 1216px, with a width of `calc(100% - 96px)`. At or below 1100px the total inset becomes 64px; at or below 780px it becomes 40px. The header’s desktop minimum height is 102px. On phones the brand and navigation stack and the final navigation rule wraps links; the earlier scrolling-nav declaration is overridden.

The shared legacy opening uses a 1.1:1 grid with a 76px gap; the medium layout uses equal columns and a 36px gap. The final cascade sets opening vertical padding to 56px / 48px on desktop and 40px / 36px on phones. Analytical sections use a .76:1.24 grid and 90px gap, reduced to 50px at medium width. At 780px they become one column with a 32px gap. Sections use 78px vertical padding, reduced to 48px on phones. These are observed values, not a complete mathematical spacing scale.

Funding tools, milestone blocks, vote panels, timeline entries, continuation links and footer groups stack on phones. Standard paragraphs retain the document’s reading rhythm. Receipt identifiers may wrap anywhere to contain long chain addresses.

The revised opening is a full-width forest field below the unchanged white masthead. Its heading and explanation use a 1.15:1 grid with a 96px gap by default, 50px in the medium rule; the final desktop override at 1000px and above is 1.4:1 with a 64px gap. It stacks at 780px. Feature top padding is 56px by default, 40px at 1000px and above, and 36px on phones. The decision cases remain in the same field, separated by one fine rule. The timeline is an open white section with 60px/50px vertical padding, reduced to 40px/36px on phones.

Current relationship figures pair a 768×224 wide SVG with a separately authored 320×576 vertical SVG; timeline figures pair 768×320 with 320×748. On briefing pages the final cascade switches both at 831px, before the 780px text-layout breakpoint. Vertical figures retain a 320px minimum and 420px maximum, centered; smaller available widths use local figure scrolling. Standalone role and sequence exports switch at 700px. These are distinct export rules, not a replacement site breakpoint. The retained `estima-decision` export is an older 480×464 artifact and does not define the new pattern.

Print hides playback and case controls and exposes every case and timeline fact; it removes the forest field, simplifies layout and omits decorative traces. Site print rules select wide figures, with the later narrow-viewport figure override still part of the actual cascade. Do not assume print changes the evidence content.

## Elevation & Depth

There are no box shadows. Depth comes from white against pale green fields, the reversed forest feature field, contrasting approval nodes, fine borders and typographic hierarchy. Most content remains directly on the page. The circle of a vote or timeline marker and the lightly rounded diagram node are functional shapes within that flat world.

**The Open Document Rule.** Use open sections and fine dividers for the reading structure; reserve tinted containers for figures, context and grouped evidence.

## Shapes

Controls and tags use the compact radius, buttons the button radius, context notes and SVG nodes the note radius, and desktop figure fields the figure radius. The phone figure field uses 5px. Default borders and section rules are 1px; diagram connectors use 1.5px. Vote markers are 30px circles. Avoid interpreting these native diagram and control shapes as a blanket ban on rounded forms.

## Components

### Buttons and links

Primary actions are solid forest with white text, a matching 1px border, 17px semibold body type and a 20px icon gap. Hover changes the filled background to `accent-hover`, without animation. Secondary links use a transparent fill with a forest border and text; their later specificity preserves that transparent fill on hover. The home reading link is an 18px semibold text action with a fine bottom rule. Inline links use offset underlines whose thickness grows on hover.

Keyboard focus is a 3px accent outline offset by 5px. Disabled buttons have half opacity and the default cursor. Pager and retry buttons are compact transparent controls; the source does not establish a bespoke hover or active treatment for them.

### Fields and filtering

Search and category fields use white backgrounds, the field-edge border and the compact radius. Labels are 16px; controls are 17px with 12px padding. The two-control toolbar stacks on phones. Filtering updates the record count and empty state; clearing restores both fields and moves focus to search. No error-color or custom disabled-field system is present.

### Navigation

Navigation is ordinary text, muted at rest. Hover and the current page share ink text and a 1px bottom rule. The desktop links are 16px; the final mobile rule uses 14px and wraps links. Preserve `aria-current` and the skip link. The small linked line above inner-page headings is a breadcrumb, not a decorative label pattern.

### Context and tags

Context notes use a pale field with generous padding and restrained corners; their body is 17px. Tags use a small pale lozenge with 13px text. These are annotations, not an invitation to add ornamental badges or generic cards.

### Evidence and payment disclosures

Tables retain their open document styling. On phones, a 15px muted instruction explains sideways scrolling; the table container is keyboard-focusable, labelled as a region and receives the shared accent outline on focus. Keep long evidence columns inside that local scroll region rather than allowing page overflow. Grid children use a zero minimum width so nested tables remain contained at phone widths.

Use native `details` / `summary` controls. Evidence blocks sit between fine rules with 17px semibold summary text and a padded body. Payment rows align a project name, amount and disclosure affordance; amounts use tabular numerals and overlap amounts use regular weight. Receipt lists preserve dates, transaction links, wallet detail and pagination inside the open record.

Hash navigation opens the target disclosure and containing disclosures, then scrolls to the target. Evidence links open their linked detail. This is in-document navigation rather than a modal or persistent overlay. A targeted evidence block fades from source emphasis to transparent over 1.2 seconds with ease-out. Smooth scrolling is enabled normally; reduced-motion preference disables smooth scrolling, animations and transitions. The approved case and timeline extension adds the bounded vocabulary described below. Sharing uses clipboard copy with a live status message and a URL-copy fallback.

### Decision figures and case controls

Use authored, accessible inline SVG with a title and description, simple rectangular nodes, fine connectors, restrained arrows, source wording and an adjacent caveat. Current figures identify proposer, participating approver and recipient with small inline person/document marks. The approval node receives the pale focal fill; ordinary nodes remain forest. Each wide/vertical pair preserves the same relationships and qualifications. Compact identifiers use the established figure-specific monospace role.

The case selector uses three native buttons with tab semantics, a visible selected state and a 44px minimum height. The default outlined state has muted reversed text; hover uses forest-hover and selection uses mint with forest text. Padding is 9px 21px, becoming 8px 16px on phones. Focus uses the shared 3px/5px geometry in mint on forest. Without JavaScript all three cases are visible and the selector stays hidden; print also exposes all cases. Keep the local context above each diagram and its caveat/source continuation below: Superbolt is a company invoice on Neutron, Creda is a Terra project milestone, and Estima distinguishes approval of the original grant by the other directors from Philipp's later release vote. Those are content qualifications, not interchangeable diagram captions.

Standalone role/sequence HTML currently links Google Fonts, unlike the self-hosted briefing pages. This is an export delivery exception, not a font-loading rule to inherit. The older Estima decision export also retains its previous sans-serif identifiers; that historical drift is not a competing identifier rule.

### Controlled timeline

The sequence adds optional emphasis to a complete four-event figure. All event text remains visible at every step; the current event gets a mint ring, semibold labels and a short tracing underline. Axis breaks and duration labels prevent equal graphical spacing from implying equal elapsed time. Source links and the motive caveat remain adjacent and available throughout.

The canonical `holder-briefing/motion-controller.js` supplies one clock: 720ms holds across four steps (2880ms total). Shape emphasis and the underline use 480ms with `cubic-bezier(.2,.8,.2,1)`; control state transitions use 160ms. Play begins only on request for this step-mode sequence, Pause preserves the step, Previous/Next move one event, Replay restarts and the final step stops. Playback pauses when the page becomes hidden. Arrow keys step, Home/End jump, Space on the sequence background toggles playback, and R replays; native button keyboard behavior remains available. The visible event counter and polite live status communicate progress.

Playback buttons have a 44×44px minimum, 4px corners and white/forest styling; Play uses the base filled action palette. Hover uses tint and accent border, pressed controls receive a fine offset accent outline, and unavailable endpoints use reduced opacity. Controls wrap on phones, with the counter on its own line.

No-JavaScript, `?motion=static`, print and reduced-motion modes preserve the complete figure. Static and reduced modes hide/disable playback controls, suppress decorative traces and show a static explanation. `?motion=step&step=0..4` provides deterministic inspection frames, not a reader-facing mode. Motion may emphasize an event but must never gate its facts.

**The Complete Evidence Rule.** Keep all timeline facts readable before enhancement, during playback and in static or reduced-motion modes; motion marks attention rather than revealing evidence.

## Do's and Don'ts

### Do:
- **Do** use the shipped white and green tokens for the rebuilt briefing.
- **Do** retain explanatory labels and financial qualifications when adapting diagrams to narrow screens.
- **Do** keep source links, native disclosures and keyboard focus visible.
- **Do** use the shipped self-hosted font families on briefing pages.
- **Do** respect reduced motion and retain evidence access without animation.

### Don't:
- **Don't** import the preserved record’s original visual presentation into new briefing surfaces.
- **Don't** replace open reading sections with a general card grid.
- **Don't** add ornamental shadows or persistent motion to this quiet document world.
- **Don't** infer an error palette or downloaded monospace family from the figure-specific system stack.
- **Don't** hide timeline facts between steps or loop the chronology automatically.
