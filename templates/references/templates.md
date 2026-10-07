> [!WARNING]
> Generic starter standards. CSS variable names below (`--color-*`, `--spacing-*`, `--font-*-family`) come from another theme (Dawn-style) and **will differ** in your base theme. Verify names in the theme's styles-variables snippet before using; theme source and `theme/AGENTS.md` win on conflict.

# Production-Ready Templates

> **Read this** when creating a new block, section, JS module, or CSS component. Copy the relevant template and adapt. Sourced from the project `CLAUDE.md`

---

## New Block Template (Production-Ready)

```liquid
{%- liquid
  assign block_id = block.id
  assign block_settings = block.settings
  assign product = closest.product
-%}

<div
  class="{{PREFIX}}-testimonial-block"
  data-block-id="{{PREFIX}}-{{ block_id }}"
  {{ block.shopify_attributes }}
>
  <blockquote class="{{PREFIX}}-testimonial-block__quote">
    <p>{{ block_settings.testimonial_text | escape }}</p>
  </blockquote>

  <div class="{{PREFIX}}-testimonial-block__author">
    {% if block_settings.author_image %}
      {{ block_settings.author_image | image_url: width: 100 | image_tag:
        alt: block_settings.author_name,
        class: '{{PREFIX}}-testimonial-block__author-image'
      }}
    {% endif %}
    <div class="{{PREFIX}}-testimonial-block__author-info">
      <p class="{{PREFIX}}-testimonial-block__author-name">
        {{ block_settings.author_name | escape }}
      </p>
      <p class="{{PREFIX}}-testimonial-block__author-title">
        {{ block_settings.author_title | escape }}
      </p>
    </div>
  </div>
</div>

{% stylesheet %}
  .{{PREFIX}}-testimonial-block {
    padding: var(--spacing-md);
    background: var(--color-background);
    border-radius: 8px;
  }

  .{{PREFIX}}-testimonial-block__quote {
    font-size: var(--font-size-lg);
    font-style: italic;
    margin-bottom: var(--spacing-md);
    color: var(--color-foreground);
  }

  .{{PREFIX}}-testimonial-block__author {
    display: flex;
    align-items: center;
    gap: var(--spacing-sm);
  }

  .{{PREFIX}}-testimonial-block__author-image {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    object-fit: cover;
  }

  @media (max-width: 767px) {
    .{{PREFIX}}-testimonial-block {
      padding: var(--spacing-sm);
    }
  }
{% endstylesheet %}

{% schema %}
{
  "name": "Testimonial",
  "settings": [
    {
      "type": "textarea",
      "id": "testimonial_text",
      "label": "Testimonial Text",
      "default": "This product changed my life!"
    },
    {
      "type": "text",
      "id": "author_name",
      "label": "Author Name",
      "default": "Jane Doe"
    },
    {
      "type": "text",
      "id": "author_title",
      "label": "Author Title",
      "default": "Verified Buyer"
    },
    {
      "type": "image_picker",
      "id": "author_image",
      "label": "Author Photo"
    }
  ],
  "presets": [
    {
      "name": "Testimonial"
    }
  ]
}
{% endschema %}
```

---

## JavaScript Module (Production-Ready)

```javascript
/**
 * Testimonial Carousel
 * Initializes a carousel with keyboard navigation and accessibility
 */

export const initializeTestimonialCarousel = () => {
  const carousels = document.querySelectorAll('[data-carousel-type="testimonial"]');

  carousels.forEach((carousel) => {
    const items = carousel.querySelectorAll('[data-carousel-item]');
    const prevBtn = carousel.querySelector('[data-carousel-prev]');
    const nextBtn = carousel.querySelector('[data-carousel-next]');
    const container = carousel.querySelector('[data-carousel-container]');

    if (!items.length) return;

    let currentIndex = 0;

    const updateCarousel = () => {
      items.forEach((item, idx) => {
        item.setAttribute('aria-hidden', idx !== currentIndex);
        item.classList.toggle('active', idx === currentIndex);
      });

      prevBtn.disabled = currentIndex === 0;
      nextBtn.disabled = currentIndex === items.length - 1;

      container.setAttribute('aria-label', `Slide ${currentIndex + 1} of ${items.length}`);
    };

    const next = () => {
      if (currentIndex < items.length - 1) {
        currentIndex++;
        updateCarousel();
      }
    };

    const prev = () => {
      if (currentIndex > 0) {
        currentIndex--;
        updateCarousel();
      }
    };

    prevBtn?.addEventListener('click', next);
    nextBtn?.addEventListener('click', prev);

    // Keyboard support
    container?.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowRight') next();
      if (e.key === 'ArrowLeft') prev();
    });

    updateCarousel();
  });
};

// Auto-initialize on page load
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initializeTestimonialCarousel);
} else {
  initializeTestimonialCarousel();
}
```

---

## CSS Architecture (Production-Ready)

```css
/* Testimonial Carousel - Mobile First */

.{{PREFIX}}-carousel {
  --carousel-gap: var(--spacing-md);
}

.{{PREFIX}}-carousel__container {
  display: flex;
  gap: var(--carousel-gap));
  overflow-x: auto;
  scroll-behavior: smooth;
  scroll-snap-type: x mandatory;
}

.{{PREFIX}}-carousel__item {
  flex: 0 0 100%;
  scroll-snap-align: start;
  padding: var(--spacing-sm);
  background: var(--color-background);
  border-radius: 8px;
}

.{{PREFIX}}-carousel__controls {
  display: flex;
  gap: var(--spacing-sm);
  margin-top: var(--spacing-md);
  justify-content: center;
}

.{{PREFIX}}-carousel__button {
  padding: var(--spacing-sm) var(--spacing-md);
  border: 1px solid var(--color-border);
  background: var(--color-background);
  color: var(--color-foreground);
  border-radius: 4px;
  cursor: pointer;
  font-size: var(--font-size-sm);
  transition: background-color 0.2s ease;
}

.{{PREFIX}}-carousel__button:hover:not(:disabled) {
  background-color: var(--color-accent);
  color: var(--color-background);
}

.{{PREFIX}}-carousel__button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.{{PREFIX}}-carousel__button:focus-visible {
  outline: 2px solid var(--color-accent);
  outline-offset: 2px;
}

/* Tablet */
@media (min-width: 768px) {
  .{{PREFIX}}-carousel__item {
    flex: 0 0 calc(50% - var(--carousel-gap) / 2);
  }
}

/* Desktop */
@media (min-width: 1024px) {
  .{{PREFIX}}-carousel__item {
    flex: 0 0 calc(33.333% - var(--carousel-gap) * 2 / 3);
  }
}

/* Reduced Motion */
@media (prefers-reduced-motion: reduce) {
  .{{PREFIX}}-carousel__container {
    scroll-behavior: auto;
  }

  .{{PREFIX}}-carousel__button {
    transition: none;
  }
}
```