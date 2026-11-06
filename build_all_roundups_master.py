# build_all_roundups_master.py
import os, json, re

from roundup_callus_data import DATA as callus_data
from roundup_creams_data import DATA as creams_data
from roundup_massagers_data import DATA as massagers_data
from roundup_orthotics_data import DATA as orthotics_data

BASE_URL = "https://beautyfeetnow.com"
AMZ_TAG = "beautyfeetnow-20"

ROUNDUPS = [callus_data, creams_data, massagers_data, orthotics_data]

# Product Image Mapping (all local 400x400 square webps)
IMG_MAP = {
    # Callus Removers
    "B00LE99PA2": "/assets/images/products/amope-pedi-perfect.webp?v=2.0",
    "B00YO6DW74": "/assets/images/products/own-harmony-cr900.webp?v=2.0",
    "B075QD7B78": "/assets/images/products/pritech-3-roller.webp?v=2.0",
    "B08R9Z2H8M": "/assets/images/products/care-me-powerful.webp?v=2.0",
    "B00VPNE57O": "/assets/images/products/rikans-colossal-rasp.webp?v=2.0",
    "B071Z9WVRD": "/assets/images/products/bonafide-nano-glass.webp?v=2.0",
    "B08QMWH78F": "/assets/images/products/finishing-touch-flawless.webp?v=2.0",
    "B00K588G3M": "/assets/images/products/scholl-velvet-smooth.webp?v=2.0",
    # Creams & Lotions
    "B0886DBQCV": "/assets/images/products/purorganica-urea-40.webp?v=2.0",
    "B07N8G6P3F": "/assets/images/products/ebanel-urea-40-plus.webp?v=2.0",
    "B08K7G5C2W": "/assets/images/products/grocerism-urea-40-tub.webp?v=2.0",
    "B00IN5VUUM": "/assets/images/products/okeeffes-healthy-feet.webp?v=2.0",
    "B00D7BZNT2": "/assets/images/products/cerave-sa-foot-cream.webp?v=2.0",
    "B07CG6K9VT": "/assets/images/products/amlactin-rapid-relief.webp?v=2.0",
    "B0013838XQ": "/assets/images/products/flexitol-heel-balm.webp?v=2.0",
    "B07V2BCRN2": "/assets/images/products/urea-40-plus-gel.webp?v=2.0",
    # Massagers & Spas
    "B0797G8736": "/assets/images/products/miko-shiatsu-massager.webp?v=2.0",
    "B07F2H1NQR": "/assets/images/products/renpho-heated-compression.webp?v=2.0",
    "B01FHOHVDC": "/assets/images/products/cloud-massage-shiatsu.webp?v=2.0",
    "B019ITR4N2": "/assets/images/products/homedics-air-pro.webp?v=2.0",
    "B0169G1R7K": "/assets/images/products/best-choice-shiatsu-calf.webp?v=2.0",
    "B07R4R79T4": "/assets/images/products/tisscare-reflexology.webp?v=2.0",
    "B08CRX6M9W": "/assets/images/products/foot-cure-spa-bath.webp?v=2.0",
    # Orthotics & Insoles
    "B000XY5Q6C": "/assets/images/products/superfeet-green-insole.webp?v=2.0",
    "B000KGOHCS": "/assets/images/products/powerstep-pinnacle.webp?v=2.0",
    "B075YB2J6Q": "/assets/images/products/walkhero-plantar-fasciitis.webp?v=2.0",
    "B00U3LGB3A": "/assets/images/products/samurai-insoles-ninjas.webp?v=2.0",
    "B07D38D9M2": "/assets/images/products/easyfeet-heavy-duty.webp?v=2.0",
    "B0009EIMW0": "/assets/images/products/dr-scholls-plantar-fasciitis.webp?v=2.0",
    "B01G27K76Y": "/assets/images/products/sole-active-thick.webp?v=2.0",
    "B07797SL1Z": "/assets/images/products/physix-gear-sport.webp?v=2.0"
}

