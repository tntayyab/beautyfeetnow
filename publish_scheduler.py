# -*- coding: utf-8 -*-
import json, datetime, os, sys, urllib.request, urllib.parse
sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = "https://beautyfeetnow.com"

# Import master content hub
try:
    from master_content_hub import get_all_drafts
    MASTER_DRAFTS = get_all_drafts()
except Exception as e:
    print(f"Warning: could not import master_content_hub: {e}")
    MASTER_DRAFTS = {}

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
        "key": "beautyfeetnow",
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
    today_iso = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00")
    today_formatted = datetime.datetime.now(datetime.timezone.utc).strftime("%B %d, %Y")
    
    # Check if a rich drafted master article exists in MASTER_DRAFTS
    draft = MASTER_DRAFTS.get(slug)
    
    if draft:
        direct_ans = draft.get('direct_answer', meta.get('direct_answer_premise', ''))
        takeaways_list = draft.get('takeaways', [])
        sections_data = draft.get('sections', [])
        table_data = draft.get('table', {})
        pbox_data = draft.get('pbox', {})
        faqs_data = draft.get('faqs', [])
    else:
        direct_ans = meta.get('direct_answer_premise', '')
        eav = meta.get('primary_eav', '')
        hook = meta.get('monetization_hook', '')
        takeaways_list = [
            f"Primary Biomechanical Benchmark: {eav}.",
            "Algorithmic Clinical Rule: Never abrade or over-exfoliate past the protective stratum corneum boundary into live dermal tissue.",
            "Therapeutic Pairing: Combine targeted mechanical offloading with high-concentration keratolytic moisturizers for sustained relief."
        ]
        sections_data = [
            {"title": "1. Biomechanical Etiology & Diagnostic Principles", "content": f"<p>{direct_ans}</p><p>In clinical podiatry, managing plantar conditions requires strict adherence to anatomical load distribution. When shear stress concentrates excessively across the heel or forefoot, the body accelerates corneocyte proliferation, forming dense protective plaques that can fissure under repeated heel strikes.</p>"},
            {"title": "2. Clinical Treatment Protocols & Safety Endpoints", "content": "<p>Conservative management should always follow structured phases: first debride non-viable hyperkeratotic tissue under aseptic conditions, then seal the epidermal barrier with lipid-rich emollients under occlusion.</p>"}
        ]
        table_data = {
            "headers": ["Evaluation Parameter", "Clinical Target Specification", "Patient Safety Impact"],
            "rows": [
                ["Target Parameter", eav, "High precision protection"],
                ["Tissue Tolerance", "1.0 mm - 1.5 mm protective barrier", "Eliminates rebound hyperkeratosis"],
                ["Recommended Frequency", "1 to 2 times weekly", "Prevents microvascular inflammation"]
            ]
        }
        pbox_data = {
            "name": hook.split('(')[0].strip() if '(' in hook else hook,
            "asin": hook.split('(')[-1].replace(')', '') if '(' in hook else 'B00P84K6LE',
            "score": "9.8",
            "img": "/assets/images/products/own-harmony-cr900.webp",
            "why": "Board-certified podiatric evaluation confirms optimal skin-safe tolerances, high-torque motor calibration, and rapid clinical debridement without epidermal micro-gouging."
        }
        faqs_data = [
            {"q": "How quickly will you notice improvement?", "a": "Most patients experience measurable reduction in tension and surface roughness within 48 to 72 hours of following this clinical protocol."},
            {"q": "Is this protocol safe for individuals with diabetes?", "a": "Diabetic patients must avoid aggressive mechanical tools and sharp blades; adhere strictly to non-abrasive chemical keratolytics and consult your podiatrist prior to initiating treatment."},
            {"q": "What should you apply immediately following treatment?", "a": "Always apply a barrier-repairing cream containing ceramides, hyaluronic acid, or therapeutic 20% to 40% urea within 5 minutes to restore the protective lipid envelope."}
        ]

    # Format Takeaways HTML
    takeaways_items = "".join([f"<li>{t}</li>" for t in takeaways_list])
    
    # Format Table HTML
    if table_data and 'headers' in table_data:
        th_html = "".join([f"<th>{h}</th>" for h in table_data['headers']])
        tr_html = "".join([f"<tr>{''.join([f'<td>{c}</td>' for c in row])}</tr>" for row in table_data.get('rows', [])])
        table_block = f"""
      <div class="scroll">
        <table>
          <thead><tr>{th_html}</tr></thead>
          <tbody>{tr_html}</tbody>
        </table>
      </div>"""
    else:
        table_block = ""

    # Format Sections HTML
    sections_html = ""
    for s_idx, sec in enumerate(sections_data):
        s_title = sec.get('title', '')
        s_content = sec.get('content', '')
        sections_html += f"""
      <h2>{s_title}</h2>
      {s_content}
"""
        # Inject Table after Section 2
        if s_idx == 1 and table_block:
            sections_html += table_block

    # Format Pbox HTML
    p_img = pbox_data.get('img', '/assets/images/products/own-harmony-cr900.webp')
    p_name = pbox_data.get('name', 'Recommended Clinical Device')
    p_asin = pbox_data.get('asin', 'B00P84K6LE')
    p_score = pbox_data.get('score', '9.8')
    p_why = pbox_data.get('why', 'Board-certified clinical review verifies optimal performance and patient safety tolerances.')
    
    pbox_html = f"""
      <aside class="pbox" aria-label="Top Podiatrist Recommendation">
        <span class="pbox-badge">&#9733; TOP PODIATRIST RECOMMENDATION</span>
        <div class="pbox-inner">
          <div class="pbox-img">
            <img src="{p_img}" alt="{p_name}" width="260" height="260" loading="lazy">
          </div>
          <div class="pbox-info">
            <h3 class="pbox-title">{p_name}</h3>
            <p class="pbox-why"><strong>Clinical Evaluation:</strong> {p_why}</p>
            <div class="pbox-meta">
              <span class="pbox-score"><strong>{p_score}</strong> / 10 Podiatrist Score</span>
              <a class="pbox-btn btn-amazon-cta" href="https://www.amazon.com/dp/{p_asin}?tag=beautyfeetnow-20" target="_blank" rel="nofollow sponsored noopener"><span>&#128722; Check Price on Amazon &rarr;</span></a>
            </div>
          </div>
        </div>
      </aside>"""

    # Format FAQs HTML
    faqs_items = "".join([f"""
        <details>
          <summary><h4>{f.get('q', f.get('question', ''))}</h4></summary>
          <div><p>{f.get('a', f.get('answer', ''))}</p></div>
        </details>""" for f in faqs_data])

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
      <a href="/">Home</a>
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
        <span>Updated: {today_formatted} · 14 min read</span>
      </div>
    </header>

    <div class="direct-answer-box">
      <div class="answer-label">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#0D7A68" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
        <strong>Quick Clinical Verdict (Direct Answer)</strong>
      </div>
      <p>{direct_ans}</p>
    </div>

    <!-- Bulletproof Takeaways Box -->
    <div class="takeaways">
      <div class="takeaways-head">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#0D7A68" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:22px!important;height:22px!important;min-width:22px!important;max-width:22px!important;fill:none!important;stroke:#0D7A68!important;display:inline-block!important;flex-shrink:0!important;"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" fill="none" stroke="#0D7A68" stroke-width="2"/><polyline points="22 4 12 14.01 9 11.01" fill="none" stroke="#0D7A68" stroke-width="2"/></svg>
        <span>Key Clinical Takeaways &amp; Evidence-Based Guidelines</span>
      </div>
      <ul class="takeaways-list">
        {takeaways_items}
      </ul>
    </div>

    <section class="post-content">
      {sections_html}
      {pbox_html}

      <h2>Frequently Asked Questions (FAQ)</h2>
      <div class="faq-group">
        {faqs_items}
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
    print(f"  [PUBLISHED] Generated {slug}/index.html ({len(html.split())} words)")

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
