# honeybee theme

A lektor theme for [Honey Bee Health](https://honeybeehealthresearch.org/)
Content is currently [Here](https://github.com/arabidopsis/honeybeehealthresearch.org)

Create a directory `themes` in the `honebeehealthresearch.org` directory and link this repo:

```bash
cd honeybeehealthresearch.org
mkdir themes
cd themes
ln -s /path/to/this/repo .
```

This theme requires a [Lektor plugin](https://github.com/arabidopsis/lektor-shortcodes).

Add to the `[packages]` section of your lektorproject configuration file

```ini
[packages]
https://github.com/arabidopsis/lektor-shortcodes/archive/main.tar.gz = ""
```

This still uses pip so the versioning info is not required.

OR you can download the repository into your packages directory

```bash
git clone https://github.com/arabidopsis/lektor-shortcodes.git $(lektor project-info --tree)/packages/
lektor plugins list # list will install any newly found plugins
```

This theme uses **bootstrap5** and has no "internal" dependency
on jQuery. Some shortcodes require some vanilla javascript to
work. In paticular the `contact-form` shortcode uses some vanilla javascript
to do form validation. Also  the `twitter` and `omap` shortcodes will
install their javascript libraries. If you have set `ua_google` then
this will *also* add its library.

## 404

To add a 404 page just add to a `content/404.html/contents.lr` file:

```ini
_model: none
---
_template: 404.html
```

## theme_settings

This theme understands a few
values in the `[theme_settings]` of
your project file.

```ini
[theme_settings]
# google analytics
ua_google = UA-XXXXX-Y
# text to overlay header
# frontispiece = 'text for header'
# sitemap.xml changefreq
changefreq = monthly
# default is no theme
theme = sunset
# is this theme a dark theme? i.e. light text on dark background
is_dark_theme = false
# bootstrap = {some-bootstrap.css}
```

The theme can be one of: `mickie`, `hollar`, `sunset`,`wandoo`, `graymor`, `electro`, `lymcha`, `deeply`, `minco`, `skeeblu`, `preptor` or `monotone`.
See [here](https://themesguide.github.io/top-hat/dist/) or, build your own
at [https://themestr.app/](https://themestr.app/) or see [http://themes.guide/](http://themes.guide/#freebies).

If you have built your own place it in `/assets/static/css/{mytheme.css}` and
add a `bootstrap = mytheme.css` to the the `[theme_settings]`. (Don't bother to set `theme` in this case)

## `/extras/globals` page

The page `/extras/globals` defines some site wide parameters including
twitter handles, facebook handles, highlight color etc.

## classes used in this theme

These are the "extra" classes known to this theme (apart from
bootstrap5 classes!). Currently only `hl`, `admonition-*`, `filter-x?bw`,
`social-logos` and `feature` have any css styles attached to them.

Also the class `dark` or `light` is attached to `body` based on
`config.THEME_SETTINGS.is_dark_theme`

* `content` wraps the entire document
* `hl` highlight class for h1,h2 etc.
* `markdown` wraps all markdown blocks
* `publication-list` wraps list of publications
  * `publication` wrapped by `publication-list` and wraps
    * `pub-date`, `pub-doi` , `pub-date`, `pub-pubmed`, `pub-title`, 
      `pub-journal`, `pub-authors` and `pub-ref`
* `social-logos` followed by `follow` wraps any social logos links
* `parallax-window` for parallax blocks
* `full-news-item` wraps a full news item card
* `sitemap` wraps sitemap links
* `admonition` and `admonition-note`, `admonition-tip`, `admonition-warning`, `admonition-info` for admonition "shortcode".
* `feature` for feature shortcode `{{feature beer}}`
* `logo` for logo overlaying header
* `vignettes` wraps vignette list marked by `vignette`
* `filter-bw` and `filter-xbw` grayscale image hovers
