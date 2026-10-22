# Contextual Guide Feedback

Work: NEWGAMES-GUIDE-FEEDBACK
Date: 2026-10-23

## Scope

Four existing guides with `guideNavigation: true` gain a modest end-of-article feedback area: Sudoku first moves, block placement, the save checklist, and the puzzle-style comparison. The homepage and article source bodies/dates are unchanged. No additional article is published.

The email link addresses `hello@newgames.ai` and pre-fills only the public article title, canonical URL and a blank question/correction prompt. It does not collect browsing history, game state or personal data, and does not send mail automatically. The reader reviews and sends the message in their email client. `/contact/` provides an ordinary-page fallback with a visible email address, useful context to include, and a reminder not to send private information. It opens at the page top rather than a fragment that could be obscured by the sticky header.

Contact guidance distinguishes editorial questions from game support and offers no response-time or publication guarantee. No form, subscription, JavaScript, analytics, local storage, account or third-party service is added. Existing privacy wording remains applicable. Mail delivery itself is not established by link validation.

## Validation

- Build the isolated staged source, not the unrelated artwork/design WIP.
- Run the repository check, Hugo production build, existing guide/feed validators and `tools/check_guide_feedback.py`.
- Check four opt-in guides, correct decoded mail recipients/subjects/bodies, contact fallback and no feedback on unrelated pages.
- Compare homepage and RSS output with the previous release; preserve publication dates and feed identities.
- Check mobile/desktop, keyboard access, JavaScript-disabled navigation, enlarged text and existing practice shortcuts.
- After the scoped GitHub commit/push, check the live site for the same markup and stylesheet.

## Follow-Up

Review voluntary reader questions before deciding on further guide expansion. This creates a feedback route, not evidence of improved retention. Do not publish readers' messages or claim measured demand. Real RSS-reader polling remains a separate unverified item.
