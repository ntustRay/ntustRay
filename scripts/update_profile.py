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


def card(title, subtitle, rows, bars=False):
    body = []
    for index, (label, value) in enumerate(rows):
        y = 122 + index * 42
        body.append(f'<text x="28" y="{y}" font-size="19" fill="#EDF0EA">{escape(label)}</text>'
                    f'<text x="472" y="{y}" text-anchor="end" font-size="21" font-weight="600" fill="#EDF0EA">{escape(str(value))}</text>')
        if bars and str(value).endswith('%'):
            width = 155 * float(str(value)[:-1]) / 100
            body.append(f'<rect x="215" y="{y - 13}" width="155" height="10" rx="3" fill="#414A48"/>'
                        f'<rect x="215" y="{y - 13}" width="{width:.2f}" height="10" rx="3" fill="#AFC3A7"/>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 386" role="img" aria-label="{escape(title, quote=True)}">
  <rect x="1" y="1" width="498" height="384" rx="4" fill="#252A2B" stroke="#414A48" stroke-width="2"/>
  <g font-family="Arial, 'Noto Sans TC', 'Microsoft JhengHei', sans-serif">
    <text x="28" y="44" font-size="27" font-weight="700" fill="#EDF0EA">{escape(title)}</text>
    <text x="28" y="72" font-size="14" fill="#BEC8C3">{escape(subtitle)}</text>
    <path d="M28 89H472" stroke="#414A48"/>
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
    top = sorted(languages.items(), key=lambda item: item[1], reverse=True)[:5]
    language_rows = [(name, f'{size / total:.1%}') for name, size in top] if total else [('尚無原始碼資料', '—')]
    # Include the remainder explicitly; percentages use ALL language bytes.
    remainder = total - sum(size for _, size in top)
    if remainder:
        language_rows.append(('其他', f'{remainder / total:.1%}'))

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
    readme = section(readme, 'REPOS', '\n'.join(repo_lines) or '目前尚無公開專案。')
    date = datetime.now(ZoneInfo('Asia/Taipei')).strftime('%Y-%m-%d')
    readme = section(readme, 'UPDATED', f'<sub>更新於 {date} · [GitHub Actions 每日更新](https://github.com/{USER}/{USER}/actions/workflows/update-profile.yml).</sub>')
    stats = card('GitHub', '公開原創 Repository', [
        ('公開專案', len(own)),
        ('Stars', sum(r['stargazers_count'] for r in own)),
        ('Forks', sum(r['forks_count'] for r in own)),
    ])
    langs = card('語言分布', '公開原創專案的原始碼位元組占比', language_rows, bars=True)
    # Fetch and validate everything before modifying tracked output files.
    (ROOT / 'assets').mkdir(exist_ok=True)
    for filename, content in [('stats.svg', stats), ('top-langs.svg', langs)]:
        ET.fromstring(content)
        (ROOT / 'assets' / filename).write_text(content, encoding='utf-8')
    (ROOT / 'README.md').write_text(readme, encoding='utf-8')
    print(f'Updated profile: {len(own)} repositories, {len(items)} articles.')


if __name__ == '__main__':
    main()
