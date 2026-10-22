"""Extract human-readable Korean text lines from generated html/md, one file per sample. usage: totext.py SRC_DIR DST_DIR"""
import re, html, sys, pathlib
src, dst = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]); dst.mkdir(exist_ok=True)
for d in sorted(p for p in src.iterdir() if p.is_dir()):
    files = [f for f in d.iterdir() if f.suffix in ('.html', '.md') and not f.name.startswith('.')]
    out = []
    for f in files:
        t = f.read_text(errors='replace')
        if f.suffix == '.html':
            t = re.sub(r'<(script|style|pre|code)\b.*?</\1>', '', t, flags=re.S | re.I)
            t = re.sub(r'<!--.*?-->', '', t, flags=re.S)
            t = re.sub(r'<br\s*/?>', ' ', t)
            t = re.sub(r'</?(span|b|strong|em|a|i|mark|small|kbd)\b[^>]*>', '', t)
            t = re.sub(r'<[^>]+>', '\n', t); t = html.unescape(t)
        else:
            t = re.sub(r'^```.*?^```', '', t, flags=re.S | re.M)
        out += [re.sub(r'\s+', ' ', l).strip() for l in t.splitlines() if re.search('[가-힣]', l)]
    (dst / f'{d.name}.txt').write_text('\n'.join(out) + '\n')
