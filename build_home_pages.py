# build_home_pages.py
import os, sys, re
from all_articles_cards import ALL_CARDS
sys.stdout.reconfigure(encoding='utf-8')

# Read base template from index.html
with open('index.html', 'r', encoding='utf-8') as f:
    base_html = f.read()

# Clean existing pagination if present
def strip_pagination(html):
    return re.sub(r'\s*<!-- Pagination Component -->\s*<nav class="pagination-nav".*?</nav>', '', html, flags=re.DOTALL)

# Ensure SVG tags have explicit width and height
def fix_svg_attributes(html):
    html = re.sub(
        r'<svg class="trust-icon"\s*(?:width="[^"]*"\s*height="[^"]*"\s*)?viewBox="0 0 24 24">',
        r'<svg class="trust-icon" width="32" height="32" viewBox="0 0 24 24">',
        html
    )
    def fix_cat_svg(match):
        prefix = match.group(1)
        svg_tag = match.group(2)
        if 'width=' not in svg_tag:
            svg_tag = '<svg width="24" height="24" viewBox="0 0 24 24">'
        return prefix + svg_tag

    html = re.sub(
        r'(<div class="cat-icon">\s*)(<svg[^>]*>)',
        fix_cat_svg,
        html
    )
    return html

cards_regex = re.compile(r'(<ul class="cards">)(.*?)(</ul>)', re.DOTALL)

# 16 cards pool
page1_cards = ALL_CARDS[:12]
page2_cards = ALL_CARDS[12:]

print(f"Total cards pool: {len(ALL_CARDS)}")
print(f"Page 1 has {len(page1_cards)} cards")
print(f"Page 2 has {len(page2_cards)} cards")

# Pagination markup for Page 1
pagination_page1 = '''
      <!-- Pagination Component -->
      <nav class="pagination-nav" aria-label="Article Pagination">
        <ul class="pagination">
          <li class="disabled"><span>&larr; Prev</span></li>
          <li class="active"><span aria-current="page">1</span></li>
          <li><a href="/page/2/">2</a></li>
          <li class="next"><a href="/page/2/" rel="next">Next &rarr;</a></li>
        </ul>
      </nav>'''

# Pagination markup for Page 2
pagination_page2 = '''
      <!-- Pagination Component -->
      <nav class="pagination-nav" aria-label="Article Pagination">
        <ul class="pagination">
          <li class="prev"><a href="/" rel="prev">&larr; Prev</a></li>
          <li><a href="/">1</a></li>
          <li class="active"><span aria-current="page">2</span></li>
          <li class="disabled"><span>Next &rarr;</span></li>
        </ul>
      </nav>'''

# --- BUILD PAGE 1 (index.html) ---
p1 = strip_pagination(base_html)
p1 = fix_svg_attributes(p1)

# Ensure canonical and rel="next"
if '<link rel="next"' not in p1:
    p1 = p1.replace(
        '<link rel="canonical" href="https://beautyfeetnow.com/">',
        '<link rel="canonical" href="https://beautyfeetnow.com/">\n<link rel="next" href="https://beautyfeetnow.com/page/2/">'
    )

cards_p1_str = '\n'.join(page1_cards) + '\n      '
new_p1_html = cards_regex.sub(rf'\1\n{cards_p1_str}\3\n{pagination_page1}', p1)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_p1_html)
print("Successfully generated index.html (Page 1) with 12 cards + pagination")

# --- BUILD PAGE 2 (page/2/index.html) ---
os.makedirs('page/2', exist_ok=True)

p2 = strip_pagination(base_html)
p2 = fix_svg_attributes(p2)

# Update head meta for Page 2
p2 = re.sub(r'<title>.*?</title>', '<title>Latest Foot Care & Buying Guides - Page 2 | Beauty Feet Now</title>', p2)
p2 = re.sub(
    r'<meta name="description" content="[^"]+"',
    '<meta name="description" content="Explore expert-tested foot care guides, orthotic comparisons, and neuropathy relief protocols - Page 2 | Beauty Feet Now."',
    p2
)
p2 = p2.replace(
    '<link rel="canonical" href="https://beautyfeetnow.com/">',
    '<link rel="canonical" href="https://beautyfeetnow.com/page/2/">\n<link rel="prev" href="https://beautyfeetnow.com/">'
)
# remove rel="next" if present
p2 = re.sub(r'<link rel="next"[^>]*>\n?', '', p2)

p2 = p2.replace(
    '<meta property="og:url" content="https://beautyfeetnow.com/">',
    '<meta property="og:url" content="https://beautyfeetnow.com/page/2/">'
)
p2 = p2.replace(
    '<meta property="og:title" content="Beauty Feet Now | Complete Foot Care & Massager Guides">',
    '<meta property="og:title" content="Latest Foot Care & Buying Guides - Page 2 | Beauty Feet Now">'
)

# Update section title
p2 = p2.replace(
    '<h2 class="section-title">Latest Foot Care & Buying Guides</h2>',
    '<h2 class="section-title">Latest Foot Care & Buying Guides — Page 2</h2>'
)

cards_p2_str = '\n'.join(page2_cards) + '\n      '
new_p2_html = cards_regex.sub(rf'\1\n{cards_p2_str}\3\n{pagination_page2}', p2)

with open('page/2/index.html', 'w', encoding='utf-8') as f:
    f.write(new_p2_html)
print("Successfully generated page/2/index.html (Page 2) with 4 cards + pagination")
