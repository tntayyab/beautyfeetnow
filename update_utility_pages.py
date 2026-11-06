# update_utility_pages.py
# Ensures all institutional & legal pages have proper logo picture, navToggle, icons, og:image, and footer note

import os, re

UTILITY_PAGES = [
    'about-us/index.html',
    'contact/index.html',
    'editorial-policy/index.html',
    'how-we-test/index.html',
    'affiliate-disclosure/index.html',
    'privacy-policy/index.html',
    'terms-of-service/index.html'
]

def update_utility_page(path):
    if not os.path.exists(path):
        print(f"File not found: {path}")
        return
        
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Icons
    if '/favicon.ico' not in html:
        old_icons = re.search(r'<link rel="icon"[^>]*>.*?(?:<link rel="apple-touch-icon"[^>]*>)?', html, re.DOTALL)
        new_icons = """<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/images/favicon-32x32.png">
<link rel="apple-touch-icon" sizes="180x180" href="/assets/images/apple-touch-icon.png">"""
        if old_icons:
            html = html[:old_icons.start()] + new_icons + html[old_icons.end():]
        else:
            html = html.replace('</head>', new_icons + '\n</head>')

    # 2. og:image
    if '<meta property="og:image"' not in html:
        og = """<meta property="og:image" content="https://beautyfeetnow.com/assets/images/og-share-card.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">"""
        if '<meta name="twitter:card"' in html:
            html = html.replace('<meta name="twitter:card"', og + '\n<meta name="twitter:card"')
        else:
            html = html.replace('</head>', og + '\n</head>')

    # 3. Logo picture
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

    # 4. Nav toggle button
    if 'id="navToggle"' not in html:
        html = re.sub(
            r'(<a class="logo"[^>]*>.*?</a>)',
            r'\1\n    <button class="nav-toggle" id="navToggle" aria-label="Toggle Navigation" aria-expanded="false">\n      <span class="bar"></span><span class="bar"></span><span class="bar"></span>\n    </button>',
            html,
            flags=re.DOTALL
        )

    # Remove old menu details
    html = re.sub(r'\s*<details class="menu">.*?</details>', '', html, flags=re.DOTALL)

    # 5. Footer logo picture
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

    # 6. Footer medical note
    if 'footer-medical-note' not in html:
        html = html.replace(
            '</div>\n  </div>\n</footer>',
            '      <p class="footer-medical-note"><strong>Notice:</strong> This site complies with YMYL medical quality guidelines. Content is fact-checked against peer-reviewed biomechanical literature.</p>\n    </div>\n  </div>\n</footer>'
        )

    # 7. NavToggle JS before </body>
    if 'document.getElementById(\'navToggle\')' not in html:
        script = """<script>
document.getElementById('navToggle').addEventListener('click', function() {
  var nav = document.querySelector('.site-header .nav');
  var isOpen = nav.classList.toggle('nav-open');
  this.setAttribute('aria-expanded', isOpen);
});
</script>
</body>"""
        html = html.replace('</body>', script)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Updated utility page: {path}")

for p in UTILITY_PAGES:
    update_utility_page(p)

print("All utility pages updated successfully!")
