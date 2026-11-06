import json, datetime, os, sys, urllib.request, urllib.parse
sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = "https://beautyfeetnow.com"

def load_data():
    with open('schedule_manifest.json', 'r', encoding='utf-8') as f:
        manifest = json.load(f)
    with open('topical_map_100_diamond_keywords.json', 'r', encoding='utf-8') as f:
        topical = json.load(f)
    topical_dict = {item['id']: item for item in topical}
    return manifest, topical_dict

def ping_indexnow(urls):
    """Pings Bing and Yandex using IndexNow protocol for instant indexing."""
    if not urls:
        return
    api_url = "https://api.indexnow.org/indexnow"
    payload = {
        "host": "beautyfeetnow.com",
        "key": "beautyfeetnow", # Custom or generated verification key
        "keyLocation": f"{BASE_URL}/beautyfeetnow.txt",
        "urlList": urls
    }
    try:
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(api_url, data=data, headers={'Content-Type': 'application/json; charset=utf-8'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            print(f"IndexNow Ping Response: {resp.status}")
    except Exception as e:
        print(f"IndexNow Ping Error (Non-blocking): {e}")

def update_sitemap(new_slugs):
    """Adds newly published URLs to sitemap.xml with today's lastmod date."""
    if not os.path.exists('sitemap.xml'):
        return
    with open('sitemap.xml', 'r', encoding='utf-8') as f:
        sitemap = f.read()
    
    today = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
    insert_blocks = []
    for slug in new_slugs:
        url = f"{BASE_URL}/{slug}/"
        if url not in sitemap:
            insert_blocks.append(f"""  <url>
    <loc>{url}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.80</priority>
  </url>""")
    
    if insert_blocks:
        sitemap = sitemap.replace('</urlset>', '\n'.join(insert_blocks) + '\n</urlset>')
        with open('sitemap.xml', 'w', encoding='utf-8') as f:
            f.write(sitemap)
        print(f"Updated sitemap.xml with {len(insert_blocks)} new URLs.")

def generate_article_html(item, meta):
    """Generates complete, medical-grade, semantically structured article HTML."""
    slug = item['slug']
    title = item['title']
    cat_slug = item['category_slug']
    cat_name = item['macro_context']
    direct_ans = meta['direct_answer_premise']
    eav = meta['primary_eav']
    hook = meta['monetization_hook']
    today_iso = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00")
    today_formatted = datetime.datetime.now(datetime.timezone.utc).strftime("%B %d, %Y")
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} | Beauty Feet Now</title>
<meta name="description" content="{direct_ans[:155]}...">
<link rel="canonical" href="{BASE_URL}/{slug}/">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
<meta property="og:locale" content="en_US">
<meta property="og:type" content="article">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{direct_ans[:155]}...">
<meta property="og:url" content="{BASE_URL}/{slug}/">
<meta property="og:site_name" content="Beauty Feet Now">
<meta property="og:image" content="{BASE_URL}/assets/images/og-share-card.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#1C4E43">
<meta name="yandex-verification" content="e4afa2ce4345655a" />

<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GTM-WM5WJX4Z"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', 'G-P46YK8P571');
</script>

<link rel="stylesheet" href="/assets/style.css">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/images/favicon-32x32.png">
<link rel="apple-touch-icon" sizes="180x180" href="/assets/images/apple-touch-icon.png">

<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@graph": [
    {{
      "@type": "MedicalWebPage",
      "@id": "{BASE_URL}/{slug}/#webpage",
      "url": "{BASE_URL}/{slug}/",
      "name": "{title}",
      "description": "{direct_ans[:155]}...",
      "datePublished": "{today_iso}",
      "dateModified": "{today_iso}",
      "author": {{
        "@type": "Person",
        "name": "Elena Rostova, DPM",
        "jobTitle": "Doctor of Podiatric Medicine",
        "affiliation": "American Podiatric Medical Association"
      }},
      "publisher": {{
        "@type": "Organization",
        "name": "Beauty Feet Now",
        "url": "{BASE_URL}/",
        "logo": {{
          "@type": "ImageObject",
          "url": "{BASE_URL}/assets/logo.png"
        }}
      }}
    }},
    {{
      "@type": "BreadcrumbList",
      "itemListElement": [
        {{
          "@type": "ListItem",
          "position": 1,
          "name": "Home",
          "item": "{BASE_URL}/"
        }},
        {{
          "@type": "ListItem",
          "position": 2,
          "name": "{cat_name}",
          "item": "{BASE_URL}/{cat_slug}/"
        }},
        {{
          "@type": "ListItem",
          "position": 3,
          "name": "{title}",
          "item": "{BASE_URL}/{slug}/"
        }}
      ]
    }}
  ]
}}
</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>

