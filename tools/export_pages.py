#!/usr/bin/env python3
"""Snapshot only the public Peace Django pages. No login, DB or POST requests."""
import argparse
import hashlib
import json
import re
import shutil
from collections import deque
from pathlib import Path
from urllib.parse import parse_qs, unquote, urljoin, urlsplit
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

LANGUAGES = ('zh-hant', 'zh-hans', 'en')
PAGES = {'': '/', 'about': '/about', 'environments': '/environments/environments',
         'admission': '/informations/informations', 'guideline': '/informations/guideline',
         'news': '/news/', 'contacts': '/contacts/contacts/'}
ALIASES = {path.rstrip('/'): key for key, path in PAGES.items()}
ALIASES.update({'/environments': 'environments', '/informations': 'admission', '/contacts': 'contacts'})
ASSET_SUFFIXES = {'.png', '.jpg', '.jpeg', '.webp', '.gif', '.svg', '.ico', '.pdf'}


def snapshot(source, output, base_path, asset_root, max_pages=100):
    source = source.rstrip('/')
    origin = urlsplit(source)
    if origin.scheme not in ('http', 'https') or not origin.netloc or origin.path:
        raise ValueError('--source must be a site origin, such as https://peace-beta-sandy.vercel.app')
    output = output.resolve()
    # Never clear an existing folder; use a new build directory instead.
    if output.exists():
        raise ValueError(f'Output already exists: {output}. Choose a new --output directory.')
    output.mkdir(parents=True)
    prefix = '/' + base_path.strip('/') if base_path.strip('/') else ''
    if '..' in prefix or not re.fullmatch(r'(?:/[A-Za-z0-9_.-]+)*', prefix):
        raise ValueError('Invalid --base-path')
    copied_static = output / 'static'
    if asset_root.is_dir():
        shutil.copytree(asset_root, copied_static, ignore=shutil.ignore_patterns('__pycache__', '.DS_Store'))
    else:
        raise ValueError(f'Cannot find public static assets: {asset_root}')
    cache = {}
    warnings = []

    def read(url, lang=None):
        headers = {'User-Agent': 'Peace-Public-Pages-Exporter/1.0'}
        if lang:
            headers['Cookie'] = 'django_language=' + lang
        with urlopen(Request(url, headers=headers), timeout=15) as response:
            final = urlsplit(response.geturl())
            if lang and final.netloc != origin.netloc:
                raise ValueError('Public HTML redirected to another host; check --source')
            return response.read()

    def page_url(lang, key):
        return prefix + '/' + lang + '/' + (key.strip('/') + '/' if key else '')

    def key_for(url):
        bits = urlsplit(url)
        if bits.netloc != origin.netloc:
            return None
        path = bits.path.rstrip('/')
        query = parse_qs(bits.query)
        if path in ALIASES:
            key = ALIASES[path]
            if key == 'news' and 'page' in query:
                page = query['page'][0]
                if not page.isdigit() or int(page) < 1:
                    return None
                return 'news' if page == '1' else 'news/page/' + str(int(page))
            return key if not bits.query else None
        match = re.fullmatch(r'/news/(\d+)', path)
        return 'news/' + match[1] if match and not bits.query else None

    def asset(raw, current, required=False):
        if not raw or raw.startswith(('data:', '#', 'mailto:', 'tel:')):
            return raw
        url = urljoin(current, raw)
        bits = urlsplit(url)
        if bits.scheme not in ('http', 'https'):
            return raw
        is_static = bits.netloc == origin.netloc and bits.path.startswith('/static/')
        # Third-party CSS/scripts keep their original public CDN URLs.
        if not is_static and Path(bits.path).suffix.lower() not in ASSET_SUFFIXES:
            return url
        if url in cache:
            return cache[url]
        if is_static:
            relative = Path('static') / unquote(bits.path.removeprefix('/static/'))
            if '..' in relative.parts:
                raise ValueError('Invalid static asset path')
        else:
            suffix = Path(bits.path).suffix.lower()
            relative = Path('assets/media') / (hashlib.sha256(url.encode()).hexdigest()[:20] + suffix)
        destination = output / relative
        if is_static and destination.is_file():
            result = prefix + '/' + relative.as_posix()
            cache[url] = result
            return result
        try:
            payload = read(url)
        except Exception as exc:
            if required:
                raise RuntimeError(f'Cannot fetch required asset: {url}') from exc
            warnings.append('Unavailable public image/file: ' + url)
            return url
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(payload)
        result = prefix + '/' + relative.as_posix()
        cache[url] = result
        return result

    total = 0
    records = []
    for lang in LANGUAGES:
        queue = deque(PAGES.items())
        seen = set()
        while queue:
            key, path = queue.popleft()
            if key in seen:
                continue
            if len(seen) >= max_pages:
                raise ValueError('Too many public pages; increase --max-pages after checking the site.')
            current = source + path
            soup = BeautifulSoup(read(current, lang), 'html.parser')
            if not soup.html or soup.html.get('lang') != lang:
                raise ValueError(f'Wrong language for {path}: expected {lang}; check Vercel deployment.')
            form = soup.select_one('.language-switcher')
            if not form or not form.select_one('.language-options'):
                raise ValueError('Expected current Peace language control is missing.')
            seen.add(key)
            # Discover only published news links and pagination from public news lists.
            if key == 'news' or key.startswith('news/page/'):
                for link in soup.find_all('a', href=True):
                    url = urljoin(current, link['href'])
                    found = key_for(url)
                    if found and found.startswith('news/') and found not in seen:
                        bits = urlsplit(url)
                        queue.append((found, bits.path + ('?' + bits.query if bits.query else '')))
            for token in soup.select('input[name="csrfmiddlewaretoken"]'):
                token.decompose()
            form['action'] = '#'
            form['data-static-languages'] = json.dumps({value: page_url(value, key) for value in LANGUAGES})
            for other in soup.find_all('form'):
                if other is form:
                    continue
                other['data-live-url'] = urljoin(current, other.get('action') or current)
                other['action'] = other['data-live-url']
                note = soup.new_tag('p')
                note['style'] = 'font-size:14px;line-height:1.6'
                note.string = {'zh-hant':'展示版：提交會前往正式網站；資料需在正式網站重新填寫。',
                               'zh-hans':'展示版：提交会前往正式网站；资料需在正式网站重新填写。',
                               'en':'Demo: submitting opens the live website. Enter your details on the live website.'}[lang]
                other.insert(0, note)
            for tag in soup.find_all(['img', 'script', 'link', 'source', 'video']):
                for attr in ('src', 'poster'):
                    if tag.has_attr(attr):
                        tag[attr] = asset(tag[attr], current, required=tag.name == 'script')
                if tag.name == 'link' and tag.has_attr('href'):
                    tag['href'] = asset(tag['href'], current, required='stylesheet' in tag.get('rel', []))
                if tag.has_attr('srcset'):
                    entries = []
                    for entry in tag['srcset'].split(','):
                        parts = entry.strip().split()
                        if parts:
                            entries.append(' '.join([asset(parts[0], current)] + parts[1:]))
                    tag['srcset'] = ', '.join(entries)
            for link in soup.find_all('a', href=True):
                raw = link['href']
                if raw.startswith(('#', 'mailto:', 'tel:', 'javascript:')):
                    continue
                url = urljoin(current, raw)
                bits = urlsplit(url)
                found = key_for(url)
                if found is not None:
                    link['href'] = page_url(lang, found) + ('#' + bits.fragment if bits.fragment else '')
                elif bits.netloc == origin.netloc:
                    link['href'] = asset(raw, current) if Path(bits.path).suffix.lower() in ASSET_SUFFIXES else url
            extra = soup.new_tag('script', src=prefix + '/static/js/pages-demo.js', defer=True)
            soup.head.append(extra)
            for script in soup.find_all('script', src=True):
                if 'language-ui.js' in script['src']:
                    script['src'] = prefix + '/static/js/pages-language-ui.js'
            destination = output / lang / key / 'index.html'
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(str(soup), encoding='utf-8')
            records.append({'language': lang, 'path': path, 'static': page_url(lang, key)})
            total += 1
        print(f'{lang}: {len(seen)} public pages', flush=True)
    # Reuse the existing control, navbar sizing and Safari dropdown handling.
    language_source = (copied_static / 'js/language-ui.js').read_text()
    marker = "  select.addEventListener('change', async function () {"
    if marker not in language_source:
        raise ValueError('Unsupported language-ui.js; do not publish this incomplete export.')
    language_script = language_source.split(marker, 1)[0] + '''  select.addEventListener('change', function () {
    const destinations = JSON.parse(form.dataset.staticLanguages);
    window.location.assign(destinations[select.value] + window.location.hash);
  });
})();
'''
    (copied_static / 'js/pages-language-ui.js').write_text(language_script)
    (copied_static / 'js/pages-demo.js').write_text('''document.addEventListener('submit', function(event) {
  const form = event.target;
  if (!form.dataset.liveUrl) return;
  event.preventDefault();
  event.stopImmediatePropagation();
  const target = new URL(form.dataset.liveUrl);
  if ((form.method || 'get').toLowerCase() === 'get') {
    for (const [key, value] of new FormData(form)) if (typeof value === 'string') target.searchParams.set(key, value);
  }
  window.location.assign(target.href);
}, true);
''')
    home = page_url('zh-hant', '')
    (output / 'index.html').write_text(f'<!doctype html><html lang="zh-hant"><meta charset="utf-8"><meta http-equiv="refresh" content="0;url={home}"><title>平安護老院</title><a href="{home}">進入展示網站</a></html>')
    (output / '404.html').write_text(f'<!doctype html><meta charset="utf-8"><title>Page not found</title><a href="{home}">返回首頁 / Home</a>')
    (output / '.nojekyll').touch()
    (output / 'export-report.json').write_text(json.dumps({'source':source, 'pages':records, 'warnings':warnings}, ensure_ascii=False, indent=2))
    print(f'Exported {total} public pages. Missing optional images/files: {len(warnings)}. Output: {output}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', default='https://peace-beta-sandy.vercel.app')
    parser.add_argument('--output', default='_site')
    parser.add_argument('--base-path', default='/peace')
    parser.add_argument('--asset-root', default='peaceweb/static')
    parser.add_argument('--max-pages', type=int, default=100)
    args = parser.parse_args()
    snapshot(args.source, Path(args.output), args.base_path, Path(args.asset_root), args.max_pages)
