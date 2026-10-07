# Liquid & Schema Standards

> **Read this** when writing or modifying Liquid, schemas, or Shopify section/block files. Sourced from the project `CLAUDE.md` — scoped to this file for context economy.

---

## 🛠️ Shopify Liquid Standards

### File Structure & Organization

#### Section vs Block vs Snippet

| Type | Purpose | Location | Scope |
|------|---------|----------|-------|
| **Section** | Full-page layout with settings; rendered by template | `/theme/sections/` | Global; multiple instances per page |
| **Block** | Reusable unit within a section; has own schema | Part of section schema | Within parent section |
| **Snippet** | Shared code fragment; no schema | `/theme/snippets/` | Called via `{% render %}` |

🔴 **REQUIRED**: Never use `{% include %}`—always use `{% render %}` (isolated scope, safer).

🔴 **REQUIRED**: Each section/block MUST have a unique `data-block-id` for testing/JS hooks:
```liquid
data-block-id="{{PREFIX}}-{{ section.id }}"
```

#### Nesting & Complexity Rules

🔴 **REQUIRED**: Max 3 levels of Liquid nesting to prevent performance degradation:
```liquid
{%- liquid
  {% if condition_1 %}
    {% if condition_2 %}
      {% if condition_3 %}
        {%- comment %} STOP HERE—use assign/capture or extract to snippet -%}
      {% endif %}
    {% endif %}
  {% endif %}
-%}
```

**DO** extract nested logic to a snippet:
```liquid
{% render 'components/conditional-renderer', data: item %}
```

**DON'T** nest more than 3 levels deep.

### Asset Management

🔴 **REQUIRED**: Use `| asset_url` for all static files. Never hardcode paths:

**DO**:
```liquid
<link rel="stylesheet" href="{{ 'component.css' | asset_url }}">
<img src="{{ 'logo.svg' | asset_url }}" alt="Logo">
```

**DON'T**:
```liquid
<link rel="stylesheet" href="/cdn/theme/assets/component.css">
<img src="https://example.com/logo.svg">
```

### Color & Styling

🔴 **REQUIRED**: All colors MUST use CSS variables from theme settings. No hardcoded hex/rgb:

**DO**:
```liquid
<div style="color: var(--color-foreground); background: var(--color-background);">
```

**DON'T**:
```liquid
<div style="color: #333; background: #fff;">
```

🟡 **RECOMMENDED**: For new color variables, use `--{{PREFIX}}-*` prefix in custom CSS:
```css
--{{PREFIX}}-accent-primary: var(--color-accent);
--{{PREFIX}}-accent-dark: color-mix(in srgb, var(--color-accent) 80%, black);
```

### Semantic HTML

🔴 **REQUIRED**: Use proper heading hierarchy (h1 → h6) and landmark elements:

**DO**:
```liquid
<main>
  <h1>Page Title</h1>
  <section>
    <h2>Section Heading</h2>
    <article>...</article>
  </section>
</main>
```

**DON'T**:
```liquid
<div class="main">
  <h3>Page Title</h3>
  <div class="section">
    <h2>Section Heading</h2>
  </div>
</div>
```

🔴 **REQUIRED**: Use semantic tags (`<header>`, `<nav>`, `<main>`, `<aside>`, `<footer>`, `<article>`, `<section>`).

---

## 📋 Schema & Configuration Standards

### Schema Validation Rules

🔴 **REQUIRED**: All schema JSON must pass Shopify validation. Apply these constraints:

| Constraint | Rule | Example |
|-----------|------|---------|
| **range steps** | `(max - min) / step ≤ 101` | `min: 0, max: 100, step: 1` = 101 steps (VALID) |
| **range max** | `max < 10000` | `max: 9999` (valid); `max: 10000` (invalid) |
| **rich_text** | Keep default under 500 chars | Avoid pre-filling with long content |
| **collection picker** | Test `visible_if` carefully | May fail in older CLI versions |

