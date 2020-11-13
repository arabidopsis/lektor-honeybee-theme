# honeybee

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
your config file.

```ini
[theme_settings]
# sitemap.xml changefreq
changefreq = monthly
# default is no theme
theme = sunset
# is this theme a dark theme i.e. light text on dark background
is_dark_theme = false
# bootstrap = {some bootstrap.css}
twitter = twitter handle for site
facebook = facebook page for site
```

The theme can be one of: `mickie`, `hollar`, `sunset`,`wandoo`, `graymor`, `electro`, `lymcha`, `deeply`, `minco`, `skeeblu`, `preptor` or `monotone`.
See [here](https://themesguide.github.io/top-hat/dist/) or, build your own
at [https://themestr.app/](https://themestr.app/) or see [http://themes.guide/](http://themes.guide/#freebies).

If you have built your own place it in `/assets/static/css/{mytheme.css}` and
add a `bootstrap = mytheme.css` to the the `[theme_settings]`. (Don't bother to set `theme` in
this case)
