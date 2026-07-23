---
name: Synthetic Intelligence Interface
colors:
  surface: '#fbf8ff'
  surface-dim: '#dbd9e1'
  surface-bright: '#fbf8ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f5f2fa'
  surface-container: '#efedf4'
  surface-container-high: '#e9e7ef'
  surface-container-highest: '#e4e1e9'
  on-surface: '#1b1b21'
  on-surface-variant: '#454651'
  inverse-surface: '#303036'
  inverse-on-surface: '#f2eff7'
  outline: '#767682'
  outline-variant: '#c6c5d3'
  surface-tint: '#4b57aa'
  primary: '#142175'
  on-primary: '#ffffff'
  primary-container: '#2e3a8c'
  on-primary-container: '#9ea9ff'
  inverse-primary: '#bcc3ff'
  secondary: '#505f76'
  on-secondary: '#ffffff'
  secondary-container: '#d0e1fb'
  on-secondary-container: '#54647a'
  tertiary: '#003421'
  on-tertiary: '#ffffff'
  tertiary-container: '#004d33'
  on-tertiary-container: '#2dc68d'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#dfe0ff'
  primary-fixed-dim: '#bcc3ff'
  on-primary-fixed: '#000d60'
  on-primary-fixed-variant: '#333f91'
  secondary-fixed: '#d3e4fe'
  secondary-fixed-dim: '#b7c8e1'
  on-secondary-fixed: '#0b1c30'
  on-secondary-fixed-variant: '#38485d'
  tertiary-fixed: '#6ffbbe'
  tertiary-fixed-dim: '#4edea3'
  on-tertiary-fixed: '#002113'
  on-tertiary-fixed-variant: '#005236'
  background: '#fbf8ff'
  on-background: '#1b1b21'
  surface-variant: '#e4e1e9'
typography:
  display-lg:
    fontFamily: Inter
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
    letterSpacing: -0.01em
  headline-lg-mobile:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  headline-md:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-sm:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  label-md:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.05em
  mono-data:
    fontFamily: JetBrains Mono
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  unit: 4px
  container-max: 1440px
  gutter: 24px
  margin-mobile: 16px
  margin-desktop: 32px
  stack-sm: 8px
  stack-md: 16px
  stack-lg: 32px
---

## Brand & Style

The design system is engineered for high-density NLP analysis, balancing technical authority with cognitive clarity. The brand personality is professional, precise, and illuminating, aimed at data scientists and intelligence analysts who require deep focus.

The design style is **Modern Corporate** with selective **Glassmorphism**. While the core interface remains grounded in structured, legible layouts to handle complex datasets, AI-driven features (like chatbots and generative summaries) utilize translucent, frosted-glass effects to signify their dynamic and non-static nature. This visual distinction helps users differentiate between raw data and AI-augmented insights. High-contrast typography and a restrained use of vibrant accents ensure that the "human" element of the platform remains accessible despite the underlying complexity.

## Colors

The palette is anchored by **Deep Indigo** (#2E3A8C) to project stability and technical trust. **Slate** (#64748B) serves as the primary neutral for secondary UI elements, ensuring the interface feels grounded without becoming visually heavy.

Functional color is critical for NLP analysis:
- **Emerald** (#10B981) is utilized exclusively for positive sentiment indicators, success states, and growth metrics.
- **Coral** (#FB7185) is used for negative sentiment, errors, and critical alerts.
- **Backgrounds** use a very soft Slate tint (#F8FAFC) to reduce eye strain during long-form reading sessions.
- **Glass Effects** use a white semi-transparent layer (RGBA 255, 255, 255, 0.6) with a 12px backdrop blur.

## Typography

This design system uses **Inter** for its exceptional legibility in high-density environments and its neutral, systematic character. The type hierarchy is strictly defined to ensure that users can scan large volumes of text and data visualizations without friction.

- **Headlines:** Use tighter letter spacing and semi-bold weights to create a strong visual anchor.
- **Body Text:** Uses a standard 16px base for optimal reading comfort. For sidebars and dense data tables, `body-sm` (14px) is the preferred standard.
- **Data Display:** For code snippets or raw NLP token strings, **JetBrains Mono** is introduced to provide a distinct visual shift toward "technical data."
- **Mobile Adjustments:** Large headlines are reduced by roughly 25% on mobile devices to preserve screen real estate for the analysis content.

## Layout & Spacing

The layout philosophy follows a **Fluid Grid** model with a maximum content width of 1440px. A 12-column grid is used for dashboards, while a 1-column centered layout (800px max-width) is reserved for long-form article analysis.

- **Rhythm:** An 8px base grid (4px unit) governs all spacing.
- **Margins:** Desktop views utilize a generous 32px outer margin to provide visual "breathing room" amidst complex data. Mobile scales down to 16px.
- **Data Density:** In analytical views, vertical spacing between list items is compressed to `stack-sm` (8px) to maximize the amount of information visible on one screen, while `stack-lg` (32px) is used to separate distinct logical sections.

## Elevation & Depth

Visual hierarchy is established through **Tonal Layers** and **Subtle Outlines** rather than heavy shadows.

- **Level 0 (Base):** Background Slate-50 (#F8FAFC).
- **Level 1 (Cards/Panels):** Pure white background with a 1px border in Slate-200. This provides a crisp, "paper-like" feel for articles and data modules.
- **Level 2 (Modals/Overlays):** These use the **Glassmorphism** effect. Surfaces are semi-transparent with a 12px backdrop blur and a thin, high-contrast white border (0.5px) to simulate light catching the edge of glass.
- **Shadows:** Only used for floating action buttons or active dropdowns. These are ultra-diffused, using 10% opacity Indigo rather than black to maintain color harmony.

## Shapes

The design system employs a **Soft** shape language. Standard elements like buttons, input fields, and cards use a 0.25rem (4px) corner radius. This conveys a professional, slightly technical edge while remaining modern.

- **NLP Badges/Chips:** Use `rounded-xl` (12px) to differentiate them from functional UI buttons.
- **AI Chat Bubbles:** Utilize a hybrid approach—outer corners are `rounded-lg` (8px), but the tail corner is sharper to indicate the source of the message.

## Components

### Buttons & Inputs
- **Primary Action:** Deep Indigo background with white text. High contrast, sharp but slightly rounded corners.
- **Secondary Action:** Ghost style—Slate-200 border, Slate-700 text.
- **Inputs:** Minimalist with a 1px Slate-200 border that transforms to a 2px Indigo border on focus.

### Sentiment Indicators
- **Badges:** Small, pill-shaped markers. Positive sentiment uses Emerald background with 10% opacity and Emerald-700 text. Negative uses Coral with 10% opacity and Coral-700 text.
- **Progress Bars:** Thin (4px height) tracks for sentiment distribution (e.g., 70% positive Emerald / 30% negative Coral).

### AI & Chat
- **Chat Interface:** AI responses are styled with the Glassmorphism effect (frosted background) to distinguish them from human-generated notes.
- **Typing Indicator:** Three animated dots using the Indigo primary color.

### Article Layouts
- **Structured Sections:** Use a "sticky" left-hand sidebar for metadata (author, date, sentiment score) and a centered main column for the body text to ensure maximum readability and focus.