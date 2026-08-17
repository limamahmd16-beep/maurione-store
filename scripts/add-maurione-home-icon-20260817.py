from pathlib import Path
import json, struct, zlib

ROOT = Path('.')
INDEX = ROOT / 'index.html'

NAVY = (7, 21, 34)
GOLD = (211, 164, 77)
WHITE = (255, 255, 255)


def inside_poly(x, y, pts):
    sign = None
    n = len(pts)
    for i in range(n):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % n]
        c = (x - x1) * (y2 - y1) - (y - y1) * (x2 - x1)
        if c == 0:
            continue
        s = c > 0
        if sign is None:
            sign = s
        elif sign != s:
            return False
    return True


def make_png(size, path):
    upper = [(.27, .28), (.59, .15), (.59, .48), (.27, .61)]
    lower = [(.44, .52), (.76, .39), (.76, .72), (.44, .85)]
    p1 = [(a * size, b * size) for a, b in upper]
    p2 = [(a * size, b * size) for a, b in lower]
    rows = []
    for y in range(size):
        row = bytearray([0])
        py = y + .5
        for x in range(size):
            px = x + .5
            if inside_poly(px, py, p1):
                rgb = NAVY
            elif inside_poly(px, py, p2):
                rgb = GOLD
            else:
                rgb = WHITE
            row.extend(rgb)
        rows.append(bytes(row))
    raw = b''.join(rows)
    def chunk(t, data):
        return struct.pack('>I', len(data)) + t + data + struct.pack('>I', zlib.crc32(t + data) & 0xffffffff)
    png = b'\x89PNG\r\n\x1a\n'
    png += chunk(b'IHDR', struct.pack('>IIBBBBB', size, size, 8, 2, 0, 0, 0))
    png += chunk(b'IDAT', zlib.compress(raw, 9))
    png += chunk(b'IEND', b'')
    path.write_bytes(png)


make_png(180, ROOT / 'apple-touch-icon.png')
make_png(192, ROOT / 'maurione-icon-192.png')
make_png(512, ROOT / 'maurione-icon-512.png')
make_png(512, ROOT / 'favicon.png')

manifest = {
    'name': 'MauriOne',
    'short_name': 'MauriOne',
    'start_url': '/',
    'display': 'standalone',
    'background_color': '#ffffff',
    'theme_color': '#ffffff',
    'icons': [
        {'src': '/maurione-icon-192.png', 'sizes': '192x192', 'type': 'image/png'},
        {'src': '/maurione-icon-512.png', 'sizes': '512x512', 'type': 'image/png'}
    ]
}
(ROOT / 'site.webmanifest').write_text(json.dumps(manifest, ensure_ascii=False, separators=(',', ':')), encoding='utf-8')

s = INDEX.read_text(encoding='utf-8')
links = '''<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="apple-mobile-web-app-title" content="MauriOne">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png?v=2">
<link rel="icon" type="image/png" sizes="512x512" href="/favicon.png?v=2">
<link rel="manifest" href="/site.webmanifest?v=2">'''
if 'rel="apple-touch-icon"' not in s:
    anchor = '<meta name="application-name" content="MauriOne"><meta name="theme-color" content="#ffffff">'
    if anchor not in s:
        raise SystemExit('head metadata anchor not found')
    s = s.replace(anchor, anchor + '\n' + links, 1)
else:
    import re
    s = re.sub(r'<link rel="apple-touch-icon"[^>]*>', '<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png?v=2">', s, count=1)
INDEX.write_text(s, encoding='utf-8')
print('MauriOne home-screen icon assets and metadata added')
