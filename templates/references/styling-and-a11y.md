> [!WARNING]
> Generic starter standards. CSS variable names below (`--color-*`, `--spacing-*`, `--font-*-family`) come from another theme (Dawn-style) and **will differ** in your base theme. Verify names in the theme's styles-variables snippet before using; theme source and `theme/AGENTS.md` win on conflict.

# Styling, Accessibility & SEO

> **Read this** when writing or modifying CSS, accessibility patterns, or SEO meta. Sourced from the project `CLAUDE.md`

---

## ♿ Accessibility (a11y) — WCAG 2.1 Level AA

### Mandatory Practices (REQUIRED)

🔴 **REQUIRED**: All interactive elements MUST be keyboard accessible and have visible focus:

```liquid
<button
  type="button"
  class="{{PREFIX}}-button"
  aria-label="{{ 'general.accessibility.close' | t }}"
>
  Close
</button>
```

```css
button:focus-visible {
  outline: 2px solid var(--color-focus);
  outline-offset: 2px;
}
```

🔴 **REQUIRED**: Proper color contrast (4.5:1 for normal text, 3:1 for large):

**DO**: Text color `#000` on background `#fff` = 21:1 contrast (PASS).

**DON'T**: Text color `#999` on background `#f5f5f5` = 2.1:1 contrast (FAIL).

Use https://webaim.org/resources/contrastchecker/ to verify.

### ARIA & Form Standards (REQUIRED)

🔴 **REQUIRED**: All form inputs have associated labels:

**DO**:
```liquid
<label for="search-input">{{ 'general.search.placeholder' | t }}</label>
<input type="search" id="search-input" name="q">
```

**DON'T**:
```liquid
<input type="search" placeholder="Search...">
```

🔴 **REQUIRED**: Dynamic content uses `aria-live`:

```liquid
<div aria-live="polite" aria-atomic="true">
  {{ 'cart.items.count' | t: count: cart.item_count }}
</div>
```

🔴 **REQUIRED**: Use correct ARIA roles for patterns:

```liquid
{%- comment %} Accordion Pattern -%}
<button
  type="button"
  id="accordion-trigger-1"
  aria-expanded="false"
  aria-controls="accordion-panel-1"
>
  Section Title
</button>
<div id="accordion-panel-1" role="region" aria-labelledby="accordion-trigger-1" hidden>
  Content here
</div>

{%- comment %} Modal Pattern -%}
<div role="dialog" aria-modal="true" aria-labelledby="modal-title">
  <h2 id="modal-title">Dialog Title</h2>
  <button aria-label="{{ 'general.accessibility.close' | t }}">×</button>
</div>
```

### Reduced Motion (REQUIRED)

🔴 **REQUIRED**: Respect `prefers-reduced-motion` media query:

**DO**:
```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

**DON'T**: Use animations that can't be disabled.

---

## 🔍 SEO Standards

### Meta Tags (REQUIRED)

🔴 **REQUIRED**: Verify meta tags in page layout/template:

| Tag | Rule | Example |
|-----|------|---------|
| `<title>` | Unique, under 60 chars | `"Blue Ceramic Vase - {{BRAND}}"`  |
| `og:title` | Under 60 chars | Same as `<title>` |
| `og:description` | Under 160 chars | Clear product/category summary |
| `og:image` | 1200×630px minimum | High-quality hero image |

### Semantic HTML & Heading Hierarchy (REQUIRED)

🔴 **REQUIRED**: One `<h1>` per page, proper hierarchy:

**DO**:
```liquid
<h1>Main Page Title</h1>
<section>
  <h2>Section Heading</h2>
  <h3>Subsection Heading</h3>
</section>
```

**DON'T**:
```liquid
<h1>Title</h1>
<h3>Next Section</h3>  <!-- Skipped h2 -->
<h1>Another Title</h1> <!-- Two h1s -->
```

---

## 📱 Responsive Design Standards

### Breakpoint Strategy (REQUIRED)

🔴 **REQUIRED**: Mobile-first CSS with these breakpoints:

```css
/* Base (mobile) - no media query needed */
.component { padding: 1rem; }