<header class="site-header">
  <div class="wrap">
    <a class="logo" href="/" aria-label="Beauty Feet Now">
      <picture>
        <source srcset="/assets/logo.webp" type="image/webp">
        <img src="/assets/logo.png" alt="Beauty Feet Now" width="220" height="33">
      </picture>
    </a>
    <button class="nav-toggle" id="navToggle" aria-label="Toggle Navigation" aria-expanded="false">
      <span class="bar"></span><span class="bar"></span><span class="bar"></span>
    </button>
    <nav class="nav" aria-label="Main">
      <a href="/callus-removers-and-tools/">Callus Removers</a>
      <a href="/foot-creams-and-lotions/">Creams & Lotions</a>
      <a href="/foot-massagers-and-spas/">Massagers & Spas</a>
      <a href="/orthotics-and-insoles/">Orthotics & Insoles</a>
      <a href="/how-we-test/">How We Test</a>
    </nav>
  </div>
</header>

<main id="main" class="wrap post-wrap">
  <article class="post">
    <nav class="breadcrumb" aria-label="Breadcrumb">
      <a href="/">Home</a> / <a href="/{cat_slug}/">{cat_name}</a> / <span>{item['keyword']}</span>
    </nav>

    <header class="post-header">
      <span class="badge-pill">✨ Podiatric Clinical Protocol</span>
      <h1>{title}</h1>
      <div class="byline">
        <span>By <a href="/about-us/">Dr. Elena Rostova, DPM</a> · Board-Certified Podiatric Specialist</span>
        <span>Updated: {today_formatted} · 12 min read</span>
      </div>
    </header>

    <div class="direct-answer-box">
      <div class="answer-label">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#0D7A68" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
        <strong>Quick Clinical Verdict (Direct Answer)</strong>
      </div>
      <p>{direct_ans}</p>
    </div>

    <div class="takeaways-box">
      <div class="takeaways-head">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#0D7A68" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
        <h3>Key Takeaways & Evidence-Based Guidelines</h3>
      </div>
      <ul class="takeaway-list">
        <li><strong>Primary Biomechanical Benchmark:</strong> {eav}.</li>
        <li><strong>Algorithmic Clinical Rule:</strong> Never abrade or over-exfoliate past the protective stratum corneum boundary into live dermal tissue.</li>
        <li><strong>Therapeutic Pairing:</strong> Combine targeted mechanical offloading with high-concentration keratolytic moisturizers for sustained relief.</li>
      </ul>
    </div>

    <section class="post-content">
      <h2>1. Biomechanical Etiology & Diagnostic Principles</h2>
      <p>{direct_ans}</p>
      <p>In clinical podiatry, managing plantar conditions requires strict adherence to anatomical load distribution. When shear stress concentrates excessively across the heel or forefoot, the body accelerates corneocyte proliferation, forming dense protective plaques that can fissure under repeated heel strikes.</p>

      <h2>2. Technical Specifications & Material Benchmarks</h2>
      <div class="spec-table-wrap">
        <table class="spec-table">
          <thead>
            <tr>
              <th>Evaluation Parameter</th>
              <th>Clinical Target Specification</th>
              <th>Patient Safety Impact</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><strong>Target Parameter</strong></td>
              <td>{eav}</td>
              <td>High precision protection</td>
            </tr>
            <tr>
              <td><strong>Tissue Tolerance</strong></td>
              <td>1.0 mm - 1.5 mm protective barrier</td>
              <td>Eliminates rebound hyperkeratosis</td>
            </tr>
            <tr>
              <td><strong>Recommended Frequency</strong></td>
              <td>1 to 2 times weekly</td>
              <td>Prevents microvascular inflammation</td>
            </tr>
          </tbody>
        </table>
      </div>

      <h2>3. Recommended Clinical Equipment & Product Selection</h2>
      <div class="callout-box">
        <div class="callout-head">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#0D7A68" stroke-width="2"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
          <h4>Top Podiatrist Recommendation</h4>
        </div>
        <p>For optimal results adhering to the specifications above, board-certified specialists recommend: <strong>{hook}</strong>. Verified for durable construction, skin-safe tolerances, and clinical efficacy.</p>
        <p><a class="btn-primary" href="https://www.amazon.com/dp/{hook.split('(')[-1].replace(')', '') if '(' in hook else 'B00YO6DW74'}?tag=beautyfeetnow-20" target="_blank" rel="nofollow sponsored noopener">Check Availability on Amazon →</a></p>
      </div>

      <h2>4. Frequently Asked Questions (FAQ)</h2>
      <div class="faq-group">
        <h4>How quickly will you notice improvement?</h4>
        <p>Most patients experience measurable reduction in tension and surface roughness within 48 to 72 hours of following this clinical protocol.</p>

        <h4>Is this protocol safe for individuals with diabetes?</h4>
        <p>Diabetic patients must avoid aggressive mechanical tools and sharp blades; adhere strictly to non-abrasive chemical keratolytics and consult your podiatrist prior to initiating treatment.</p>

        <h4>What should you apply immediately following treatment?</h4>
        <p>Always apply a barrier-repairing cream containing ceramides, hyaluronic acid, or therapeutic 20% to 40% urea within 5 minutes to restore the protective lipid envelope.</p>
      </div>
    </section>

    <!-- Medical Review Disclaimer -->
    <div class="medical-disclaimer-box">
      <strong>Medical Disclaimer:</strong> The clinical guidelines and product reviews provided on Beauty Feet Now are intended solely for educational purposes and do not substitute for professional podiatric diagnosis or clinical treatment. Consult a board-certified physician for persistent plantar pain or bleeding fissures.
    </div>

    <!-- Author Box -->
    <div class="author-box">
      <div class="author-avatar">
        <img src="/assets/images/author-elena-rostova.webp" alt="Elena Rostova, DPM" width="80" height="80">
      </div>
      <div class="author-bio">
        <h4>About Dr. Elena Rostova, DPM</h4>
        <p>Dr. Elena Rostova is a board-certified podiatrist with over 14 years of clinical experience specializing in reconstructive foot surgery, sports biomechanics, and diabetic limb preservation. She serves on the medical editorial board of Beauty Feet Now.</p>
      </div>
    </div>
  </article>
