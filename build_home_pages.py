# build_home_pages.py
# Generates index.html (Page 1) and page/2/index.html (Page 2) with exact pagination,
# mobile hamburger nav, icon suite, og:image, and YMYL compliance.

import os, sys, re
from all_articles_cards import ALL_CARDS
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    base_html = f.read()

# Update icons and og:image in head
def update_head(html):
    # Icon suite
    old_icons = re.search(r'<link rel="icon"[^>]*>.*?(?:<link rel="apple-touch-icon"[^>]*>)?', html, re.DOTALL)
    new_icons = """<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/images/favicon-32x32.png">
<link rel="apple-touch-icon" sizes="180x180" href="/assets/images/apple-touch-icon.png">"""
    
    if old_icons:
        html = html[:old_icons.start()] + new_icons + html[old_icons.end():]
    
    # og:image
    if '<meta property="og:image"' not in html:
        og_tag = """<meta property="og:image" content="https://beautyfeetnow.com/assets/images/og-share-card.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">"""
        html = html.replace('<meta name="twitter:card"', og_tag + '\n<meta name="twitter:card"')
        
    return html

# Update header with picture logo and hamburger toggle
def update_header(html):
    # Logo to picture
    html = re.sub(
        r'<a class="logo" href="/" aria-label="Beauty Feet Now">\s*<img src="/assets/logo.png"[^>]*>\s*</a>',
        """<a class="logo" href="/" aria-label="Beauty Feet Now">
      <picture>
        <source srcset="/assets/logo.webp" type="image/webp">
        <img src="/assets/logo.png" alt="Beauty Feet Now" width="220" height="33">
      </picture>
    </a>""",
        html
    )
    
    # Nav toggle button
    if 'id="navToggle"' not in html:
        html = re.sub(
            r'(<a class="logo"[^>]*>.*?</a>)',
            r'\1\n    <button class="nav-toggle" id="navToggle" aria-label="Toggle Navigation" aria-expanded="false">\n      <span class="bar"></span><span class="bar"></span><span class="bar"></span>\n    </button>',
            html,
            flags=re.DOTALL
        )
        
    # Remove old <details class="menu">
    html = re.sub(r'\s*<details class="menu">.*?</details>', '', html, flags=re.DOTALL)
    return html

# Update footer
def update_footer(html):
    # Footer logo to picture
    html = re.sub(
        r'<a class="footer-logo" href="/" aria-label="Beauty Feet Now">\s*<img src="/assets/logo.png"[^>]*>\s*</a>',
        """<a class="footer-logo" href="/" aria-label="Beauty Feet Now">
          <picture>
            <source srcset="/assets/logo.webp" type="image/webp">
            <img src="/assets/logo.png" alt="Beauty Feet Now" width="220" height="33">
          </picture>
        </a>""",
        html
    )
    
    # Footer medical note
    if 'footer-medical-note' not in html:
        html = html.replace(
            '</div>\n  </div>\n</footer>',
            '      <p class="footer-medical-note"><strong>Notice:</strong> This site complies with YMYL medical quality guidelines. Content is fact-checked against peer-reviewed biomechanical literature.</p>\n    </div>\n  </div>\n</footer>'
        )
        
    # Nav script before </body>
    if 'navToggle' not in html or "document.getElementById('navToggle')" not in html:
        script = """<script>
document.getElementById('navToggle').addEventListener('click', function() {
  var nav = document.querySelector('.site-header .nav');
  var isOpen = nav.classList.toggle('nav-open');
  this.setAttribute('aria-expanded', isOpen);
});
</script>
</body>"""
        html = html.replace('</body>', script)
        
    return html

# Strip existing pagination
def strip_pagination(html):
    return re.sub(r'\s*<!-- Pagination Component -->\s*<nav class="pagination-nav".*?</nav>', '', html, flags=re.DOTALL)

# SVG dimension fix
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

page1_cards = ALL_CARDS[:12]
page2_cards = ALL_CARDS[12:]

# EXACT Pagination Component markup as specified by user
pagination_page1 = '''
      <!-- Pagination Component -->
      <nav class="pagination-nav" aria-label="Pagination">
        <div class="pagination">
          <span class="pagination-btn pagination-prev disabled">&larr; Prev</span>
          <span class="pagination-link active">1</span>
          <a href="/page/2/" class="pagination-link">2</a>
          <a href="/page/2/" class="pagination-btn pagination-next">Next &rarr;</a>
        </div>
      </nav>'''

pagination_page2 = '''
      <!-- Pagination Component -->
      <nav class="pagination-nav" aria-label="Pagination">
        <div class="pagination">
          <a href="/" class="pagination-btn pagination-prev">&larr; Prev</a>
          <a href="/" class="pagination-link">1</a>
          <span class="pagination-link active">2</span>
          <span class="pagination-btn pagination-next disabled">Next &rarr;</span>
        </div>
      </nav>'''

# --- BUILD PAGE 1 (index.html) ---
p1 = base_html
p1 = update_head(p1)
p1 = update_header(p1)
p1 = update_footer(p1)
p1 = strip_pagination(p1)
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
print("Successfully generated index.html (Page 1) with 12 cards + exact pagination")

# --- BUILD PAGE 2 (page/2/index.html) ---
os.makedirs('page/2', exist_ok=True)

p2 = new_p1_html
p2 = strip_pagination(p2)

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
p2 = re.sub(r'<link rel="next"[^>]*>\n?', '', p2)

p2 = p2.replace(
    '<meta property="og:url" content="https://beautyfeetnow.com/">',
    '<meta property="og:url" content="https://beautyfeetnow.com/page/2/">'
)
p2 = p2.replace(
    '<meta property="og:title" content="Beauty Feet Now | Complete Foot Care & Massager Guides">',
    '<meta property="og:title" content="Latest Foot Care & Buying Guides - Page 2 | Beauty Feet Now">'
)

p2 = p2.replace(
    '<h2 class="section-title">Latest Foot Care & Buying Guides</h2>',
    '<h2 class="section-title">Latest Foot Care & Buying Guides — Page 2</h2>'
)

cards_p2_str = '\n'.join(page2_cards) + '\n      '
new_p2_html = cards_regex.sub(rf'\1\n{cards_p2_str}\3\n{pagination_page2}', p2)

with open('page/2/index.html', 'w', encoding='utf-8') as f:
    f.write(new_p2_html)
print("Successfully generated page/2/index.html (Page 2) with 4 cards + exact pagination")
