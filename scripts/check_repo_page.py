#!/usr/bin/env python3
"""Consistency check for docs/repositories.md.

Verifies the things that fail silently on the 仓库 page:
  * sidebar sub counts vs. the sub-section headings
  * sidebar sub order vs. the body order
  * total count label vs. the real number of cards
  * duplicate card ids
  * cards missing name / description / stars
  * avatars still pointing straight at github.com (should go through the CDN)

Usage:  python scripts/check_repo_page.py
Exit code 0 when everything matches, 1 otherwise.
"""

import io
import re
import sys

PATH = 'docs/repositories.md'


def main() -> int:
    s = io.open(PATH, encoding='utf-8').read()

    nav_start = s.index('<nav class="side-nav"')
    nav = s[nav_start:s.index('</nav>')]
    main_start = s.index('<main class="region region-main"')
    body = s[main_start:s.index('</main>')]

    problems = []

    side = [(m.group(1), m.group(2)) for m in re.finditer(
        r'class="sub-item" data-sub="([^"]+)"[^>]*>[^<]*<span class="sub-n">(\d+)</span>', nav)]
    body_subs = [(m.group(1), m.group(2)) for m in re.finditer(
        r'<section class="sub" data-sub="([^"]+)">\s*<h3 class="sub-head">[^<]*'
        r'<span class="sub-count">(\d+)</span>', body)]

    if side != body_subs:
        only_side = [k for k, _ in side if k not in dict(body_subs)]
        only_body = [k for k, _ in body_subs if k not in dict(side)]
        if only_side or only_body:
            problems.append('sub keys differ: sidebar-only=%s body-only=%s' % (only_side, only_body))
        for (k1, c1), (k2, c2) in zip(side, body_subs):
            if (k1, c1) != (k2, c2):
                problems.append('order/count differs at %s/%s: sidebar=(%s,%s) body=(%s,%s)'
                                % (k1, k2, k1, c1, k2, c2))
                break

    # cards per sub
    positions = [(m.start(), m.group(1)) for m in
                 re.finditer(r'<section class="sub" data-sub="([^"]+)">', body)]
    for i, (pos, key) in enumerate(positions):
        end = positions[i + 1][0] if i + 1 < len(positions) else len(body)
        actual = body[pos:end].count('<li class="repo-item"')
        declared = dict(body_subs).get(key)
        if declared is not None and str(actual) != declared:
            problems.append('sub %s: declared %s, actual %d' % (key, declared, actual))

    cards = re.findall(r'<li class="repo-item" id="([^"]+)">', body)
    total = len(cards)
    if len(set(cards)) != len(cards):
        dupes = sorted({c for c in cards if cards.count(c) > 1})
        problems.append('duplicate ids: %s' % dupes)

    label = re.search(r'id="resetCount">(\d+)\s*个仓库', s)
    if label and int(label.group(1)) != total:
        problems.append('resetCount says %s, actual %d' % (label.group(1), total))

    for cid in cards:
        block_start = body.index('id="%s"' % cid)
        block_end = body.index('</li>', block_start)
        block = body[block_start:block_end]
        for cls, label_name in (('repo-name', '名称'), ('repo-desc', '描述'), ('repo-stars', '星数')):
            if 'class="%s"' % cls not in block:
                problems.append('card %s missing %s' % (cid, label_name))

    direct = len(re.findall(r'src="https://github\.com/', s))
    if direct:
        problems.append('%d avatars still point at github.com directly' % direct)

    print('cards: %d | subs: %d | groups: %d'
          % (total, len(body_subs), body.count('class="cat"')))
    if problems:
        print('FAIL')
        for p in problems:
            print('  -', p)
        return 1
    print('OK')
    return 0


if __name__ == '__main__':
    sys.exit(main())
