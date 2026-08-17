from pathlib import Path

p = Path('index.html')
html = p.read_text(encoding='utf-8')

# Remove the dark overlay from the hero background so the uploaded image is shown clearly.
html = html.replace("linear-gradient(rgba(2,3,4,.45),rgba(7,16,30,.55)),", "")

marker = "/* MauriOne clean hero v15 */"
css = """
/* MauriOne clean hero v15 */
#siteHero .hero-copy{
  display:none!important;
}
#siteHero{
  background-color:#fff!important;
}
"""
if marker not in html:
    html = html.replace('</style>', css + '\n</style>', 1)

p.write_text(html, encoding='utf-8')

assert marker in html
assert 'linear-gradient(rgba(2,3,4,.45),rgba(7,16,30,.55)),' not in html
assert '#siteHero .hero-copy' in html
print('hero cleanup applied')