**DO**:
```json
{
  "type": "range",
  "id": "padding",
  "min": 0,
  "max": 100,
  "step": 5,
  "unit": "px",
  "label": "Padding",
  "default": 20
}
```

**DON'T**:
```json
{
  "type": "range",
  "id": "padding",
  "min": 0,
  "max": 10000,
  "step": 1,
  "label": "Padding"
}
```

### Settings Organization

🔴 **REQUIRED**: Group related settings into logical groups using `"info"` fields:

```json
{
  "type": "header",
  "content": "Layout Settings"
},
{
  "type": "select",
  "id": "layout_style",
  "label": "Layout Style",
  "options": [
    { "label": "Grid", "value": "grid" },
    { "label": "List", "value": "list" }
  ]
},
{
  "type": "info",
  "content": "Choose how products are displayed. Grid shows images prominently; List is text-heavy."
}
```

🟡 **RECOMMENDED**: Always provide sensible defaults for all settings (don't leave blank).

### Localization & Translations

🔴 **REQUIRED**: All user-facing text must use translation keys:

**DO**:
```liquid
<p>{{ 'sections.product.add_to_cart' | t }}</p>
<button>{{ 'general.accessibility.close' | t }}</button>
```

**DON'T**:
```liquid
<p>Add to cart</p>
<button>Close</button>
```

🟡 **RECOMMENDED**: Check `/theme/locales/en.default.json` for existing keys before creating new ones.

---

## 🚀 Performance Standards

### Image Optimization (REQUIRED)

🔴 **REQUIRED**: All product/featured images MUST include responsive srcsets and lazy loading:

```liquid
{{ image | image_url: width: 1500 | image_tag:
  widths: '375, 550, 750, 1100, 1500',
  sizes: '(min-width: 1200px) 50vw, (min-width: 750px) calc(50vw - 2rem), calc(100vw - 2rem)',
  loading: 'lazy',
  alt: image.alt | escape,
  class: 'product-image'
}}
```

🔴 **REQUIRED**: Define aspect ratio to prevent CLS (Cumulative Layout Shift):

```html
<div class="image-wrapper" style="aspect-ratio: 3 / 4;">
  {{ image | image_url: width: 500 | image_tag: loading: 'lazy', alt: image.alt }}
</div>
```

**DO**: Compress images to < 200KB (PNG/JPG); use WebP with fallbacks.

**DON'T**: Load unoptimized full-res images; use hardcoded widths without srcset.

### JavaScript Performance (RECOMMENDED)

🟡 **RECOMMENDED**: Keep individual JS files under 50KB (gzipped). Split large features:

**DO**:
```javascript
// Separate module for each feature
export const initializeProductCarousel = () => { /* */ };
export const initializeQuickView = () => { /* */ };

// Import only what you need
import { initializeProductCarousel } from './carousel.js';
```

**DON'T**:
```javascript
// 200KB monolith with all features
const initializeEverything = () => { /* */ };
```

🟡 **RECOMMENDED**: Defer non-critical scripts:
```html
<script src="tracking.js" defer></script>
<script type="module" src="critical.js"></script>
```

🟡 **RECOMMENDED**: Complex inline JS/CSS should be moved to separate files in `theme/assets/` to improve maintainability, caching, and readability.

### CSS Performance (RECOMMENDED)

🟡 **RECOMMENDED**: Inline critical CSS (above-the-fold). Load component styles async:

```liquid
<style>
  /* Critical hero styles */
  .hero { background: var(--color-background); }
</style>
<link rel="preload" as="style" href="{{ 'hero-extra.css' | asset_url }}">
<link rel="stylesheet" href="{{ 'hero-extra.css' | asset_url }}">
```

---

## Shopify-Specific Standards

### Metafields & Metaobjects (RECOMMENDED)

🟡 **RECOMMENDED**: Use metafields for extended product/collection data:

```liquid
{% if product.metafields.custom.hero_image %}
  {{ product.metafields.custom.hero_image | image_url: width: 1500 | image_tag }}
{% endif %}

{% if product.metafields.custom.feature_list.value %}
  {% for feature in product.metafields.custom.feature_list.value %}
    <li>{{ feature }}</li>
  {% endfor %}
{% endif %}
```

**Metafield Naming Convention**:
- **Namespace**: `custom` (for {{BRAND}} custom fields)
- **Key**: Descriptive, snake_case: `hero_image`, `sale_badge_text`, `feature_list`

### Dynamic Sources (RECOMMENDED)

🟡 **RECOMMENDED**: Support dynamic content sources in block settings:

```json
{
  "type": "product",
  "id": "featured_product",
  "label": "Featured Product"
}
```

This allows merchants to use dynamic sources (e.g., first product in collection, product by tag).

### App Block Compatibility (OPTIONAL)

🟢 **OPTIONAL**: If block can be used in app contexts, include:

```json
{
  "type": "product",
  "id": "product",
  "label": "Product"
}
```

Shopify apps can now inject your block into post-purchase flows, email, etc.

### Section Rendering API (OPTIONAL)

🟢 **OPTIONAL**: Use `{% render %}` instead of `{% include %}` to ensure predictable rendering in section rendering contexts.

---

## 🐛 Debugging & Developer Workflow

### Logging Convention (RECOMMENDED)

🟡 **RECOMMENDED**: Use structured console logging with namespace:

```javascript
const log = (message, data) => {
  if (window.DEBUG) {
    console.log(`[{{BRAND}}] ${message}`, data);
  }
};

// Usage
log('Product loaded', { id: product.id, title: product.title });
log('Cart updated', cart);
```

### Error Handling (REQUIRED)

🔴 **REQUIRED**: All async operations must have error handling:

**DO**:
```javascript
async function updateCart(variant) {
  try {
    const response = await fetch('/cart/add.js', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ items: [{ id: variant.id, quantity: 1 }] })
    });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const data = await response.json();
    log('Cart updated', data);
    return data;
  } catch (error) {
    console.error('[{{BRAND}}] Add to cart failed:', error);
    showErrorMessage('Failed to add item to cart. Please try again.');
  }
}
```

**DON'T**:
```javascript
const response = await fetch('/cart/add.js', { /* */ });
const data = await response.json(); // No error handling!
```

### Testing Strategy (RECOMMENDED)

🟡 **RECOMMENDED**: Verify locally before deployment:

```bash
# 1. Run linter
npm run lint

# 2. Start local dev server
npm run dev

# 3. Test in browser at different sizes (F12 → Device Toolbar)
# 4. Check Lighthouse (Chrome DevTools → Lighthouse)
# 5. Run accessibility audit (Chrome DevTools → Lighthouse → Accessibility)
# 6. Test keyboard navigation (Tab through page)
# 7. Check console for errors (F12 → Console)
```

### Backward Compatibility (RECOMMENDED)

🟡 **RECOMMENDED**: When modifying existing sections/blocks, maintain backward compatibility:

```liquid
{% comment %} Fallback for old setting names {% endcomment %}
{% assign image_height = block.settings.image_height | default: block.settings.height %}
{% assign show_title = block.settings.show_title | default: true %}
```

---

## 🔐 Security Checklist

🔴 **REQUIRED**: All code must follow these security rules:

- **User Input**: Always sanitize via Shopify filters (`| escape`, `| strip_html`)
- **XSS Prevention**: Never use `| raw` with user-generated content
- **External Scripts**: Only load from trusted Shopify CDNs or verified vendors
- **HTTPS**: All resources must load over HTTPS (Shopify enforces this)
- **CSRF Tokens**: Forms automatically include `{{ form | payment_terms }}`

**DO**:
```liquid
{{ product.description | strip_html | escape }}
```

**DON'T**:
```liquid
{{ user_comment | raw }}
```