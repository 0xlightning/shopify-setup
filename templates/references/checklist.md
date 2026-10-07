# Pre-Deployment Checklist & Quality Gates

> **Read this** before commit, before push, before requesting review. Sourced from the project `CLAUDE.md`

---

## 🧪 Testing & Validation

### Pre-Deployment Checklist (REQUIRED)

🔴 **REQUIRED**: All of the following MUST pass before merging:

- [ ] **Linting**: `npm run lint` returns 0 errors, 0 warnings
- [ ] **Live Preview**: `npm run dev` renders without console errors
- [ ] **Responsive**: Tested at 375px (mobile), 768px (tablet), 1440px (desktop)
- [ ] **Colors**: No hardcoded hex/rgb values; all use CSS variables
- [ ] **Images**: All have `alt` attributes; non-decorative images are descriptive
- [ ] **Forms**: Inputs have labels; validation errors display; submit works
- [ ] **Accessibility**: 
  - [ ] Tab navigation works
  - [ ] All buttons/links keyboard accessible
  - [ ] Focus indicators visible
  - [ ] No color-only indicators
  - [ ] ARIA attributes correct
- [ ] **Lighthouse** (Chrome DevTools):
  - [ ] Performance: 90+
  - [ ] Accessibility: 100
  - [ ] Best Practices: 90+
  - [ ] SEO: 90+
- [ ] **Cross-browser**: Chrome, Safari, Firefox (latest 2 versions each)
- [ ] **No console errors**: Check console for JS errors/warnings
- [ ] **Asset loading**: All images, CSS, JS load without 404s

### Testing Dimensions

🔴 **REQUIRED**: Test at these specific sizes:

| Device | Width | Use Case |
|--------|-------|----------|
| **Mobile** | 375px | iPhone SE / small phones |
| **Mobile** | 414px | iPhone 14 / standard phones |
| **Mobile** | 428px | iPhone 14 Pro / large phones |
| **Tablet** | 768px | iPad / standard tablet |
| **Tablet** | 820px | iPad Air / larger tablet |
| **Desktop** | 1024px | Minimum desktop width |
| **Desktop** | 1440px | Standard laptop |
| **Desktop** | 1920px | Full HD / larger screens |

---

## 📊 Success Metrics

Your code is production-ready when:

| Metric | Target | Verification |
|--------|--------|--------------|
| **Linting** | 0 errors | `npm run lint` |
| **Manual QA** | All checklist items pass | Pre-Deployment Checklist (above) — no automated test suite is configured |
| **Lighthouse Performance** | 90+ | Chrome DevTools |
| **Lighthouse Accessibility** | 100 | Chrome DevTools |
| **Responsive** | 375px–1920px | Manual testing |
| **Cross-browser** | Chrome, Safari, Firefox | Tested on latest 2 versions |
| **a11y** | WCAG 2.1 AA | axe DevTools audit |
| **Code Coverage** | Critical paths | Test reports |

---

## 🚨 Common Mistakes to Avoid

| Mistake | Why It Fails | Fix |
|---------|------------|-----|
| Hardcoded colors | Breaks theme customization | Use `var(--color-*)` |
| Deep Liquid nesting | Performance impact | Extract to snippets (max 3 levels) |
| No alt attributes | Accessibility fails | Add descriptive alt to all images |
| `{% include %}` | Scope pollution | Always use `{% render %}` |
| Skipped heading levels | SEO/accessibility | H1 → H2 → H3 (no gaps) |
| Unresponsive images | Layout shift (CLS) | Include srcset + aspect ratio |
| No error handling | Silent failures | Wrap async in try/catch |
| Focus management missing | Keyboard nav fails | Add `:focus-visible` CSS |
| Schema validation fails | Deployment blocked | Test in Shopify CLI before pushing |
| Monolithic sections | Unmaintainable | Split into section + snippets/blocks |

---

## 📤 Output Formatting & Communication

### Claude's Output Expectations (REQUIRED)

🔴 **REQUIRED**: When generating code, Claude MUST:

1. **Provide complete, working implementations** — No stubs or `// TODO` placeholders
2. **Include inline documentation** — Explain *why*, not *what*
3. **Bundle related files** — Don't ask to "fill in styles later"
4. **Show architectural decisions** — Briefly explain structure choices
5. **Avoid unnecessary verbosity** — Output code, not lengthy preambles

**DO**:
```
I'll add a new "testimonial-carousel" section with the following features:

**Architecture**:
- Section handles configuration via schema
- Snippet (testimonial-item.liquid) renders each testimonial with lazy-loaded image
- JavaScript (testimonial-carousel.js) initializes Swiper with accessibility hooks

**Files to create**:
1. /theme/sections/testimonial-carousel.liquid
2. /theme/snippets/testimonial-item.liquid
3. /theme/assets/testimonial-carousel.js
4. /theme/assets/testimonial-carousel.css

[Full code follows...]
```

**DON'T**:
```
I can create a testimonial carousel. The section will need:
- Schema to let merchants add testimonials
- CSS for styling
- JavaScript for carousel functionality
Would you like me to start with the HTML structure?
```

### Code Review Process (RECOMMENDED)

🟡 **RECOMMENDED**: When asked to review code, Claude should:

1. Check against `claude.md` + the relevant `references/` file
2. Flag 🔴 **REQUIRED** violations as blocking
3. Flag 🟡 **RECOMMENDED** issues as improvements
4. Provide corrected code snippets
5. Explain the rationale