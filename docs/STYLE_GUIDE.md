> [!IMPORTANT]
> This is a local copy of the Style Guide for the **rating** microservice.
> Please refer to the main repository's [docs/STYLE_GUIDE.md](../../docs/STYLE_GUIDE.md) for the authoritative source of truth.

# Tender Finder 2.0 Style Guide

## UI/UX Principles (Porsche Design System Inspired)

### 1. Absolute Sovereign Immersion
The user must feel they are inside a secure, high-fidelity command center. Any browser-native UI that breaks this immersion is forbidden.

### 2. Zero Pop-up Mandate
*   **No Alerts**: Standard browser `alert()`, `confirm()`, or `prompt()` calls are strictly forbidden. They are unreliable and break the professional aesthetic.
*   **Inline Status**: Use inline status messages, progress bars, or toast-style notifications that are part of the page's DOM.
*   **High-Contrast Feedback**: Errors should use the `--accent-color` (#d5001c), and successes should use a muted success green, integrated into the PDS color palette.

### 3. Typography & Spacing
*   **Inter / Roboto**: Use clean, modern sans-serif fonts.
*   **Letter Spacing**: Use `0.1em` to `0.2em` for headers and buttons to enhance the premium feel.
*   **Monospacing**: Use for identifiers, keys, and status codes to emphasize the technical nature of the system.

### 4. Clean 19:19 Design Language
*   **Absolute Black**: Dark mode must utilize `#000000` for the primary canvas to ensure maximum visual depth and focus.
*   **High-Density Grids**: UI should be optimized for information density. Remove redundant headers and use tight spacing (8-12px) for data cards.
*   **Micro-Indicators**: Use subtle micro-icons or sparkle emojis (✨) for status enrichment (e.g., AI Enriched) to avoid cluttering the view with heavy badges.
*   **Small Metadata**: Meta-information (dates, IDs, clients) should use a reduced font size (10px) and muted opacity (0.5-0.6) to keep the primary title readable.

### 5. Cross-Platform Responsiveness
*   **Dynamic Viewports**: Always use `dvh` (Dynamic Viewport Height) or `vh` fallbacks for full-screen layouts to ensure perfect fit on mobile browsers (Safari/Chrome) where address bars expand and contract.
*   **Adaptive Grids**: Dashboard layouts must use fluid grids that gracefully transition from multi-column (Desktop) to single-column (Mobile) views.
*   **System-Native Refinement**: Replace default OS scrollbars with themed, minimal custom scrollbars (especially for Windows/Dell users) to maintain the "Sovereign Immersion."

### 6. Tactile & Premium Interactions
*   **Glassmorphism**: Use `backdrop-filter: blur()` for sticky elements (like headers) to create depth and a high-end feel.
*   **Reactive Feedback**: 
    *   **Lifting**: Interactive cards should lift slightly (`translateY`) on hover to indicate clickability.
    *   **Scaling**: Buttons should provide immediate haptic-style feedback via subtle scaling (`scale(0.95)`) when pressed.
*   **Smooth Transitions**: All state changes (theme toggles, hovers, visibility) must use cubic-bezier transitions for an "Apple-style" fluidity.

### 7. Role-Based Theming
*   **Bright Background**: Standard Users interact with the platform using a bright, clean, premium background theme.
*   **Dark Background**: Admins (specifically Basti and Nils) are granted a deep, dark mode canvas to maintain executive status indicators.

## Authentication Logic

### 1. Perpetual Handshake
Human sessions should be valid indefinitely unless explicitly revoked via the IAM Sovereign Control panel.

### 2. Hard-Deny Default
All endpoints must default to a 401/403 state unless a valid cryptographic principal is presented and verified against the real-time database state.

## Approved Porsche Design System Components
The UI should exclusively use the following components from the Porsche Design System (v3):

1. [**Accordion**](https://designsystem.porsche.com/v3/components/accordion)
2. [**Banner**](https://designsystem.porsche.com/v3/components/banner)
3. [**Button**](https://designsystem.porsche.com/v3/components/button)
4. [**Button Pure**](https://designsystem.porsche.com/v3/components/button-pure)
5. [**Button Tile**](https://designsystem.porsche.com/v3/components/button-tile)
6. [**Canvas**](https://designsystem.porsche.com/v3/components/canvas)
7. [**Carousel**](https://designsystem.porsche.com/v3/components/carousel)
8. [**Checkbox**](https://designsystem.porsche.com/v3/components/checkbox)
9. [**Crest**](https://designsystem.porsche.com/v3/components/crest)
10. [**Display**](https://designsystem.porsche.com/v3/components/display)
11. [**Divider**](https://designsystem.porsche.com/v3/components/divider)
12. [**Drilldown**](https://designsystem.porsche.com/v3/components/drilldown)
13. [**Fieldset**](https://designsystem.porsche.com/v3/components/fieldset)
14. [**Flag**](https://designsystem.porsche.com/v3/components/flag)
15. [**Flyout**](https://designsystem.porsche.com/v3/components/flyout)
16. [**Heading**](https://designsystem.porsche.com/v3/components/heading)
17. [**Icon**](https://designsystem.porsche.com/v3/components/icon)
18. [**Inline Notification**](https://designsystem.porsche.com/v3/components/inline-notification)
19. [**Input Date**](https://designsystem.porsche.com/v3/components/input-date)
20. [**Input Email**](https://designsystem.porsche.com/v3/components/input-email)
21. [**Input Month**](https://designsystem.porsche.com/v3/components/input-month)
22. [**Input Number**](https://designsystem.porsche.com/v3/components/input-number)
23. [**Input Password**](https://designsystem.porsche.com/v3/components/input-password)
24. [**Input Search**](https://designsystem.porsche.com/v3/components/input-search)
25. [**Input Tel**](https://designsystem.porsche.com/v3/components/input-tel)
26. [**Input Text**](https://designsystem.porsche.com/v3/components/input-text)
27. [**Input Time**](https://designsystem.porsche.com/v3/components/input-time)
28. [**Input Url**](https://designsystem.porsche.com/v3/components/input-url)
29. [**Input Week**](https://designsystem.porsche.com/v3/components/input-week)
30. [**Link**](https://designsystem.porsche.com/v3/components/link)
31. [**Link Pure**](https://designsystem.porsche.com/v3/components/link-pure)
32. [**Link Tile**](https://designsystem.porsche.com/v3/components/link-tile)
33. [**Link Tile Model Signature**](https://designsystem.porsche.com/v3/components/link-tile-model-signature)
34. [**Link Tile Product**](https://designsystem.porsche.com/v3/components/link-tile-product)
35. [**Modal**](https://designsystem.porsche.com/v3/components/modal)
36. [**Model Signature**](https://designsystem.porsche.com/v3/components/model-signature)
37. [**Multi Select**](https://designsystem.porsche.com/v3/components/multi-select)
38. [**Pagination**](https://designsystem.porsche.com/v3/components/pagination)
39. [**Pin Code**](https://designsystem.porsche.com/v3/components/pin-code)
40. [**Popover**](https://designsystem.porsche.com/v3/components/popover)
41. [**Radio Group**](https://designsystem.porsche.com/v3/components/radio-group)
42. [**Scroller**](https://designsystem.porsche.com/v3/components/scroller)
43. [**Segmented Control**](https://designsystem.porsche.com/v3/components/segmented-control)
44. [**Select**](https://designsystem.porsche.com/v3/components/select)
45. [**Sheet**](https://designsystem.porsche.com/v3/components/sheet)
46. [**Spinner**](https://designsystem.porsche.com/v3/components/spinner)
47. [**Stepper Horizontal**](https://designsystem.porsche.com/v3/components/stepper-horizontal)
48. [**Switch**](https://designsystem.porsche.com/v3/components/switch)
49. [**Table**](https://designsystem.porsche.com/v3/components/table)
50. [**Tabs**](https://designsystem.porsche.com/v3/components/tabs)
51. [**Tabs Bar**](https://designsystem.porsche.com/v3/components/tabs-bar)
52. [**Tag**](https://designsystem.porsche.com/v3/components/tag)
53. [**Tag Dismissible**](https://designsystem.porsche.com/v3/components/tag-dismissible)
54. [**Text**](https://designsystem.porsche.com/v3/components/text)
55. [**Text List**](https://designsystem.porsche.com/v3/components/text-list)
56. [**Textarea**](https://designsystem.porsche.com/v3/components/textarea)
57. [**Toast**](https://designsystem.porsche.com/v3/components/toast)
58. [**Wordmark**](https://designsystem.porsche.com/v3/components/wordmark)

*Note: Deprecated or internal wrapper components (e.g., TextareaWrapper, SelectWrapper) must not be used.*
