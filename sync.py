#!/usr/bin/python3

from datetime import datetime, timezone
import github3
import os
import re
import sys
import yaml

def main():
    with open('config.yml') as fh:
        conf = yaml.safe_load(fh)

    token = os.getenv('GITHUB_TOKEN')
    assert token
    g = github3.login(token=token)

    groups = []
    for group in conf['groups']:
        repos = []
        groups.append({
            'name': group['name'],
            'repos': repos,
        })

        for desc in group['repos']:
            owner, name = desc.split('/')
            repo = g.repository(owner=owner, repository=name)

            try:
                release = repo.latest_release()
            except github3.exceptions.NotFoundError:
                print(
                    f"No releases (tags don't count): {desc}",
                    file=sys.stderr
                )
                continue
            delta = datetime.now(timezone.utc) - release.published_at

            compare = repo.compare_commits(
                release.tag_name, repo.default_branch
            )
            nontrivial_commits = len([
                c for c in compare.commits
                # not merge commit
                if len(c.parents) == 1 and
                # not by Dependabot
                (c.author is None or c.author.login != 'dependabot[bot]')
            ])

            repos.append({
                'repo': desc,
                'url': repo.html_url,
                'release': re.sub('^[a-z-]+', '', release.tag_name),
                'release_url': release.html_url,
                'release_date': release.published_at.strftime("%Y-%m-%d"),
                'release_days': int(delta.total_seconds() / 86400),
                'compare_commits': compare.ahead_by,
                'compare_nontrivial': nontrivial_commits,
                'compare_url': compare.html_url,
            })

    with open('docs/_data/repos.yml', 'w') as fh:
        yaml.dump({
            'groups': groups,
            'updated': datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
            'green_thresh': conf['thresholds']['green'],
            'yellow_thresh': conf['thresholds']['yellow'],
        }, fh)

if __name__ == '__main__':
    main()
