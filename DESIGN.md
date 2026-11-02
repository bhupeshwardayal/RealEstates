# Design System: Sovereign Asset & Capital

> **Bright Luxury Proptech & Wealth-Management Interface**  
> Tailored for the **AI-Powered Real Estate Advisor & Property Matcher** (SRS v1.0).

---

## 1. Visual Theme & Atmosphere
The design system establishes a hyper-refined, institutional-grade proptech and wealth-management aesthetic tailored for high-net-worth real estate acquisition, conversational property matching, and fractional capital deployment. The ethos fuses architectural modernism with quantitative precision: ultra-crisp white canvases, surgical micro-lines, and deliberate negative space convey institutional security and bespoke luxury.

### Atmosphere Spectrum:
- **Density:** Balanced & Architectural (5/10)
- **Variance:** Offset Asymmetric Layouts (6/10)
- **Motion:** Fluid CSS & Micro-Interactions (6/10)
- **Aesthetic Archetype:** Minimalism with Ambient Glass & Micro-Borders

---

## 2. Color Palette & Roles

| Token | Name | Hex Code | Functional Role |
| :--- | :--- | :--- | :--- |
| `primary` | Imperial Emerald | `#003527` | Dominant brand mark, primary actions, and hero headers |
| `primary-container` | Deep Emerald | `#064E3B` | Interactive primary buttons, emphasis badges |
| `primary-fixed` | Mint Frost | `#B0F0D6` | Ambient pill backgrounds, active beacon pulses |
| `tertiary` | High-Luster Jade | `#0D9488` | AI match tags, confidence highlights, yield meters |
| `canvas-base` | Pure Crystalline White | `#FFFFFF` | Core application surfaces, cards, input backgrounds |
| `surface-ground` | Soft Alabaster | `#FAF8FF` | Full-page background canvas |
| `surface-low` | Slate Dew | `#F2F3FF` | Recessed containers, form inputs, zebra striping |
| `neutral-text` | Obsidian Slate | `#131B2E` | High-contrast WCAG AAA primary typographic ink |
| `secondary-text` | Muted Steel | `#545F73` | Subtitles, metadata tags, micro-labels |
| `outline-border` | Whisper Slate | `#E2E8F0` | 1px micro-borders, structural dividers |
| `badge-verified` | Emerald Tint | `#ECFDF5` | RERA and Grounding Verified trust seals |

---

## 3. Typographic Architecture

- **Display & Headings:** `Plus Jakarta Sans` — Track-tight, controlled geometric scale, weight-driven hierarchy (`600`, `700`, `800`).
- **Body & Financial Disclosures:** `Inter` — Relaxed leading, maximum 65 characters per line, neutral secondary tone.
- **Quantitative & Numerical Valuations:** `Plus Jakarta Sans` with `tabular-nums` enabled (`₹1.22 Cr`, `7.1% Net Yield`, `₹84,700/mo`) to guarantee zero optical jitter during dynamic recalculations.
- **Status & Operational Tags:** `label-caps` in strict uppercase with expanded tracking (`0.06em`, `11px`, `font-weight: 600`).

---

## 4. Component Stylings & Behaviors

### Primary Investment Actions & Buttons
- Flat solid background (`#064E3B`), crisp white text, `0.5rem` (`8px`) border radius, `12px` vertical by `24px` horizontal padding.
- Micro-interaction: Smooth hover transition to `#047857`, `-1px` tactile translate on active state.

### Conversational AI Console
- Split-screen layout positioning the natural language query stream alongside prompt suggestion chips.
- Message bubbles clearly differentiated: High-contrast emerald bubble for user queries, ambient frosted bubble with verified RERA/Grounding badges for AI responses.
- Grounding badge: Emerald pill (`#ECFDF5`) with sparkle icon, latency indicator (`182ms`), and direct links to registry index documents.

### Real-Time Financial Amortization & Yield Engine
- Interactive range sliders for Property Value (₹30L – ₹5Cr), Down Payment (10% – 50%), Loan Tenure (5 – 30 Years), and Interest Rate (7% – 12%).
- Dynamic live recalculations of:
  - Monthly EMI ($E = P \cdot r \cdot \frac{(1+r)^n}{(1+r)^n - 1}$)
  - Gross Rental Yield ($\text{Yield} = \frac{\text{Annual Rent}}{\text{Purchase Price}} \times 100$)
  - Loan-to-Value (LTV) and Principal Breakdown.

### Asset Dossier Cards
- Uncropped 16:10 architectural visual canvas with rounded corners (`1rem`).
- Floating badges for AI Match score (`99.4% AI Match`) and RERA certification.
- Three-column structured metrics grid: Carpet Area, Configuration (BHK), and Possession Status.
- Secondary actions: `Inspect Grounding`, `Calculate Loan`, and `Schedule Tour`.

---

## 5. Anti-Patterns (Strictly Enforced)

- ❌ No emojis in UI interfaces.
- ❌ No generic AI neon/purple outer glows.
- ❌ No pure black (`#000000`) surfaces.
- ❌ No fabricated or ungrounded statistics.
- ❌ No generic 3-column identical card rows without asymmetric visual anchors.
- ❌ No broken Unsplash placeholder image links.