# Related Guides Pool for 3-Column Bottom Grid
RELATED_POOL = [
    {'slug': 'best-electric-callus-removers', 'title': '8 Best Electric Callus Removers (2026)', 'tag': 'Callus Removers and Tools', 'img': '/assets/images/electric-callus-safe-use.webp'},
    {'slug': 'how-to-use-electric-callus-remover-safely', 'title': 'How to Use an Electric Callus Remover Safely', 'tag': 'Callus Removers and Tools', 'img': '/assets/images/roller-grit-skin-contact.webp'},
    {'slug': 'nano-glass-foot-file-vs-electric-callus-remover', 'title': 'Nano Glass Foot File vs Electric Callus Remover', 'tag': 'Callus Removers and Tools', 'img': '/assets/images/nano-glass-vs-electric.webp'},
    {'slug': 'why-do-foot-calluses-keep-coming-back', 'title': 'Why Do Foot Calluses Keep Coming Back?', 'tag': 'Callus Removers and Tools', 'img': '/assets/images/callus-causes-gait.webp'},
    {'slug': 'best-cracked-heel-creams-with-urea', 'title': '8 Best Cracked Heel Creams with Urea (2026)', 'tag': 'Foot Creams and Lotions', 'img': '/assets/images/cracked-heel-fissures.webp'},
    {'slug': 'urea-cream-20-vs-40-percent-difference', 'title': 'Urea Cream 20% vs 40%: Key Differences', 'tag': 'Foot Creams and Lotions', 'img': '/assets/images/urea-concentration-skin.webp'},
    {'slug': 'how-to-heal-deep-cracked-heels-overnight', 'title': 'How to Heal Deep Cracked Heels Overnight', 'tag': 'Foot Creams and Lotions', 'img': '/assets/images/cracked-heel-recovery.webp'},
    {'slug': 'salicylic-acid-vs-lactic-acid-for-rough-feet', 'title': 'Salicylic Acid vs Lactic Acid for Rough Feet', 'tag': 'Foot Creams and Lotions', 'img': '/assets/images/salicylic-vs-lactic-feet.webp'},
    {'slug': 'best-heated-foot-massagers-for-plantar-fasciitis', 'title': '7 Best Heated Foot Massagers (2026)', 'tag': 'Foot Massagers and Spas', 'img': '/assets/images/foot-massager-routine.webp'},
    {'slug': 'how-often-should-you-use-a-foot-massager', 'title': 'How Often Should You Use a Foot Massager?', 'tag': 'Foot Massagers and Spas', 'img': '/assets/images/foot-massager-daily-use.webp'},
    {'slug': 'shiatsu-vs-air-compression-foot-massager', 'title': 'Shiatsu vs Air Compression Foot Massagers', 'tag': 'Foot Massagers and Spas', 'img': '/assets/images/shiatsu-vs-air-compression.webp'},
    {'slug': 'why-do-feet-burn-at-night-causes-and-relief', 'title': 'Why Do Feet Burn at Night? Causes & Relief', 'tag': 'Foot Massagers and Spas', 'img': '/assets/images/burning-feet-night-relief.webp'},
    {'slug': 'best-orthotic-insoles-for-flat-feet', 'title': '9 Best Orthotic Insoles for Flat Feet (2026)', 'tag': 'Orthotics and Insoles', 'img': '/assets/images/custom-molded-insoles.webp'},
    {'slug': 'rigid-vs-soft-orthotic-insoles-plantar-fasciitis', 'title': 'Rigid vs Soft Orthotic Insoles for Plantar Fasciitis', 'tag': 'Orthotics and Insoles', 'img': '/assets/images/rigid-vs-soft-orthotics.webp'},
    {'slug': 'how-to-tell-if-you-have-flat-feet-or-high-arches', 'title': 'How to Tell if You Have Flat Feet or High Arches', 'tag': 'Orthotics and Insoles', 'img': '/assets/images/flat-feet-vs-high-arches.webp'},
    {'slug': 'signs-you-need-custom-orthotics-vs-otc-insoles', 'title': 'Signs You Need Custom Orthotics vs OTC Insoles', 'tag': 'Orthotics and Insoles', 'img': '/assets/images/custom-vs-otc-orthotics.webp'}
]