/* Tablet - 768px and up */
@media (min-width: 768px) {
  .component { padding: 1.5rem; }
}

/* Desktop - 1024px and up */
@media (min-width: 1024px) {
  .component { padding: 2rem; }
}

/* Large desktop - 1440px and up */
@media (min-width: 1440px) {
  .component { padding: 2.5rem; }
}
```

🟡 **RECOMMENDED**: Use container queries for component-level responsiveness:

```css
@container (min-width: 500px) {
  .card { display: grid; grid-template-columns: auto 1fr; }
}
```

### Touch Target Size (REQUIRED)

🔴 **REQUIRED**: All interactive elements ≥ 44×44px (at least one dimension):

**DO**: `<button class="btn">Click me</button>` + CSS `min-height: 44px; min-width: 44px;`

**DON'T**: `<a href="/">Small link</a>` = 24×24px

---

## 🎨 CSS Architecture & Naming

### CSS Variable System (REQUIRED)

🔴 **REQUIRED**: Use only theme-provided CSS variables (`--color-*`, `--font-*`, `--space-*`):

**Available Variables** (from Shopify Dawn theme):
```css
/* Colors */
--color-foreground
--color-background
--color-accent
--color-shadow
--color-success
--color-error
--color-warning

/* Typography */
--font-body-family
--font-heading-family
--font-body-scale
--font-heading-scale

/* Spacing */
--spacing-xs: 0.25rem
--spacing-sm: 0.5rem
--spacing-md: 1rem
--spacing-lg: 2rem
--spacing-xl: 3rem
```

🔴 **REQUIRED**: Avoid `!important` in custom CSS. Use the theme's CSS variable system and proper selector specificity to manage styles.

🔴 **REQUIRED**: All new components must use `var(--color-*)` and `var(--spacing-*)` instead of hardcoded hex codes or pixel values.

**DO**: Use existing variables:
```css
.card {
  color: var(--color-foreground);
  background: var(--color-background);
  padding: var(--spacing-md);
}
```

**DON'T**: Create custom variables without `--{{PREFIX}}-` prefix:
```css
/* This will clash with theme settings */
--card-bg: #fff;
--card-text: #000;
```

🟡 **RECOMMENDED**: If you must create new variables, use prefix:
```css
:root {
  --{{PREFIX}}-hero-min-height: 400px;
  --{{PREFIX}}-accent-dark: color-mix(in srgb, var(--color-accent) 80%, black);
}
```

### BEM Naming Convention (REQUIRED)

🔴 **REQUIRED**: All custom classes follow BEM with `{{PREFIX}}-` prefix:

```css
/* Block: {{PREFIX}}-card */
.{{PREFIX}}-card {
  border-radius: 8px;
  box-shadow: var(--shadow-md);
}

/* Element: {{PREFIX}}-card__header */
.{{PREFIX}}-card__header {
  padding: var(--spacing-md);
  border-bottom: 1px solid var(--color-border);
}

/* Modifier: {{PREFIX}}-card--featured */
.{{PREFIX}}-card--featured {
  border: 2px solid var(--color-accent);
}

/* Sub-element: {{PREFIX}}-card__header-title */
.{{PREFIX}}-card__header-title {
  font-size: var(--font-size-lg);
  font-weight: 600;
}
```

**DO**: Use BEM strictly:
```css
.{{PREFIX}}-product-grid
.{{PREFIX}}-product-grid__item
.{{PREFIX}}-product-grid__item--sale
.{{PREFIX}}-product-grid__item-badge
```

**DON'T**: Use nested selectors or non-BEM naming:
```css
.{{PREFIX}}-product-grid > div > .item { }  /* Not BEM */
.product-item { }  /* Missing {{PREFIX}}- prefix */
```