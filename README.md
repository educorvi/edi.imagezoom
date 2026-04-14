# edi.imagezoom

> **Disclaimer:** This README was generated with the assistance of AI.

A Plone add-on that integrates the [js-image-zoom](https://github.com/malaman/js-image-zoom) JavaScript library to provide on-hover or on-click image zooming for images embedded in rich-text (HTML) content fields. When activated on a content item, every `<img>` tag found in the item's text body gains a "zoom" link beneath it. Clicking the link opens a Bootstrap modal that displays the full-size version of the image.

---

## Table of Contents

- [Features](#features)
- [Requirements & External Dependencies](#requirements--external-dependencies)
- [Installation](#installation)
- [What This Package Includes](#what-this-package-includes)
  - [Behavior: `IImageZoomMarker`](#behavior-iimagezoommarker)
  - [Viewlet: `imagezoom-script-viewlet`](#viewlet-imagezoom-script-viewlet)
  - [Browser Layer: `IEdiImagezoomLayer`](#browser-layer-iediimagezoomplayer)
  - [Static Resources](#static-resources)
- [Configuration](#configuration)
  - [Enabling the Behavior on a Content Type](#enabling-the-behavior-on-a-content-type)
  - [Activating Zoom on a Content Item](#activating-zoom-on-a-content-item)
- [How It Works](#how-it-works)
- [Supported Content Types](#supported-content-types)
- [Translations / Localization](#translations--localization)
- [Contribute](#contribute)
- [Support](#support)
- [License](#license)

---

## Features

- **Behavior** (`IImageZoomMarker`) that adds a per-item toggle to enable/disable image zooming.
- **Viewlet** that automatically scans the rich-text body of a content item for `<img>` tags and injects:
  - A "zoom" anchor below each image that triggers a Bootstrap modal.
  - Bootstrap modals containing the full-size image (fetched via Plone's `@@download/image` traversal view).
  - Inline initialization of the `js-image-zoom` library for any element with the CSS class `edi-zoom-image`.

---

## Requirements & External Dependencies

### Python / Plone

| Dependency | Purpose |
|---|---|
| `Plone` ≥ 5.2 | Tested Plone version |
| `plone.api` ≥ 1.8.4 | Plone API utilities |
| `plone.app.dexterity` | Dexterity content-type framework (behavior registration) |
| `plone.restapi` | Declared as a dependency; ensures REST API support is available for Plone installations that use it |
| `z3c.jbot` | Template override mechanism (overrides directory) |
| `beautifulsoup4` (`bs4`) | Parses the rich-text HTML to find `<img>` tags |
| Python ≥ 3.8 | Minimum Python version |

### Front-end

| Dependency | How it is provided |
|---|---|
| **jQuery** | Must be present in the Plone theme (standard in most Plone 5 Bootstrap-based themes) |
| **Bootstrap 4/5** (modals + utility classes) | Must be present in the active Plone theme. The viewlet uses `data-toggle="modal"`, `data-target`, `modal-xl`, `modal-dialog`, `img-fluid`, `float-right`, etc. |
| **Bootstrap Icons** (`bi bi-binoculars`) | Must be included in the theme to display the binoculars icon on the zoom link |
| **js-image-zoom** | Bundled as a static resource at `++resource++edi.imagezoom/js-image-zoom.js` — no extra installation needed |

> **Important:** This add-on is designed to work with a Bootstrap-based Plone theme that includes Bootstrap modals and Bootstrap Icons. It will not work correctly with the default Plone 5 Barceloneta theme without additional front-end setup.

---

## Installation

1. Add `edi.imagezoom` to your buildout eggs:

   ```ini
   [buildout]
   ...
   eggs =
       ...
       edi.imagezoom
   ```

2. Run `bin/buildout`.

3. Start your Plone instance and navigate to **Site Setup → Add-ons**.

4. Install **edi.imagezoom**.

Alternatively, install via pip:

```bash
pip install edi.imagezoom
```

---

## What This Package Includes

### Behavior: `IImageZoomMarker`

**ZCML name:** `edi.imagezoom.behaviors.image_zoom.IImageZoomMarker`
**Title (German):** *ImageZoom für Haupttexte*
**Description (German):** *Erlaubt die automatische Vergrößerung von Bildern im Haupttext.*

This Dexterity behavior adds a single boolean field to the content type's **Settings** fieldset:

| Field | Type | Default | Label |
|---|---|---|---|
| `zoommarker` | `Bool` | `False` | *Bilder vergrößern aktivieren* ("Enable image zoom") |

When `zoommarker` is `True` on a content item, the viewlet will inject zoom links and modals for all images found in the item's rich-text body.

---

### Viewlet: `imagezoom-script-viewlet`

**Name:** `imagezoom-script-viewlet`
**Manager:** `plone.app.layout.viewlets.interfaces.IBelowContent`
**Registered for:** all content (`for="*"`)
**Permission:** `zope2.View`
**Template:** `imagezoom-script-viewlet.pt`

The viewlet renders below the main content area and does the following:

1. **Always** includes and initializes the `js-image-zoom` library for any element with the CSS class `edi-zoom-image` (using `options2`: `fillContainer: true`, `zoomWidth: 200`, horizontal offset 10).
2. **When `zoommarker` is `True`** on the current context:
   - Parses the rich-text HTML with BeautifulSoup to collect all `<img>` tags.
   - For each image, resolves the full-size image URL by stripping Plone image scale suffixes (`large`, `preview`, `mini`, `thumb`, `tile`, `icon`, `listing`) and replacing `@@images` with `@@download/image`.
   - Injects a JavaScript block that appends a Bootstrap modal trigger link (`<a data-toggle="modal" …>`) after each `.image-richtext` image.
   - Renders a Bootstrap modal `<div>` for each discovered image, using the image's `title` and `alt` attributes and linking to the full-resolution download URL.

**Image ID resolution:** The viewlet reads the image UID from the `data-val` HTML attribute on the `<img>` tag if present; otherwise it falls back to parsing the UID from the image `src` URL. Modal IDs are prefixed with `edi` to avoid conflicts.

---

### Browser Layer: `IEdiImagezoomLayer`

**Interface:** `edi.imagezoom.interfaces.IEdiImagezoomLayer`

A standard Plone browser layer registered via `browserlayer.xml`. All views and resources provided by this add-on are scoped to this layer, which is active only when the add-on is installed.

---

### Static Resources

Registered under the resource name `edi.imagezoom`:

| File | Description |
|---|---|
| `++resource++edi.imagezoom/js-image-zoom.js` | The bundled [js-image-zoom](https://github.com/malaman/js-image-zoom) JavaScript library |

---

## Configuration

### Enabling the Behavior on a Content Type

The zoom behavior must be added to any Dexterity content type you want to support image zooming on.

**Via the Plone UI:**

1. Go to **Site Setup → Dexterity Content Types**.
2. Select the content type (e.g. *Page*, *Document*, or a custom type).
3. Open the **Behaviors** tab.
4. Enable **ImageZoom für Haupttexte** (`edi.imagezoom.behaviors.image_zoom.IImageZoomMarker`).
5. Save.

**Via Generic Setup (FTP/filesystem profile):**

In your site policy package's `profiles/default/types/<TypeName>.xml`, add the behavior:

```xml
<property name="behaviors" purge="false">
  <element value="edi.imagezoom.behaviors.image_zoom.IImageZoomMarker" />
</property>
```

---

### Activating Zoom on a Content Item

Once the behavior is assigned to a content type:

1. Open the content item in edit mode.
2. Navigate to the **Settings** tab (or fieldset).
3. Enable the checkbox **Bilder vergrößern aktivieren** (*Enable image zoom*).
4. Save.

Images embedded in the item's rich-text body will now have zoom links injected when the page is viewed.

---

## How It Works

```
Content item (with zoommarker=True)
  │
  └─► IBelowContent viewlet renders
        │
        ├─► Includes js-image-zoom.js
        ├─► JS: adds zoom trigger links after each .image-richtext img
        │         (reads UID from data-val attr or src URL)
        └─► HTML: Bootstrap modal <div> per image
                    └─► Full-size image via @@download/image
```

1. A visitor loads a page where the content item has `zoommarker = True`.
2. The `imagezoom-script-viewlet` renders below the content.
3. JavaScript (jQuery) scans the DOM for `img.image-richtext` and `figure.image-richtext > img` elements and appends a "vergrößern" (zoom) link after each one.
4. Clicking the link opens a Bootstrap modal showing the full-size image (loaded from `@@download/image` instead of the default scaled URL).

---

## Supported Content Types

The viewlet inspects:

- `self.context.text` — the standard `IRichText` field available on Plone's default *Document* (`plone.app.contenttypes`) and most custom Dexterity types.

Any Dexterity content type that has a `text` rich-text field and has the `IImageZoomMarker` behavior assigned will work out of the box. The viewlet can be extended to support additional rich-text fields on custom content types.

---

## Translations / Localization

Currently, the package UI labels are available in **German only**. The translation catalog is located in `src/edi/imagezoom/locales/`.

---

## Contribute

- **Issue Tracker:** https://github.com/educorvi/edi.imagezoom/issues
- **Source Code:** https://github.com/educorvi/edi.imagezoom

---

## Support

lars.walther@educorvi.de

---

## License

The project is licensed under the **GNU General Public License v2 (GPLv2)**.