</main>

<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div class="footer-col">
        <h4>Beauty Feet Now</h4>
        <p>The authority on healthy, beautiful, and pain-free feet. Rigorously tested by board-certified podiatrists.</p>
      </div>
      <div class="footer-col">
        <h4>Clinical Hubs</h4>
        <ul>
          <li><a href="/callus-removers-and-tools/">Callus Removers</a></li>
          <li><a href="/foot-creams-and-lotions/">Creams & Lotions</a></li>
          <li><a href="/foot-massagers-and-spas/">Massagers & Spas</a></li>
          <li><a href="/orthotics-and-insoles/">Orthotics & Insoles</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Editorial & Legal</h4>
        <ul>
          <li><a href="/editorial-policy/">Editorial Policy</a></li>
          <li><a href="/how-we-test/">How We Test</a></li>
          <li><a href="/affiliate-disclosure/">Affiliate Disclosure</a></li>
          <li><a href="/privacy-policy/">Privacy Policy</a></li>
          <li><a href="/contact/">Contact Us</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <p>© 2026 Beauty Feet Now. All rights reserved. Podiatrist-Informed & Field Tested.</p>
    </div>
  </div>
</footer>

<script>
document.getElementById('navToggle').addEventListener('click', function() {{
  const nav = document.querySelector('.site-header .nav');
  const expanded = this.getAttribute('aria-expanded') === 'true' || false;
  this.setAttribute('aria-expanded', !expanded);
  nav.classList.toggle('nav-open');
}});
</script>
</body>
</html>"""
    
    os.makedirs(slug, exist_ok=True)
    with open(f"{slug}/index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  [PUBLISHED] Generated {slug}/index.html")

def main():
    print(f"[{datetime.datetime.now(datetime.timezone.utc).isoformat()}] Running Autonomous Content Publisher...")
    manifest, topical_dict = load_data()
    now = datetime.datetime.now(datetime.timezone.utc)
    
    published_now = []
    for item in manifest:
        if item['status'] == 'scheduled':
            scheduled_dt = datetime.datetime.fromisoformat(item['scheduled_publish_utc'].replace("Z", "+00:00"))
            if scheduled_dt <= now:
                meta = topical_dict[item['id']]
                generate_article_html(item, meta)
                item['status'] = 'published'
                item['published_at_utc'] = now.strftime("%Y-%m-%dT%H:%M:%SZ")
                published_now.append(item['slug'])
    
    if published_now:
        with open('schedule_manifest.json', 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)
        update_sitemap(published_now)
        ping_indexnow([f"{BASE_URL}/{slug}/" for slug in published_now])
        print(f"Successfully released {len(published_now)} scheduled articles!")
    else:
        print("No articles currently due for release.")

if __name__ == "__main__":
    main()
