# build_home_pages.py
import os, sys, re
sys.stdout.reconfigure(encoding='utf-8')

# 1. Read base index.html
with open('index.html', 'r', encoding='utf-8') as f:
    orig_html = f.read()

# 2. Extract existing cards
cards = re.findall(r'(\s*<li>\s*<article class="card">.*?</article>\s*</li>)', orig_html, re.DOTALL)
print(f"Extracted {len(cards)} original cards from index.html")

# Define the card for the 4th roundup guide: /best-orthotic-insoles-for-flat-feet/
insole_card = '''        <li>
          <article class="card">
            <span class="card-pic">
              <img src="https://m.media-amazon.com/images/I/71fV7kP0s1L._AC_SL1500_.jpg" alt="Superfeet GREEN Professional-Grade High Arch Insoles" width="88" height="88" loading="lazy">
            </span>
            <div class="card-body">
              <span class="tag">Orthotics & Insoles</span>
              <h3><a href="/best-orthotic-insoles-for-flat-feet/">8 Best Orthotic Insoles for Flat Feet & Plantar Fasciitis (2026 Tested)</a></h3>
              <p>Compare top podiatrist-approved orthotic insoles by arch rigidity, deep heel cup stabilization, and shock absorption for flat feet relief.</p>
              <time datetime="2026-11-05">Updated November 5, 2026</time>
            </div>
          </article>
        </li>'''

# Check if insole_card is already present
has_insole = any('best-orthotic-insoles-for-flat-feet' in c for c in cards)
if not has_insole:
    # Insert right after the third roundup guide (index 3)
    cards.insert(3, insole_card)
    print("Inserted /best-orthotic-insoles-for-flat-feet/ at position 4")

print(f"Total cards pool: {len(cards)}")

# Slicing: Page 1 (0 to 12), Page 2 (12 to end)
page1_cards = cards[:12]
page2_cards = cards[12:]

print(f"Page 1 has {len(page1_cards)} cards")
print(f"Page 2 has {len(page2_cards)} cards")

# Clean existing pagination if present
def strip_pagination(html):
    return re.sub(r'\s*<!-- Pagination Component -->\s*<nav class="pagination-nav".*?</nav>', '', html, flags=re.DOTALL)

# Clean existing cards block
cards_regex = re.compile(r'(<ul class="cards">)(.*?)(</ul>)', re.DOTALL)

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
base_p1 = strip_pagination(orig_html)

# Add rel="next" if not present in head
if '<link rel="next"' not in base_p1:
    base_p1 = base_p1.replace(
        '<link rel="canonical" href="https://beautyfeetnow.com/">',
        '<link rel="canonical" href="https://beautyfeetnow.com/">\n<link rel="next" href="https://beautyfeetnow.com/page/2/">'
    )

cards_p1_str = '\n'.join(page1_cards) + '\n      '
new_p1_html = cards_regex.sub(rf'\1\n{cards_p1_str}\3\n{pagination_page1}', base_p1)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_p1_html)
print("Successfully generated index.html (Page 1) with 12 cards + pagination")

# --- BUILD PAGE 2 (page/2/index.html) ---
os.makedirs('page/2', exist_ok=True)

base_p2 = strip_pagination(orig_html)

# Update head meta for Page 2
base_p2 = re.sub(r'<title>.*?</title>', '<title>Latest Foot Care & Buying Guides - Page 2 | Beauty Feet Now</title>', base_p2)
base_p2 = re.sub(
    r'<meta name="description" content="[^"]+"',
    '<meta name="description" content="Explore expert-tested foot care guides, orthotic comparisons, and neuropathy relief protocols - Page 2 | Beauty Feet Now."',
    base_p2
)
base_p2 = base_p2.replace(
    '<link rel="canonical" href="https://beautyfeetnow.com/">',
    '<link rel="canonical" href="https://beautyfeetnow.com/page/2/">\n<link rel="prev" href="https://beautyfeetnow.com/">'
)
base_p2 = base_p2.replace(
    '<meta property="og:url" content="https://beautyfeetnow.com/">',
    '<meta property="og:url" content="https://beautyfeetnow.com/page/2/">'
)
base_p2 = base_p2.replace(
    '<meta property="og:title" content="Beauty Feet Now | Complete Foot Care & Massager Guides">',
    '<meta property="og:title" content="Latest Foot Care & Buying Guides - Page 2 | Beauty Feet Now">'
)

# Update section title
base_p2 = base_p2.replace(
    '<h2 class="section-title">Latest Foot Care & Buying Guides</h2>',
    '<h2 class="section-title">Latest Foot Care & Buying Guides — Page 2</h2>'
)

cards_p2_str = '\n'.join(page2_cards) + '\n      '
new_p2_html = cards_regex.sub(rf'\1\n{cards_p2_str}\3\n{pagination_page2}', base_p2)

with open('page/2/index.html', 'w', encoding='utf-8') as f:
    f.write(new_p2_html)
print("Successfully generated page/2/index.html (Page 2) with 4 cards + pagination")
