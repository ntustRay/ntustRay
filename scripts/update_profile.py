"""Refresh public profile data using only the Python standard library."""
import json
import os
import re
import urllib.request
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from html import escape
from pathlib import Path
from urllib.parse import quote, urlparse
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
USER = os.environ.get('GH_USER', 'ntustRay')
BLOG = 'https://ntustray.github.io/mr-blog/rss.xml'


def get(url):
    headers = {'User-Agent': 'ntustRay-profile-generator'}
    if urlparse(url).netloc == 'api.github.com':
        headers['Accept'] = 'application/vnd.github+json'
        if os.environ.get('GITHUB_TOKEN'):
            headers['Authorization'] = 'Bearer ' + os.environ['GITHUB_TOKEN']
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=30) as response:
        return response.read()


def api(path):
    return json.loads(get('https://api.github.com' + path))


def markdown(text):
    text = ' '.join(str(text).split())
    return re.sub(r'([\\`*_{}\[\]<>|])', r'\\\1', text)


def link(title, url):
    if urlparse(url).scheme not in {'https', 'http'}:
        raise ValueError('Invalid link URL')
    return f'[{markdown(title)}]({quote(url, safe=":/?=&%#@+~.-_")})'


def section(text, tag, body):
    start, end = f'<!-- {tag}:START -->', f'<!-- {tag}:END -->'
    if text.count(start) != 1 or text.count(end) != 1:
        raise ValueError(f'Expected exactly one {tag} section')
    head, rest = text.split(start)
    _, tail = rest.split(end)
    return f'{head}{start}\n{body}\n{end}{tail}'


def card(title, subtitle, rows):
    height = 130 + 44 * max(1, len(rows))
    body = []
    for index, (label, value) in enumerate(rows):
        y = 126 + index * 44
        body.append(f'<text x="28" y="{y}" font-size="18" fill="#c3d3e5">{escape(label)}</text>'
                    f'<text x="472" y="{y}" text-anchor="end" font-size="22" font-weight="700" fill="#7dd3fc">{escape(str(value))}</text>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 {height}" role="img" aria-label="{escape(title, quote=True)}">
  <rect width="500" height="{height}" rx="24" fill="#081426" stroke="#283a59"/>
  <g font-family="system-ui, sans-serif">
    <text x="28" y="42" font-size="26" font-weight="800" fill="#f7fbff">{escape(title)}</text>
    <text x="28" y="72" font-size="14" fill="#a7c0db">{escape(subtitle)}</text>
    <path d="M28 90H472" stroke="#22d3ee" stroke-width="2"/>
    {''.join(body)}
  </g>
</svg>
'''


def main():
    repos, page = [], 1
    while True:
        batch = api(f'/users/{USER}/repos?type=owner&per_page=100&page={page}')
        repos.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    # Never expose private repositories, even with a more privileged token.
    own = [r for r in repos if not r['private'] and not r['fork']]
    languages = {}
    with ThreadPoolExecutor(max_workers=6) as pool:
        for data in pool.map(lambda r: api(f"/repos/{r['full_name']}/languages"), own):
            for name, size in data.items():
                languages[name] = languages.get(name, 0) + size
    total = sum(languages.values())
    top = sorted(languages.items(), key=lambda item: item[1], reverse=True)[:6]
    language_rows = [(name, f'{size / total:.1%}') for name, size in top] if total else [('No source data', '—')]
    # Include the remainder explicitly; percentages use ALL language bytes.
    remainder = total - sum(size for _, size in top)
    if remainder:
        language_rows.append(('Other', f'{remainder / total:.1%}'))

    recent = sorted([r for r in own if not r['archived'] and r['name'].lower() != USER.lower()],
                    key=lambda r: r['pushed_at'] or '', reverse=True)[:5]
    repo_lines = []
    for r in recent:
        desc = markdown(r['description'] or '')
        desc = desc[:157] + '…' if len(desc) > 160 else desc
        repo_lines.append(f"- {link(r['name'], r['html_url'])}" + (f' — {desc}' if desc else '')
                          + f" <sub>{(r['pushed_at'] or '')[:10]}</sub>")

    items = ET.fromstring(get(BLOG)).findall('./channel/item')[:5]
    if not items:
        raise ValueError('Blog feed contains no articles; keeping existing files')
    blog_lines = [f"- {link(item.findtext('title'), item.findtext('link'))}" for item in items]

    readme = (ROOT / 'README.md').read_text(encoding='utf-8')
    readme = section(readme, 'BLOG', '\n'.join(blog_lines))
    readme = section(readme, 'REPOS', '\n'.join(repo_lines) or 'No public projects yet.')
    date = datetime.now(ZoneInfo('Asia/Taipei')).strftime('%Y-%m-%d')
    readme = section(readme, 'UPDATED', f'<sub>Updated {date} · Public repositories only · [Daily refresh](https://github.com/{USER}/{USER}/actions/workflows/update-profile.yml)</sub>')
    stats = card('GitHub stats', 'Public original repositories', [
        ('Repositories', len(own)),
        ('Stars earned', sum(r['stargazers_count'] for r in own)),
        ('Forks received', sum(r['forks_count'] for r in own)),
    ])
    langs = card('Top languages', 'Share of source bytes · public original repos', language_rows)
    # Fetch and validate everything before modifying tracked output files.
    (ROOT / 'assets').mkdir(exist_ok=True)
    for filename, content in [('stats.svg', stats), ('top-langs.svg', langs)]:
        ET.fromstring(content)
        (ROOT / 'assets' / filename).write_text(content, encoding='utf-8')
    (ROOT / 'README.md').write_text(readme, encoding='utf-8')
    print(f'Updated profile: {len(own)} repositories, {len(items)} articles.')


if __name__ == '__main__':
    main()
