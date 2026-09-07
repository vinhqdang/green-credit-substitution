"""Convert references.bib to an APA 7 \\thebibliography block for elsarticle+natbib."""
import re
import sys

BIB = 'latex/references.bib'

# Proper nouns / acronyms that keep their capitalisation when a title-case
# title is converted to APA sentence case.
KEEP = set()  # proper nouns are protected by {braces} in the .bib itself


def split_entries(text):
    out = []
    i = 0
    while True:
        m = re.compile(r'@(\w+)\s*\{\s*([^,\s]+)\s*,', re.S).search(text, i)
        if not m:
            break
        depth = 1
        j = m.end()
        while j < len(text) and depth:
            if text[j] == '{':
                depth += 1
            elif text[j] == '}':
                depth -= 1
            j += 1
        out.append((m.group(1).lower(), m.group(2), text[m.end():j - 1]))
        i = j
    return out


def parse_fields(body):
    fields = {}
    i = 0
    while i < len(body):
        while i < len(body) and body[i] in ' \t\r\n,':
            i += 1
        m = re.compile(r'(\w+)\s*=\s*').match(body, i)
        if not m:
            nxt = body.find(',', i)
            if nxt == -1:
                break
            i = nxt + 1
            continue
        i = m.end()
        if body[i] == '{':
            depth, j = 1, i + 1
            while j < len(body) and depth:
                if body[j] == '{':
                    depth += 1
                elif body[j] == '}':
                    depth -= 1
                j += 1
            val = body[i + 1:j - 1]
            i = j
        else:
            j = i
            while j < len(body) and body[j] not in ',\n':
                j += 1
            val = body[i:j]
            i = j
        fields[m.group(1).lower()] = ' '.join(val.split())
        nxt = body.find(',', i)
        i = len(body) if nxt == -1 else nxt + 1
    return fields


def split_authors(raw):
    """Split a BibTeX author field, respecting {braced corporate names}."""
    parts, depth, cur = [], 0, ''
    tokens = raw.split(' and ')
    # re-join tokens that were split inside braces
    for t in tokens:
        cur = (cur + ' and ' + t) if cur else t
        depth += cur.count('{') - cur.count('}')
        if depth <= 0:
            parts.append(cur.strip())
            cur, depth = '', 0
    if cur:
        parts.append(cur.strip())
    return parts


def initials(given):
    out = []
    for tok in re.split(r'[\s.]+', given):
        if not tok:
            continue
        if '-' in tok:  # hyphenated given name: Thi-Hong-Hanh -> T.-H.-H.
            out.append('-'.join(p[0] + '.' for p in tok.split('-') if p))
        else:
            out.append(tok[0] + '.')
    return ' '.join(out)


def fmt_author(a):
    if a.startswith('{') and a.endswith('}'):
        return a[1:-1]  # corporate author, verbatim
    if ',' in a:
        last, given = [x.strip() for x in a.split(',', 1)]
    else:
        bits = a.split()
        last, given = bits[-1], ' '.join(bits[:-1])
    return f'{last}, {initials(given)}' if given else last


def author_list(raw):
    people = [fmt_author(a) for a in split_authors(raw)]
    if len(people) == 1:
        return people[0]
    if len(people) == 2:
        return f'{people[0]}, \\& {people[1]}'
    return ', '.join(people[:-1]) + f', \\& {people[-1]}'


def editor_list(raw):
    """APA editors read given-name-first: B. S. Jones & R. Z. Smith."""
    out = []
    for a in split_authors(raw):
        if ',' in a:
            last, given = [x.strip() for x in a.split(',', 1)]
        else:
            bits = a.split()
            last, given = bits[-1], ' '.join(bits[:-1])
        out.append(f'{initials(given)} {last}'.strip())
    if len(out) == 1:
        return out[0]
    if len(out) == 2:
        return f'{out[0]}, \\& {out[1]}'
    return ', '.join(out[:-1]) + f', \\& {out[-1]}'


def cite_label(raw):
    """natbib label: Smith; Smith and Jones; Smith et al."""
    people = split_authors(raw)
    def last(a):
        if a.startswith('{') and a.endswith('}'):
            return a[1:-1]
        return a.split(',')[0].strip() if ',' in a else a.split()[-1]
    names = [last(p) for p in people]
    if len(names) == 1:
        return names[0]
    if len(names) == 2:
        return f'{names[0]} and {names[1]}'
    return f'{names[0]} et al.'


