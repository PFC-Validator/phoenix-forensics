# Control page: visual explanation and proposal connection

## Editorial basis

This update reorganizes the existing 16 November control review. It adds no new
chain capture and does not widen its 27-contract scope. The new proposal section
links the exact 16 November discussion revision already used on the overview
and governance pages: `f5c703162cb9b08a218dcec67aae6fe645d064dd`.

- Proposal 1 changes membership through a controlled transition, preserving the
  affirmative-approval minimum. Removing a director alone does not transfer an
  ERIS contract administrator or registry owner.
- Proposal 2 supplies independent governance/accountability measures and can
  proceed with the existing Board if Proposal 1 fails.
- Both call for direct and indirect authority records, source/build/licence and
  maintenance access, verified operating readiness, and a dated remedy for gaps.
- Seven-day acknowledgement and 21-day dossier clocks run from passage. Proposal
  2's preliminary/final review clocks run from legal adoption (30/60 days).
- Discussion, passage, legal adoption and executed contract changes remain
  distinct. The evidence does not establish misconduct or liability, and neither
  proposal automatically recovers assets or transfers unrelated ERIS property.

## Visual meaning

The forest figure separates the Board's normal payment authority, ERIS's power
to replace Treasury code, and ERIS's registry ownership. Replacement Treasury
code could bypass Board authorization without changing the Board's own voting
threshold. The figure does not depict unilateral ordinary payments by ERIS.

The visible ledger credits completed hub/bridge upgrade transfers and configured
Treasury safeguards, while distinguishing unresolved TLA administration and
configuration handovers and current-source validation. TLA's one/three-month
commitments are not attributed to the Treasury grant. The timeline records
selected dated events without inventing elapsed-time proportions or a calendar
deadline absent from the original commitment.

## Design and validation

Impeccable 4.8.0 and the approved forest diagram skin were used. Independent
source review identified article-width reflow as a risk, addressed through HTML
labels and container-based layout rather than fixed-width SVG text.

The manual detector flagged inherited heading-leading, type-scale and boundary
padding patterns. Its tracking warning misread the existing `-.025em` rule as
larger negative values; the CSS declaration and Chrome rendering were checked.
Fine section/table rules intentionally have no lateral box padding; their text
has column/cell spacing. The design record now documents the actual shipped
container and type sizes. No detector score is treated as visual verification.

Final source review found and resolved incomplete indexes on pages with unlabelled
sections, a missing screen-reader-only utility and a skipped timeline heading
level. Existing IDs remain unchanged; newly indexed sections receive readable,
unique IDs. The diagram self-check targets standalone animated SVG documents;
it rejected this page's necessary external citations, normal site script and
static HTML figure. Those assumptions do not apply to this embedded figure; its
meaning and reflow were checked in Chrome instead. No citations were removed to
satisfy that tool.

Chrome visual checks covered the 1575px desktop control diagram and shared
Treasury rail, the 1024px timeline, and 390px proposal text, control routes,
commitment rows and compact navigation. The menu opens with Enter and links
reach their sections. Final reload confirmed hidden date suffixes. The site
verifier passed in both the audit and publishing checkouts; all 1,671 public
files matched by SHA-256 before packaging. No private screenshots are included.