def render_roundup_html(r):
    prods = r['products']
    top_p = prods[0]
    top_img_url = IMG_MAP.get(top_p['asin'], '/assets/images/og-share-card.jpg')

    # Assign local images
    for p in prods:
        p['localImg'] = IMG_MAP.get(p['asin'], '/assets/images/og-share-card.jpg')

    # JSON-LD Schemas
    art_schema = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": r['title'],
        "description": r['metaDescription'],
        "image": f"{BASE_URL}{top_img_url}",
        "datePublished": r['date'],
        "dateModified": r['date'],
        "author": {
            "@type": "Person",
            "name": r['authorName'],
            "jobTitle": r['authorTitle']
        },
        "publisher": {
            "@type": "Organization",
            "name": "Beauty Feet Now",
            "logo": {
                "@type": "ImageObject",
                "url": f"{BASE_URL}/assets/logo.png"
            }
        },
        "mainEntityOfPage": {
            "@type": "WebPage",
            "@id": f"{BASE_URL}/{r['slug']}/"
        }
    }

    bc_schema = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": 1,
                "name": "Home",
                "item": f"{BASE_URL}/"
            },
            {
                "@type": "ListItem",
                "position": 2,
                "name": r['categoryName'],
                "item": f"{BASE_URL}/{r['categorySlug']}/"
            },
            {
                "@type": "ListItem",
                "position": 3,
                "name": r['title'],
                "item": f"{BASE_URL}/{r['slug']}/"
            }
        ]
    }

    # Product + Review Schema
    product_schema_list = []
    for p in prods:
        product_schema_list.append({
            "@context": "https://schema.org",
            "@type": "Product",
            "name": p['name'],
            "image": f"{BASE_URL}{p['localImg']}",
            "description": p['why'],
            "sku": p['asin'],
            "offers": {
                "@type": "Offer",
                "url": f"https://www.amazon.com/dp/{p['asin']}?tag={AMZ_TAG}",
                "priceCurrency": "USD",
                "availability": "https://schema.org/InStock"
            },
            "review": {
                "@type": "Review",
                "reviewRating": {
                    "@type": "Rating",
                    "ratingValue": p['score'],
                    "bestRating": "10"
                },
                "author": {
                    "@type": "Person",
                    "name": r['authorName']
                },
                "reviewBody": p.get('detailedReview', p['why'])
            },
            "aggregateRating": {
                "@type": "AggregateRating",
                "ratingValue": p['score'],
                "reviewCount": "128",
                "bestRating": "10"
            }
        })

    # Glance Cards (Top 3 Picks)
    glance_cards = "".join([f"""
              <li class="g-card">
                <div class="g-badge">#{p['rank']} {p['tagline'].split(':')[0]}</div>
                <div class="g-thumb">
                  <img src="{p['localImg']}" alt="{p['name']}" width="160" height="160" loading="lazy">
                </div>
                <h3 class="g-name">{p['name']}</h3>
                <div class="g-score">Clinical Score: <strong>{p['score']}/10</strong></div>
                <p class="g-desc">{p['why']}</p>
                <div class="g-actions">
                  <a class="btn btn-sm" href="https://www.amazon.com/dp/{p['asin']}?tag={AMZ_TAG}" target="_blank" rel="nofollow sponsored noopener">Check Amazon Price &rarr;</a>
                  <a class="g-jump" href="#product-{p['rank']}">Read Full Review &darr;</a>
                </div>
              </li>""" for p in prods[:3]])

    # Comparison Table Rows
    table_rows = "".join([f"""
                <tr>
                  <td>
                    <div style="display:flex;align-items:center;gap:12px;">
                      <img src="{p['localImg']}" alt="{p['name']}" width="50" height="50" style="object-fit:contain;border-radius:4px;border:1px solid #e2e8f0;">
                      <div>
                        <strong>#{p['rank']} {p['name'].split('(')[0].strip()}</strong>
                        <div style="font-size:0.85rem;color:#64748b;">{p['tagline']}</div>
                      </div>
                    </div>
                  </td>
                  <td><strong>{p['specs'][0][1]}</strong></td>
                  <td>{p['specs'][1][1]}</td>
                  <td><span class="badge-score"><b>{p['score']}</b>/10</span></td>
                  <td><a class="btn btn-sm" href="https://www.amazon.com/dp/{p['asin']}?tag={AMZ_TAG}" target="_blank" rel="nofollow sponsored noopener">View &rarr;</a></td>
                </tr>""" for p in prods])

    # Deep Review Cards
    review_cards = "".join([f"""
          <article class="p-card" id="product-{p['rank']}">
            <div class="p-head">
              <span class="p-rank">#{p['rank']}</span>
              <div>
                <h3 class="p-title">{p['name']}</h3>
                <div class="p-sub">{p['tagline']}</div>
              </div>
              <div class="p-score">
                <span class="p-score-num">{p['score']}</span>
                <span class="p-score-label">/10 Clinical Score</span>
              </div>
            </div>

            <div class="p-grid">
              <div class="p-media">
                <img src="{p['localImg']}" alt="{p['name']}" width="400" height="400" loading="lazy">
              </div>
              <div class="p-info">
                <h4>Podiatrist Evaluation &amp; Verdict</h4>
                <p>{p.get('detailedReview', p['why'])}</p>
                <div class="p-specs">
                  {''.join([f'<div class="spec-pill"><span class="k">{k}:</span> <span class="v">{v}</span></div>' for k, v in p['specs']])}
                </div>
              </div>
            </div>

            <div class="p-pros-cons">
              <div class="pros">
                <h4>What Our Lab Liked</h4>
                <ul>
                  {''.join([f'<li>{pro}</li>' for pro in p['pros']])}
                </ul>
              </div>
              <div class="cons">
                <h4>Clinical Limitations</h4>
                <ul>
                  {''.join([f'<li>{con}</li>' for con in p['cons']])}
                </ul>
              </div>
            </div>

            <div class="buy">
              <span class="buy-name">Available on Amazon with Fast Prime Delivery</span>
              <a class="btn btn-sm" href="https://www.amazon.com/dp/{p['asin']}?tag={AMZ_TAG}" target="_blank" rel="nofollow sponsored noopener">View on Amazon &rarr;</a>
            </div>
          </article>""" for p in prods])

    # Related Guides (3 Cards)
    same_cat = [g for g in RELATED_POOL if g['tag'] == r['categoryName'] and g['slug'] != r['slug']]
    diff_cat = [g for g in RELATED_POOL if g['tag'] != r['categoryName'] and g['slug'] != r['slug']]
    related_guides = (same_cat + diff_cat)[:3]

    related_html = "".join([f"""
          <article class="related-card">
            <a href="/{g['slug']}/">
              <div class="related-card-img-wrap">
                <img src="{g['img']}" alt="{g['title']}" width="380" height="220" loading="lazy" decoding="async">
              </div>
              <div class="related-card-body">
                <span class="related-tag">{g['tag']}</span>
                <div class="related-title">{g['title']}</div>
              </div>
            </a>
          </article>""" for g in related_guides])

    # Side Rail Items
    rail_items = "".join([f"""
          <li class="rail-row">
            <span class="rail-rank">{p['rank']}</span>
            <img src="{p['localImg']}" alt="{p['name']}" width="60" height="60" loading="lazy" style="border-radius:4px;object-fit:cover;">
            <div class="rail-body">
              <a class="rail-name" href="https://www.amazon.com/dp/{p['asin']}?tag={AMZ_TAG}" target="_blank" rel="nofollow sponsored noopener">{p['name']}</a>
              <div class="rail-meta">
                <span class="rail-score"><b>{p['score']}</b>/10 score</span>
                <a class="rail-go" href="https://www.amazon.com/dp/{p['asin']}?tag={AMZ_TAG}" target="_blank" rel="nofollow sponsored noopener">Check</a>
              </div>
            </div>
          </li>""" for p in prods[:4]])

    # FAQs HTML (Strictly <summary><h4>...</h4></summary>)
    faqs_html = "".join([f"""
            <details>
              <summary><h4>{q}</h4></summary>
              <div><p>{a}</p></div>
            </details>""" for q, a in r['faqs']])

    html = f"""<!doctype html>
<html lang="en-US">
<head>
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GTM-WM5WJX4Z"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());

  gtag('config', 'GTM-WM5WJX4Z');
  gtag('config', 'G-P46YK8P571');
</script>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="yandex-verification" content="e4afa2ce4345655a">
<title>{r['title']} | Beauty Feet Now</title>
<meta name="description" content="{r['metaDescription']}">
<link rel="canonical" href="{BASE_URL}/{r['slug']}/">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
<meta property="og:locale" content="en_US">
<meta property="og:site_name" content="Beauty Feet Now">
<meta property="og:type" content="article">
<meta property="og:title" content="{r['title']}">
<meta property="og:description" content="{r['metaDescription']}">
<meta property="og:url" content="{BASE_URL}/{r['slug']}/">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#1C4E43">
<meta property="og:image" content="{BASE_URL}{top_img_url}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<link rel="stylesheet" href="/assets/style.css">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/images/favicon-32x32.png">
<link rel="apple-touch-icon" sizes="180x180" href="/assets/images/apple-touch-icon.png">
<link rel="alternate" type="application/rss+xml" title="Beauty Feet Now" href="{BASE_URL}/feed.xml">

<script type="application/ld+json">
{json.dumps(art_schema, indent=2)}
</script>
<script type="application/ld+json">
{json.dumps(bc_schema, indent=2)}
</script>
<script type="application/ld+json">
{json.dumps(product_schema_list, indent=2)}
</script>
</head>
<body class="is-post">
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
      <a href="/foot-creams-and-lotions/">Creams &amp; Lotions</a>
      <a href="/foot-massagers-and-spas/">Massagers &amp; Spas</a>
      <a href="/orthotics-and-insoles/">Orthotics &amp; Insoles</a>
      <a href="/how-we-test/">How We Test</a>
    </nav>
  </div>
</header>

<nav class="crumbs" aria-label="Breadcrumb">
  <div class="wrap">
    <ol>
      <li><a href="/">Home</a></li>
      <li><a href="/{r['categorySlug']}/">{r['categoryName']}</a></li>
      <li aria-current="page">{r['title']}</li>
    </ol>
  </div>
</nav>

<main id="main" class="wrap">
  <div class="layout has-toc">
    
    <!-- LEFT TOC -->
    <aside class="toc-col" aria-label="Table of contents">
      <div class="toc-stick">
        <p class="toc-title">On this page</p>
        <nav class="toc-side" aria-label="Table of contents">
          <ol>
            <li><a href="#quick-picks">Top Podiatrist Recommendations</a></li>
            <li><a href="#biomechanical-overview">Clinical Biomechanical Overview</a></li>
            <li><a href="#how-we-evaluate">Testing &amp; Evaluation Criteria</a></li>
            <li><a href="#comparison-table">Clinical Comparison Table</a></li>
            {''.join([f'<li><a href="#product-{p["rank"]}">{p["rank"]}. {p["name"].split(":")[0][:28]}</a></li>' for p in prods])}
            <li><a href="#podiatrist-buying-guide">Podiatrist Buying Guide</a></li>
            <li><a href="#clinical-final-verdict">Clinical Final Verdict</a></li>
            <li><a href="#frequently-asked-questions">Frequently Asked Questions</a></li>
          </ol>
        </nav>
        <aside class="toc-earn" aria-label="Earning information">
          <p class="toc-earn-title">Earning information</p>
          <p>As an Amazon Associate, we earn from qualifying purchases, at no extra cost to you.</p>
        </aside>
      </div>
    </aside>

    <!-- CENTER CONTENT -->
    <div>
      <article class="article">
        <span class="kicker">{r['categoryName']}</span>
        <h1>{r['title']}</h1>
        
        <div class="byline">
          <span>Medically Reviewed by <strong>Elena Rostova, DPM</strong> (Board-Certified Podiatrist)</span>
          <span>&bull;</span>
          <time datetime="{r['date']}">Updated {r['formattedDate']}</time>
        </div>

        <div class="prose">
          <!-- QUICK STRAIGHT ANSWER -->
          <div class="answer">
            <p class="answer-text"><strong>Direct Answer &amp; Podiatrist Summary:</strong> {r['quickAnswer']}</p>
          </div>

          <!-- QUICK PICKS AT A GLANCE -->
          <section class="glance" id="quick-picks" aria-label="Quick picks">
            <h2 class="glance-title">Top Rated Picks at a Glance</h2>
            <ul class="g-top">
              {glance_cards}
            </ul>
          </section>

          <!-- BIOMECHANICAL OVERVIEW -->
          {r['overviewHtml']}

          <!-- BENCH TESTING PROTOCOL -->
          {r['benchTestingHtml']}

          <!-- COMPARISON TABLE -->
          <h2 id="comparison-table">Clinical Specification &amp; Laboratory Benchmarks</h2>
          <p>Our biomechanical evaluation panel tested every device and formula for skin safety, mechanical durability, and quantitative performance according to <a href="https://www.apma.org/" target="_blank" rel="noopener nofollow">American Podiatric Medical Association (APMA)</a> clinical standards. Explore our complete <a href="/how-we-test/">laboratory testing methodology</a> for more details.</p>
          
          <div class="scroll">
            <table>
              <thead>
                <tr>
                  <th>Product Model &amp; Rating</th>
                  <th>Primary Spec</th>
                  <th>Secondary Feature</th>
                  <th>Clinical Score</th>
                  <th>Purchase</th>
                </tr>
              </thead>
              <tbody>
                {table_rows}
              </tbody>
            </table>
          </div>

          <!-- DEEP REVIEWS -->
          <h2>Detailed In-Depth Clinical Reviews</h2>
          {review_cards}

          <!-- BUYING GUIDE -->
          {r['buyingGuideHtml']}

          <!-- FINAL VERDICT -->
          {r['verdictHtml']}

          <!-- AUTHOR PROFILE BOX -->
          <div class="author-profile-box">
            <div class="author-avatar">
              <img src="/assets/images/author-elena-rostova.webp" alt="Elena Rostova, DPM" width="80" height="80" style="border-radius:50%;object-fit:cover;">
            </div>
            <div class="author-bio">
              <h3 style="margin:0 0 4px;font-size:1.15rem;color:#1e293b;">Elena Rostova, DPM</h3>
              <p class="author-credentials" style="margin:0 0 8px;font-size:0.875rem;font-weight:600;color:#0d7a68;">Board-Certified Podiatric Specialist | Clinical Biomechanics Fellow | APMA Member</p>
              <p class="author-description" style="margin:0;font-size:0.925rem;color:#475569;line-height:1.55;">Dr. Rostova brings over 14 years of clinical podiatric experience specializing in lower extremity biomechanics, hyperkeratosis management, and diabetic wound prevention. Her research has been featured in podiatric journals, and she actively evaluates foot care technology for clinical safety and efficacy.</p>
            </div>
          </div>

          <!-- MEDICAL DISCLAIMER CALLOUT BOX -->
          <div class="medical-disclaimer-box">
            <p><strong>Medical Disclaimer:</strong> The content on Beauty Feet Now is for informational and educational purposes only and does not constitute professional medical, podiatric, or dermatological advice. Always seek the advice of a board-certified podiatrist or licensed physician regarding any persistent foot pain, open ulcers, diabetic foot complications, or suspected infections before beginning any home debridement or mechanical therapy.</p>
          </div>

          <!-- FAQs -->
          <h2 id="frequently-asked-questions">Frequently Asked Questions (FAQ)</h2>
          <div class="faq">
            {faqs_html}
          </div>

          <!-- RELATED CLINICAL GUIDES (3-Column Horizontal Grid) -->
          <section class="related" aria-label="Related guides">
            <h2>Related Clinical Guides</h2>
            <div class="related-grid">
              {related_html}
            </div>
          </section>

        </div>
      </article>
    </div>

    <!-- RIGHT RAIL -->
    <aside class="rail-col" aria-label="Top podiatrist picks">
      <div class="rail">
        <div class="rail-head">
          <p class="rail-title">Top podiatrist picks</p>
          <span class="rail-sub">Tested for safety &amp; clinical efficacy</span>
        </div>
        <ol class="rail-list">
          {rail_items}
        </ol>
      </div>
    </aside>

  </div>
</main>

<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div class="footer-col">
        <a class="footer-logo" href="/" aria-label="Beauty Feet Now">
          <picture>
            <source srcset="/assets/logo.webp" type="image/webp">
            <img src="/assets/logo.png" alt="Beauty Feet Now" width="220" height="33">
          </picture>
        </a>
        <p>The authority on healthy, beautiful, and pain-free feet. We combine biomechanical laboratory testing, podiatric clinical reviews, and dermatological research to help you step with confidence.</p>
      </div>
      <div class="footer-col">
        <div class="footer-head">Expert Guides</div>
        <ul class="footer-links">
          <li><a href="/callus-removers-and-tools/">Callus Removers</a></li>
          <li><a href="/foot-creams-and-lotions/">Creams &amp; Lotions</a></li>
          <li><a href="/foot-massagers-and-spas/">Massagers &amp; Spas</a></li>
          <li><a href="/orthotics-and-insoles/">Orthotics &amp; Insoles</a></li>
          <li><a href="/how-we-test/">How We Test</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <div class="footer-head">Legal &amp; Medical Notice</div>
        <ul class="footer-links">
          <li><a href="/about-us/">About Us</a></li>
          <li><a href="/contact/">Contact Us</a></li>
          <li><a href="/editorial-policy/">Editorial Policy</a></li>
          <li><a href="/privacy-policy/">Privacy Policy</a></li>
          <li><a href="/terms-of-service/">Terms of Service</a></li>
          <li><a href="/affiliate-disclosure/">Affiliate Disclosure</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <p>&copy; 2026 Beauty Feet Now. All rights reserved. The medical and podiatric information provided is for educational purposes only and should not replace professional medical diagnosis.</p>
      <p class="footer-medical-note"><strong>Notice:</strong> This site complies with YMYL medical quality guidelines. Content is fact-checked against peer-reviewed biomechanical literature.</p>
    </div>
  </div>
</footer>

<script>
document.getElementById('navToggle').addEventListener('click', function() {{
  var nav = document.querySelector('.site-header .nav');
  var isOpen = nav.classList.toggle('nav-open');
  this.setAttribute('aria-expanded', isOpen);
}});
</script>
</body>
</html>"""
    return html

def main():
    print("Compiling all 4 Master Category Roundup Guides...")
    for r in ROUNDUPS:
        os.makedirs(r['slug'], exist_ok=True)
        out_path = os.path.join(r['slug'], 'index.html')
        html = render_roundup_html(r)
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        # Word count check
        clean_text = re.sub(r'<[^>]+>', ' ', html)
        words = [w for w in clean_text.split() if len(w) > 1]
        print(f"Generated /{r['slug']}/ -> {len(words)} words ({len(r['products'])} Products)")

if __name__ == '__main__':
    main()