def sentence_case(title):
    """Title case -> APA sentence case, preserving braces and proper nouns."""
    # protect braced spans
    spans = []
    def stash(m):
        spans.append(m.group(1))
        return f'\x00{len(spans) - 1}\x00'
    t = re.sub(r'\{([^{}]*)\}', stash, title)

    words = t.split(' ')
    out = []
    start_of_sentence = True
    for w in words:
        core = w.strip('.,;:?!()')
        if '\x00' in w or not core:
            out.append(w)
            start_of_sentence = w.endswith((':', '.', '?', '!'))
            continue
        if core in KEEP or core.rstrip("'s") in KEEP:
            out.append(w)
        elif core.isupper() and len(core) > 1:
            out.append(w)              # acronym
        elif start_of_sentence:
            out.append(w[0].upper() + w[1:] if w[0].islower() else w)
        elif re.match(r'^[A-Z][a-z]', core):
            # lowercase each hyphen-separated part unless it is an acronym
            def low(part):
                if part[:1].isupper() and not (part.isupper() and len(part) > 1):
                    return part[0].lower() + part[1:]
                return part
            out.append('-'.join(low(x) for x in w.split('-')))
        else:
            out.append(w)
        start_of_sentence = w.endswith((':', '.', '?', '!'))
    t = ' '.join(out)
    for i, span in enumerate(spans):
        t = t.replace(f'\x00{i}\x00', span)
    return t


def pages_apa(p):
    p = p.replace('--', '\u2013').replace(' - ', '\u2013')
    return p.replace('\u2013', '--')


def doi_line(f):
    if f.get('doi'):
        return f" \\url{{https://doi.org/{f['doi']}}}"
    return ''


def format_entry(etype, key, f):
    auth = author_list(f['author'])
    year = f.get('year', 'n.d.')
    title = sentence_case(f.get('title', ''))
    head = f'{auth} ({year}).'

    if etype == 'article':
        journal = f.get('journal', '')
        sep = '' if title.endswith(('?', '!')) else '.'
        bits = f'{head} {title}{sep} \\emph{{{journal}}}'
        if f.get('volume'):
            bits += f', \\emph{{{f["volume"]}}}'
            if f.get('number'):
                bits += f'({f["number"]})'
        elif f.get('number'):
            bits += f', {f["number"]}'
        if f.get('pages'):
            pg = pages_apa(f['pages'])
            # no range dash means it is an article number, not a page range
            bits += f', Article {pg}' if '--' not in pg else f', {pg}'
        bits += '.' + doi_line(f)
        return bits

    if etype == 'book':
        dot = '' if title.endswith(('?', '!')) else '.'
        s = f'{head} \\emph{{{title}}}{dot} {f.get("publisher", "")}.'
        return s + doi_line(f)

    if etype == 'incollection':
        eds = editor_list(f['editor']) if f.get('editor') else ''
        s = f'{head} {title}. In {eds} (Eds.), \\emph{{{sentence_case(f.get("booktitle", ""))}}}'
        if f.get('volume'):
            s += f' (Vol. {f["volume"]}'
            s += f', pp. {pages_apa(f["pages"])})' if f.get('pages') else ')'
        elif f.get('pages'):
            s += f' (pp. {pages_apa(f["pages"])})'
        s += f'. {f.get("publisher", "")}.'
        return s + doi_line(f)

    if etype == 'techreport':
        dot = '' if title.endswith(('?', '!')) else '.'
        s = f'{head} \\emph{{{title}}}{dot} {f.get("institution", "")}.'
        return s + doi_line(f)

    # misc
    s = f'{head} \\emph{{{title}}}' + ('' if title.endswith(('?', '!')) else '.')
    if f.get('howpublished'):
        s += f' {f["howpublished"]}.'
    if f.get('note'):
        s += ' ' + f['note']
    return s + doi_line(f)


def main():
    text = open(BIB).read()
    entries = []
    for etype, key, body in split_entries(text):
        f = parse_fields(body)
        entries.append((etype, key, f))

    def sortkey(e):
        raw = e[2]['author']
        first = split_authors(raw)[0]
        if first.startswith('{'):
            last, given = first[1:-1], ''
        elif ',' in first:
            last, given = [x.strip() for x in first.split(',', 1)]
        else:
            bits = first.split()
            last, given = bits[-1], ' '.join(bits[:-1])
        return (last.lower(), given.lower(), e[2].get('year', ''))

    entries.sort(key=sortkey)

    lines = [r'\begin{thebibliography}{99}', '']
    for etype, key, f in entries:
        label = f'{cite_label(f["author"])}({f.get("year", "n.d.")})'
        lines.append(f'\\bibitem[{label}]{{{key}}}')
        lines.append(format_entry(etype, key, f))
        lines.append('')
    lines.append(r'\end{thebibliography}')
    out = '\n'.join(lines)
    sys.stdout.write(out)


if __name__ == '__main__':
    main()
