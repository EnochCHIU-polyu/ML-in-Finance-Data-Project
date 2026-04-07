---
name: create-ppt
description: "Create PowerPoint-ready technical presentation decks from reports, notebooks, or project notes. Use when you need slide outlines, speaker notes, visual recommendations, and quality checks for an ML/analytics PPT deliverable."
argument-hint: "Topic, audience, duration, and source materials for the deck"
user-invocable: true
---

# Create PPT

Generate a complete, presentation-ready slide plan from source material with clear narrative flow, visual guidance, and a final quality gate.

Default profile: Technical/ML audience, English output, full workflow, PowerPoint-focused structure.

## When to Use

- Convert a technical report into slides.
- Turn notebook/project outputs into an executive briefing.
- Build a client/class presentation with time constraints.
- Improve an existing deck structure and messaging.

## Inputs to Collect

- Presentation goal and desired outcome.
- Audience level: technical/ML by default unless user overrides.
- Time limit (for example 5, 10, 15, or 30 minutes).
- Source assets: reports, notebooks, metrics, charts, logs.
- Required style constraints: template, language, tone, branding.

If any input is missing, ask targeted follow-up questions before drafting.

## Workflow

1. Define the talk contract.

- Write one sentence each for: objective, target audience, and call-to-action.
- Calculate slide budget using a pacing rule of about 1 slide per minute.
- Reserve 1-2 slides for backup/Q&A if audience is technical.

2. Extract and rank source material.

- Identify key claims, supporting evidence, and notable numbers.
- Classify candidate content as: must-have, nice-to-have, discard.
- Prefer evidence with measurable impact and clear provenance.

3. Design the storyline.

- Choose one narrative arc:
  - Problem -> Analysis -> Solution -> Impact.
  - Goal -> Method -> Results -> Risks -> Next steps.
  - Context -> Experiments -> Findings -> Decision.
- Create a sectioned outline with estimated time per section.

4. Produce slide-by-slide blueprint.

- For each slide define:
  - Slide title (assertive, outcome-oriented).
  - One core message sentence.
  - 3-5 bullets maximum.
  - Recommended visual type (line chart, bar chart, table, diagram, image).
  - Speaker note summary (2-4 lines).
- Keep one idea per slide.

5. Add evidence and visuals.

- Map each claim to a data point, chart, or source quote.
- If a chart is unclear, rewrite with simpler encoding and one highlighted insight.
- Ensure chart labels include units and time windows.

6. Run quality checks.

- Narrative coherence: each slide should answer "why this now?".
- Readability: short bullets, consistent terminology, no text walls.
- Time fit: estimated speaking time should not exceed the limit.
- Decision readiness: final slides include recommendation, risks, and next actions.

7. Prepare deliverables.

- Output final deck package:
  - Slide outline with numbering.
  - Suggested layout per slide (title and content, two-column, comparison, full-bleed chart).
  - Presenter notes.
  - Visual/table checklist.
  - Per-slide evidence source mapping.
  - Optional appendix slide list.
- If requested, generate a condensed version (for example 5-slide executive summary).

## PowerPoint Output Contract

- Provide slide titles that can be copied directly as PowerPoint slide headers.
- Keep body copy concise for common PPT layouts:
  - Title and content: 3-5 bullets.
  - Two-column: up to 3 bullets per side.
  - Chart slide: one chart + one takeaway sentence.
- Include presenter notes under a clear Notes label for each slide.
- Mark optional animations/transitions only when they reinforce logic.

## Decision Rules

- If audience is executive:
  - Lead with outcome and business impact within first 2 slides.
  - Minimize methodology depth; keep technical details in appendix.
- If audience is technical:
  - Include data and method assumptions explicitly.
  - Add limitations, ablations, and failure modes.
- If time is under 10 minutes:
  - Use at most 7 core slides and 1 backup slide.
- If source quality is weak or inconsistent:
  - Flag confidence levels and list validation gaps before conclusions.

## Completion Criteria

- The deck has a clear beginning, middle, and end.
- Every major claim is backed by evidence.
- Slide count matches time constraints.
- A final recommendation and concrete next steps are present.
- Output is ready to transfer into PowerPoint/Google Slides with minimal rewriting.
- Technical appendix covers assumptions, limitations, and validation checks.

## Example Prompts

- /create-ppt Build a 12-minute technical presentation from our stock regression report for an ML audience.
- /create-ppt Turn this project report into a 6-slide executive briefing focused on business impact and risk.
- /create-ppt Redesign this draft deck for a classroom presentation with clearer storyline and speaker notes.
