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
