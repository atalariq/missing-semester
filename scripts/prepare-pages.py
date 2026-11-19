#!/usr/bin/env python3
"""Mount Jekyll output, retain original heading anchors, and check locale fidelity."""
import argparse
from collections import Counter
from html import escape
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from urllib.parse import unquote, urljoin, urlsplit


class DOM(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.headings = []
        self.ids = set()
        self.links = []
        self.images = []
        self.code = []
        self.pre = []
        self.incode = self.inpre = False
        self.codebuf = self.prebuf = ''
        self.lang = None
        self.lines = [0]
        for line in text.splitlines(keepends=True):
            self.lines.append(self.lines[-1] + len(line))
        self.feed(text)

    def handle_starttag(self, tag, pairs):
        a = dict(pairs)
        if tag == 'html':
            self.lang = a.get('lang')
        if a.get('id'):
            self.ids.add(a['id'])
        if re.fullmatch('h[1-6]', tag):
            line, col = self.getpos()
            self.headings.append((tag, a.get('id'), self.lines[line - 1] + col))
        if tag == 'a' and 'href' in a:
            self.links.append(a['href'])
        if tag in ('img', 'script', 'iframe', 'link'):
            value = a.get('src') if tag != 'link' else a.get('href')
            if value:
                self.images.append(value)
        if tag == 'pre':
            self.inpre, self.prebuf = True, ''
        if tag == 'code':
            self.incode, self.codebuf = True, ''

    def handle_data(self, text):
        if self.incode:
            self.codebuf += text
        if self.inpre:
            self.prebuf += text

    def handle_endtag(self, tag):
        if tag == 'code' and self.incode:
            self.code.append(self.codebuf)
            self.incode = False
        if tag == 'pre' and self.inpre:
            self.pre.append(self.prebuf)
            self.inpre = False


def file_for(site, urlpath):
    p = site / unquote(urlpath).lstrip('/')
    if p.is_dir():
        return p / 'index.html'
    return p


class Mount(HTMLParser):
    """Edit actual tag attributes only: never rewrite examples inside code text."""
    def __init__(self, text, site, base):
        super().__init__(convert_charrefs=False)
        self.text, self.site, self.base = text, site, base
        self.edits = []
        self.lines = [0]
        for line in text.splitlines(keepends=True):
            self.lines.append(self.lines[-1] + len(line))
        self.feed(text)

    def handle_starttag(self, tag, pairs):
        raw = self.get_starttag_text()
        changed = raw
        for attr, value in pairs:
            if attr not in ('href', 'src') or not value or not value.startswith('/') or value.startswith('//'):
                continue
            if value == self.base or value.startswith(self.base + '/'):
                continue
            parsed = urlsplit(value)
            local = parsed.path
            if tag == 'a' and not local.startswith('/id/') and file_for(self.site, '/id' + local).is_file():
                local = '/id' + local
            new = self.base + local + ('?' + parsed.query if parsed.query else '') + ('#' + parsed.fragment if parsed.fragment else '')
            # All Jekyll source attributes are quoted; keep the original quote and other bytes.
            pattern = r'(?i)(\b' + attr + r'\s*=\s*)([\"\'])(.*?)\2'
            changed = re.sub(pattern, lambda m: m[1] + m[2] + escape(new, quote=True) + m[2], changed, count=1)
        if changed != raw:
            line, col = self.getpos()
            self.edits.append((self.lines[line - 1] + col, len(raw), changed))

    handle_startendtag = handle_starttag

    def result(self):
        text = self.text
        for offset, length, replacement in reversed(self.edits):
            text = text[:offset] + replacement + text[offset + length:]
        return text


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('site', type=Path)
    ap.add_argument('english', type=Path, help='Native Jekyll build of the pinned original source')
    ap.add_argument('--baseurl', default='/missing-semester')
    ap.add_argument('--report', type=Path, default=Path('TRANSLATION_QA.json'))
    args = ap.parse_args()
    site, english, base = args.site.resolve(), args.english.resolve(), args.baseurl.rstrip('/')
    pages, aliases, blocks, pairs = 0, 0, 0, []
    for target in sorted((site / 'id').rglob('*.html')):
        relative = target.relative_to(site / 'id')
        source = english / relative
        if not source.is_file():
            continue  # Added download index, translated repository README, and 404.
        text = target.read_text()
        a, b = DOM(source.read_text()), DOM(text)
        assert a.pre == b.pre, ('Preformatted code changed', relative)
        assert Counter(a.code) == Counter(b.code), ('Code literal changed', relative,
            list((Counter(a.code) - Counter(b.code)).elements()), list((Counter(b.code) - Counter(a.code)).elements()))
        assert [x[0] for x in a.headings] == [x[0] for x in b.headings], ('Heading structure changed', relative)
        edits = []
        for original, localized in zip(a.headings, b.headings):
            anchor = original[1]
            if anchor and anchor not in b.ids:
                edits.append((localized[2], '<a id="' + escape(anchor, quote=True) + '"></a>\n'))
                b.ids.add(anchor)
                aliases += 1
        for offset, alias in reversed(edits):
            text = text[:offset] + alias + text[offset:]
        target.write_text(text)
        blocks += len(a.pre)
        pairs.append(str(relative))
        pages += 1
    for target in site.rglob('*.html'):
        target.write_text(Mount(target.read_text(), site, base).result())
    # GitHub Pages reads the project-root error page, while the pinned English
    # source remains available unchanged in the repository/reference build.
    if (site / 'id/404.html').is_file():
        (site / '404.html').write_text((site / 'id/404.html').read_text())
    cache = {}
    def load(path):
        path = path.resolve()
        if path not in cache:
            cache[path] = DOM(path.read_text())
        return cache[path]
    errors, links = [], 0
    for target in sorted((site / 'id').rglob('*.html')):
        dom = load(target)
        assert dom.lang == 'id', target
        origin = 'https://preview.invalid' + base + '/' + target.relative_to(site).as_posix()
        for url in dom.links + dom.images:
            parsed = urlsplit(url)
            if parsed.scheme or parsed.netloc:
                continue
            resolved = urlsplit(urljoin(origin, url))
            if not resolved.path.startswith(base + '/'):
                errors.append([str(target.relative_to(site)), url, 'outside project mount'])
                continue
            dest = file_for(site, resolved.path.removeprefix(base))
            if not dest.is_file():
                errors.append([str(target.relative_to(site)), url, 'missing file'])
            elif resolved.fragment and dest.suffix == '.html' and unquote(resolved.fragment) not in load(dest).ids:
                errors.append([str(target.relative_to(site)), url, 'missing anchor'])
            links += 1
    result = {'native_paired_pages': pages, 'paired_paths': pairs, 'pre_blocks_exact': blocks,
        'all_code_literals_exact': True, 'source_anchor_aliases_added': aliases,
        'local_links_and_assets_checked': links, 'link_errors': errors, 'human_review': False}
    args.report.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'paired_paths'}, ensure_ascii=False))
    assert not errors, f'{len(errors)} local link errors; see {args.report}'


if __name__ == '__main__':
    main()
