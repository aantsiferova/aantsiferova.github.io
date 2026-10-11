# Anastasia Antsiferova — personal website

Source of [aantsiferova.github.io](https://aantsiferova.github.io), built with [Jekyll](https://jekyllrb.com/) and the [al-folio](https://github.com/alshedivat/al-folio) theme.

## Where things live

- `_pages/about.md` — home page (bio, affiliations)
- `_bibliography/papers.bib` — publications (`abbr` = venue badge, `selected = {true}` = shown on the home page)
- `_projects/` — research projects; papers are linked with `{% cite key %}`, card stats are computed by `_plugins/project-stats.rb`
- `_news/` — news items (`inline: true` for short items without a separate page)
- `_data/cv.yml`, `_data/socials.yml` — CV and contact links

## Run locally

```bash
docker compose up
# or
bundle install && bundle exec jekyll serve
```

See [INSTALL.md](INSTALL.md) and [CUSTOMIZE.md](CUSTOMIZE.md) for the theme documentation.
