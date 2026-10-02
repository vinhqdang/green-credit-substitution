"""Write chicago_refs.tex: a Taylor & Francis Chicago author-date reference list
built from references.bib, restricted to keys cited in manuscript.tex."""
import re
import unicodedata

BIB = 'references.bib'
TEX = 'manuscript.tex'
OUT = 'chicago_refs.tex'

PLACES = {
    'Cambridge University Press': 'Cambridge',
    'Oxford University Press': 'Oxford',
    'Elsevier': 'Amsterdam',
}
SMALL = {'a', 'an', 'the', 'and', 'but', 'or', 'nor', 'for', 'so', 'yet', 'as', 'at',
         'by', 'in', 'of', 'on', 'to', 'up', 'via', 'vs', 'from', 'with', 'into', 'over',
         'per', 'than', 'versus'}


def parse_bib(text):
    entries = {}
    for m in re.finditer(r'@(\w+)\{([^,]+),(.*?)\n\}', text, re.S):
        etype, key, body = m.group(1).lower(), m.group(2).strip(), m.group(3)
        fields = {}
        for f in re.finditer(r'(\w+)\s*=\s*\{(.*?)\},?\s*\n', body + '\n', re.S):
            fields[f.group(1).lower()] = ' '.join(f.group(2).split())
        entries[key] = (etype, fields)
    return entries


def split_names(author):
    if author.startswith('{') and author.endswith('}'):
        return [('', author[1:-1])]
    names = []
    for a in author.split(' and '):
        last, _, first = a.partition(',')
        names.append((first.strip(), last.strip()))
    return names


def fmt_authors(names):
    parts = []
    for i, (first, last) in enumerate(names):
        if not first:
            parts.append(last)
        elif i == 0:
            parts.append(f'{last}, {first}')
        else:
            parts.append(f'{first} {last}')
    if len(parts) == 1:
        return parts[0]
    return ', '.join(parts[:-1]) + ', and ' + parts[-1]


def cite_label(names):
    lasts = [last for _, last in names]
    if len(lasts) == 1:
        return lasts[0]
    if len(lasts) == 2:
        return f'{lasts[0]} and {lasts[1]}'
    if len(lasts) == 3:
        return f'{lasts[0]}, {lasts[1]}, and {lasts[2]}'
    return f'{lasts[0]} et al.'


def cap_word(word, force):
    """Capitalise one word for headline style, leaving protected or mixed-case words alone."""
    if word.startswith('{') or any(c.isupper() for c in word[1:]) or not word[:1].isalpha():
        return word
    if not force and word.lower() in SMALL:
        return word.lower()
    return word[:1].upper() + word[1:]


def title_case(title):
    tokens = re.split(r'(\s+)', title)
    words = [i for i, t in enumerate(tokens) if t.strip()]
    out = list(tokens)
    after_colon = True
    for n, i in enumerate(words):
        tok = tokens[i]
        force = after_colon or n == len(words) - 1
        pieces = tok.split('-')
        pieces = [cap_word(p, force or j > 0) if p else p for j, p in enumerate(pieces)]
        out[i] = '-'.join(pieces)
        after_colon = tok.endswith(':') or tok.endswith('?')
    return ''.join(out)


def quoted(title):
    t = title_case(title)
    end = '' if t.endswith(('?', '!', '.')) else '.'
    return f'``{t}{end}\'\''


def italic(title):
    t = title_case(title)
    end = '' if t.endswith(('?', '!', '.')) else '.'
    return f'\\emph{{{t}}}{end}'


def doi(f):
    return f' \\url{{https://doi.org/{f["doi"]}}}' if 'doi' in f else ''


def entry(etype, f):
    names = split_names(f['author'])
    who = fmt_authors(names)
    if f['author'].startswith('{International Finance Corporation'):
        who = 'IFC (International Finance Corporation)'
    head = f'{who}. {f["year"]}.'
    if etype == 'article':
        vol = f.get('volume', '')
        num = f' ({f["number"]})' if 'number' in f else ''
        pages = f.get('pages', '')
        src = f'\\emph{{{f["journal"]}}}'
        if vol:
            src += f' {vol}{num}'
            if pages:
                src += f': {pages}'
        elif pages:
            src += f': {pages}'
        return f'{head} {quoted(f["title"])} {src}.{doi(f)}'
    if etype == 'book':
        pub = f['publisher']
        return f'{head} {italic(f["title"])} {PLACES.get(pub, "")}: {pub}.{doi(f)}'
    if etype == 'incollection':
        eds = ' and '.join(f'{fi} {la}' for fi, la in split_names(f['editor']))
        pub = f['publisher']
        return (f'{head} {quoted(f["title"])} In \\emph{{{title_case(f["booktitle"])}}}, '
                f'vol.~{f["volume"]}, edited by {eds}, {f["pages"]}. '
                f'{PLACES.get(pub, "")}: {pub}.{doi(f)}')
    if etype == 'techreport':
        return (f'{head} {italic(f["title"])} EBRD Working Paper 268. London: European Bank '
                f'for Reconstruction and Development.{doi(f)}')
    if etype == 'misc':
        url = re.search(r'\\url\{([^}]*)\}', f['note']).group(1)
        return f'{head} {italic(f["title"])} Washington, DC: World Bank Group. \\url{{{url}}}'
    raise ValueError(etype)


def sort_key(item):
    key, (etype, f) = item
    s = re.sub(r'\\.|[{}]', '', f['author'])
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower()
    return (s, f['year'])


def main():
    entries = parse_bib(open(BIB).read())
    tex = open(TEX).read()
    cited = set()
    for m in re.finditer(r'\\cite[pt]?\*?(?:\[[^\]]*\])*\{([^}]*)\}', tex):
        cited.update(k.strip() for k in m.group(1).split(','))
    missing = cited - entries.keys()
    if missing:
        raise SystemExit(f'cited but not in bib: {sorted(missing)}')
    lines = ['\\begin{thebibliography}{99}', '']
    for key, (etype, f) in sorted(((k, entries[k]) for k in cited), key=sort_key):
        label = 'IFC' if key == 'ifc2025sbfn' else cite_label(split_names(f['author']))
        lines.append(f'\\bibitem[{label}({f["year"]})]{{{key}}}')
        lines.append(entry(etype, f))
        lines.append('')
    lines.append('\\end{thebibliography}')
    open(OUT, 'w').write('\n'.join(lines) + '\n')
    print(f'{len(cited)} references written to {OUT}')


if __name__ == '__main__':
    main()
