---
layout: default
title: Latest CoreOS upstream releases
---

# Latest CoreOS upstream releases

{% for group in site.data.repos.groups %}
### {{ group.name }}

| Repository | Current release | Release date | Commits since release (non-trivial / all) |
| --- | --- | --- | --- |
{% for repo in group.repos %}| [{{ repo.repo }}]({{ repo.url }}) | [{{ repo.release }}]({{ repo.release_url }}) | {% if repo.release_days < site.data.repos.green_thresh %}🟢{% elsif repo.release_days < site.data.repos.yellow_thresh %}🟨{% else %}🛑{% endif %} {{ repo.release_date }} ({{ repo.release_days }} days ago) | {{ repo.compare_nontrivial }} / [{{ repo.compare_commits }}]({{ repo.compare_url }}) |
{% endfor %}
{% endfor %}

Last updated: {{ site.data.repos.updated }}
