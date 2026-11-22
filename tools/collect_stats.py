# Appends one row of public GitHub stats to stats.csv and prints any newly crossed star milestone.
# Run by .github/workflows/stats.yml. Copyright (c) 2026 nudarofficial. MIT License, see LICENSE.
# Usage: python3 tools/collect_stats.py OWNER/REPO path/to/stats.csv
import csv, datetime, json, os, sys, urllib.request
from pathlib import Path

repo, path = sys.argv[1], Path(sys.argv[2])
MILESTONES = [1, 5, 10, 25, 50, 100, 250, 500, 1000, 2500, 5000]
headers = {'Accept': 'application/vnd.github+json', 'User-Agent': 'humanize-stats'}
if os.environ.get('GITHUB_TOKEN'):
    headers['Authorization'] = 'Bearer ' + os.environ['GITHUB_TOKEN']

def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=30) as r:
        return json.load(r)

info = get(f'https://api.github.com/repos/{repo}')
releases = get(f'https://api.github.com/repos/{repo}/releases?per_page=100')
downloads = sum(a.get('download_count', 0) for r in releases for a in r.get('assets', []))
row = {'date': datetime.date.today().isoformat(), 'stars': info['stargazers_count'], 'forks': info['forks_count'],
       'watchers': info['subscribers_count'], 'open_issues': info['open_issues_count'], 'zip_downloads': downloads}
try:  # views and clones need a token with push access; skip quietly without one
    traffic = get(f'https://api.github.com/repos/{repo}/traffic/views')
    clones = get(f'https://api.github.com/repos/{repo}/traffic/clones')
    row['views_14d'], row['clones_14d'] = traffic.get('count', ''), clones.get('count', '')
except Exception:
    row['views_14d'] = row['clones_14d'] = ''

fields = ['date', 'stars', 'forks', 'watchers', 'open_issues', 'zip_downloads', 'views_14d', 'clones_14d']
rows = list(csv.DictReader(path.open())) if path.exists() else []
previous = int(rows[-1]['stars']) if rows else 0
rows = [r for r in rows if r['date'] != row['date']] + [row]
with path.open('w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)
crossed = [m for m in MILESTONES if previous < m <= row['stars']]
print(json.dumps(row))
if crossed and os.environ.get('GITHUB_OUTPUT'):
    with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
        f.write(f'milestone={crossed[-1]}\nstars={row["stars"]}\n')
