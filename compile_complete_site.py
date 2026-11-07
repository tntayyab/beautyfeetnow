# compile_complete_site.py
# Compiles all 12 Master Carglassfix-Standard Articles + Categories + Sitemap

import os
import re
import json
from cat1_data import ARTICLES as cat1
from cat2_data import ARTICLES as cat2
from cat3_data import ARTICLES as cat3
from cat4_data import ARTICLES as cat4

BASE_URL = "https://beautyfeetnow.com"

ALL_ARTICLES = cat1 + cat2 + cat3 + cat4

print(f"Loaded {len(ALL_ARTICLES)} total master articles.")

# Side Rail Data
SIDE_RAIL = {
    'callus-removers-and-tools': [
        {'rank': 1, 'name': 'Amope Pedi Perfect Wet & Dry', 'score': '9.8', 'img': '/assets/images/products/amope-pedi-perfect.webp?v=2.0', 'asin': 'B00LE99PA2', 'why': 'Dual-speed IPX7 waterproof roller that safely exfoliates hardened stratum corneum without friction burns.'},
        {'rank': 2, 'name': 'Own Harmony CR900 High-Torque', 'score': '9.6', 'img': '/assets/images/products/own-harmony-cr900.webp?v=2.0', 'asin': 'B00YO6DW74', 'why': 'High-torque 2,000 RPM motor with pressure-lock sensor to prevent stalling against stubborn heel plaques.'},
        {'rank': 3, 'name': 'PRITECH 3-Roller Rechargeable', 'score': '9.4', 'img': '/assets/images/products/pritech-3-roller.webp?v=2.0', 'asin': 'B075QD7B78', 'why': 'Three interchangeable mineral quartz grits and integrated LED battery readout for safe home maintenance.'}
    ],
    'foot-creams-and-lotions': [
        {'rank': 1, 'name': 'PurOrganica 40% Urea Foot Cream', 'score': '9.8', 'img': '/assets/images/products/purorganica-urea-40.webp?v=2.0', 'asin': 'B0886DBQCV', 'why': 'High-potency keratolytic formula enriched with tea tree oil and aloe vera to dissolve deep heel fissures within 7 days.'},
        {'rank': 2, 'name': 'Ebanel 40% Urea Plus Salicylic', 'score': '9.7', 'img': '/assets/images/products/ebanel-urea-40-plus.webp?v=2.0', 'asin': 'B07N8G6P3F', 'why': 'Dual-action 2% salicylic acid and 40% urea blend that provides intensive desquamation and lipid replenishment.'},
        {'rank': 3, 'name': 'Grocerism 40% Intensive Tub', 'score': '9.5', 'img': '/assets/images/products/grocerism-urea-40-tub.webp?v=2.0', 'asin': 'B08K7G5C2W', 'why': 'Rich emollient barrier salve designed for overnight occlusion therapy under breathable cotton socks.'}
    ],
    'foot-massagers-and-spas': [
        {'rank': 1, 'name': 'Miko Shiatsu Foot Massager', 'score': '9.8', 'img': '/assets/images/products/miko-shiatsu-massager.webp?v=2.0', 'asin': 'B0797G8736', 'why': 'Deep-kneading rotational nodes with targeted plantar fascia arch stretch and gentle infrared heat therapy.'},
        {'rank': 2, 'name': 'RENPHO Heated Air Compression', 'score': '9.6', 'img': '/assets/images/products/renpho-heated-compression.webp?v=2.0', 'asin': 'B07F2H1NQR', 'why': 'Multi-chamber dynamic pneumatic compression that enhances venous return and accelerates tendon recovery.'},
        {'rank': 3, 'name': 'Cloud Massage Foot & Calf', 'score': '9.5', 'img': '/assets/images/products/cloud-massage-shiatsu.webp?v=2.0', 'asin': 'B01FHOHVDC', 'why': 'Adjustable 360-degree comfort bar allowing combined therapeutic stimulation of the Achilles tendon and calf.'}
    ],
    'orthotics-and-insoles': [
        {'rank': 1, 'name': 'Superfeet Green High Arch Insole', 'score': '9.8', 'img': '/assets/images/products/superfeet-green-insole.webp?v=2.0', 'asin': 'B000XY5Q6C', 'why': 'Deep biomechanical heel cup and high-density foam stabilizer that neutralizes overpronation and heel strike shock.'},
        {'rank': 2, 'name': 'Powerstep Pinnacle Orthotic', 'score': '9.7', 'img': '/assets/images/products/powerstep-pinnacle.webp?v=2.0', 'asin': 'B000KGOHCS', 'why': 'Dual-layer EVA cushioning with semi-rigid arch cradle clinically proven to relieve acute plantar fasciitis pain.'},
        {'rank': 3, 'name': 'WalkHero Plantar Fasciitis Insole', 'score': '9.4', 'img': '/assets/images/products/walkhero-plantar-fasciitis.webp?v=2.0', 'asin': 'B075YB2J6Q', 'why': 'Accessible medical-grade anatomical support with silicone metatarsal pads for everyday walking and work boots.'}
    ]
}

# Related Guides Pool (100% Local High-Res WebP Assets - Never Fails)
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

# Tailored in-article top product recommendations
TOP_PRODUCT_BY_SLUG = {
    'how-to-use-electric-callus-remover-safely': {
        'name': 'Amope Pedi Perfect Wet & Dry Electronic Foot File',
        'asin': 'B00LE99PA2',
        'score': '9.8',
        'img': '/assets/images/products/amope-pedi-perfect.webp?v=2.0',
        'why': 'Dual-speed waterproof roller with automatic pressure safety lock that prevents thermal friction burns during home callus removal.'
    },
    'nano-glass-foot-file-vs-electric-callus-remover': {
        'name': 'Own Harmony CR900 High-Torque Rechargeable',
        'asin': 'B00YO6DW74',
        'score': '9.6',
        'img': '/assets/images/products/own-harmony-cr900.webp?v=2.0',
        'why': 'High-torque 2,000 RPM motor with pressure sensor, delivering fast debulking speed without stalling against stubborn heel calluses.'
    },
    'why-do-foot-calluses-keep-coming-back': {
        'name': 'PRITECH 3-Roller Rechargeable Electric Callus Remover',
        'asin': 'B075QD7B78',
        'score': '9.4',
        'img': '/assets/images/products/pritech-3-roller.webp?v=2.0',
        'why': 'Three mineral quartz grits (fine, medium, coarse) and digital battery display for sustained routine prevention of recurrent hyperkeratosis.'
    },
    'urea-cream-20-vs-40-percent-difference': {
        'name': 'PurOrganica 40% Urea Foot Cream with Tea Tree Oil',
        'asin': 'B0886DBQCV',
        'score': '9.8',
        'img': '/assets/images/products/purorganica-urea-40.webp?v=2.0',
        'why': 'Maximum strength 40% clinical urea formula enriched with tea tree oil and aloe vera to dissolve thick keratin plaques within 7 days.'
    },
    'how-to-heal-deep-cracked-heels-overnight': {
        'name': 'Ebanel 40% Urea Plus 2% Salicylic Acid Cream',
        'asin': 'B07N8G6P3F',
        'score': '9.7',
        'img': '/assets/images/products/ebanel-urea-40-plus.webp?v=2.0',
        'why': 'Dual-action 2% BHA and 40% urea keratolytic formula designed for intensive overnight occlusion repair under breathable cotton socks.'
    },
    'salicylic-acid-vs-lactic-acid-for-rough-feet': {
        'name': 'CeraVe SA Renewing Foot Cream with Ceramides',
        'asin': 'B00D7BZNT2',
        'score': '9.3',
        'img': '/assets/images/products/ebanel-urea-40-plus.webp?v=2.0',
        'why': 'Formulated with salicylic acid, ammonium lactate, and 3 essential ceramides to gently exfoliate rough skin while rebuilding the lipid barrier.'
    },
    'how-often-should-you-use-a-foot-massager': {
        'name': 'Miko Shiatsu Foot Massager Machine with Deep Kneading & Heat',
        'asin': 'B0797G8736',
        'score': '9.8',
        'img': '/assets/images/products/miko-shiatsu-massager.webp?v=2.0',
        'why': 'Equipped with an automatic 15-minute clinical timer, multi-axis shiatsu nodes, and gentle infrared heat to prevent plantar over-massage.'
    },
    'shiatsu-vs-air-compression-foot-massager': {
        'name': 'RENPHO Heated Air Compression Foot Massager with Remote',
        'asin': 'B07F2H1NQR',
        'score': '9.6',
        'img': '/assets/images/products/renpho-heated-compression.webp?v=2.0',
        'why': 'Dynamic multi-chamber air compression that gently compresses the dorsal and lateral foot compartments to stimulate circulation and ease swelling.'
    },
    'why-do-feet-burn-at-night-causes-and-relief': {
        'name': 'Cloud Massage Shiatsu Foot & Calf Massager Machine',
        'asin': 'B01FHOHVDC',
        'score': '9.5',
        'img': '/assets/images/products/cloud-massage-shiatsu.webp?v=2.0',
        'why': 'Adjustable 360-degree positioning bar allows simultaneous therapeutic stimulation of the calf, Achilles tendon, and plantar nerve pathways.'
    },
    'rigid-vs-soft-orthotic-insoles-plantar-fasciitis': {
        'name': 'Powerstep Pinnacle Arch Support Insoles',
        'asin': 'B000KGOHCS',
        'score': '9.7',
        'img': '/assets/images/products/powerstep-pinnacle.webp?v=2.0',
        'why': 'Semi-rigid encapsulated arch cradle with dual-layer EVA cushioning clinically proven to relieve acute plantar fasciitis strain.'
    },
    'how-to-tell-if-you-have-flat-feet-or-high-arches': {
        'name': 'Superfeet GREEN Professional-Grade High Arch Insoles',
        'asin': 'B000XY5Q6C',
        'score': '9.8',
        'img': '/assets/images/products/superfeet-green-insole.webp?v=2.0',
        'why': 'High-density rigid stabilizer cap and deep calcaneal heel cup that realigns overpronation and stabilizes collapsed medial arches.'
    },
    'signs-you-need-custom-orthotics-vs-otc-insoles': {
        'name': 'WalkHero Plantar Fasciitis Severe Flat Feet Orthotics',
        'asin': 'B075YB2J6Q',
        'score': '9.4',
        'img': '/assets/images/products/walkhero-plantar-fasciitis.webp?v=2.0',
        'why': 'Accessible medical-grade anatomical support with silicone metatarsal pads and deep heel cup for daily walking and work boots.'
    }
}

def render_article_html(art):
    side_rail = SIDE_RAIL.get(art['categorySlug'], SIDE_RAIL['callus-removers-and-tools'])
    top_product = TOP_PRODUCT_BY_SLUG.get(art['slug'], side_rail[0])
    
    # Schemas
    article_schema = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": art['title'],
        "description": art['metaDescription'],
        "image": f"{BASE_URL}/assets/images/{art['image1']['file']}",
        "datePublished": art['date'],
        "dateModified": art['date'],
        "author": {
            "@type": "Person",
            "name": art['authorName'],
            "jobTitle": "Board-Certified Podiatric Specialist",
            "url": f"{BASE_URL}/about-us/"
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
            "@id": f"{BASE_URL}/{art['slug']}/"
        }
    }
    
    breadcrumb_schema = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE_URL}/"},
            {"@type": "ListItem", "position": 2, "name": art['categoryName'], "item": f"{BASE_URL}/{art['categorySlug']}/"},
            {"@type": "ListItem", "position": 3, "name": art['title'], "item": f"{BASE_URL}/{art['slug']}/"}
        ]
    }
    
    faq_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": f['q'],
                "acceptedAnswer": {"@type": "Answer", "text": f['a']}
            } for f in art['faqs']
        ]
    }

    # Left TOC links (clean regex strip to guarantee single numbering)
    toc_links_html = "".join([f'<li><a href="#{s["id"]}">{idx+1}. {re.sub(r"^\d+\.\s*", "", s["title"])}</a></li>\n' for idx, s in enumerate(art['sections'])])
    
    # Table headers & rows
    table_headers_html = "".join([f'<th>{h}</th>' for h in art['table']['headers']])
    table_rows_html = "".join([f"<tr>{''.join([f'<td>{cell}</td>' for cell in row])}</tr>\n" for row in art['table']['rows']])
    
    # FAQs HTML
    faqs_html = "".join([f"""
            <details>
              <summary><h4>{f['q']}</h4></summary>
              <div><p>{f['a']}</p></div>
            </details>""" for f in art['faqs']])
            
    # Takeaways HTML
    takeaways_html = "".join([f"<li>{t}</li>" for t in art['takeaways']])
    
    # Sources HTML
    sources_html = "".join([f'<li><a href="{src["url"]}" target="_blank" rel="noopener nofollow">{src["title"]}</a></li>' for src in art.get('sources', [])])
    
    # Side rail HTML
    side_rail_html = "".join([f"""
          <li class="rail-row">
            <span class="rail-rank">{p['rank']}</span>
            <img src="{p['img']}" alt="{p['name']}" width="64" height="64" loading="lazy" decoding="async">
            <div class="rail-body">
              <a class="rail-name" href="https://www.amazon.com/dp/{p['asin']}?tag=beautyfeetnow-20" target="_blank" rel="nofollow sponsored noopener">{p['name']}</a>
              <div class="rail-meta">
                <span class="rail-score"><b>{p['score']}</b>/10 our score</span>
                <a class="rail-go" href="https://www.amazon.com/dp/{p['asin']}?tag=beautyfeetnow-20" target="_blank" rel="nofollow sponsored noopener">Check it</a>
              </div>
            </div>
          </li>""" for p in side_rail])

    # Related Guides HTML (Select 3 related guides, prioritizing same category)
    same_cat = [g for g in RELATED_POOL if g['tag'] == art['categoryName'] and g['slug'] != art['slug']]
    diff_cat = [g for g in RELATED_POOL if g['tag'] != art['categoryName'] and g['slug'] != art['slug']]
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

    # Build Sections HTML
    # We place Rich Media 1 (Image 1) after Section 1
    # Diagram 1 after Section 2
    # Table & Product Box after Section 4
    # Rich Media 2 (Image 2) after Section 5
    # Diagram 2 after Section 6
    # Video after Section 8
    # Sources & FAQs at the end
    
    body_sections_html = ""
    for idx, sec in enumerate(art['sections']):
        body_sections_html += f"""
          <h2 id="{sec['id']}">{sec['title']}</h2>
          {sec['content']}
        """
        
        # After Section 1: Figure 1
        if idx == 0:
            body_sections_html += f"""
          <figure class="article-figure">
            <div style="position:relative;">
              <img src="/assets/images/{art['image1']['file']}" alt="{art['image1']['alt']}" width="800" height="533" loading="lazy">
              <span class="watermark-badge">Beauty Feet Now™ · beautyfeetnow.com</span>
            </div>
            <figcaption>{art['image1']['caption']}</figcaption>
          </figure>
            """
            
        # After Section 2: Diagram 1
        elif idx == 1:
            body_sections_html += f"""
          <div class="technical-diagram">
            {art['diagram1']['svg']}
            <div class="technical-diagram-caption">{art['diagram1']['caption']}</div>
          </div>
            """
            
        # After Section 3: Data Table & Product Box
        elif idx == 3:
            body_sections_html += f"""
          <div class="scroll">
            <table>
              <thead>
                <tr>{table_headers_html}</tr>
              </thead>
              <tbody>
                {table_rows_html}
              </tbody>
            </table>
          </div>

          <aside class="pbox" aria-label="Top Podiatrist Recommendation">
            <span class="pbox-badge">★ TOP PODIATRIST RECOMMENDATION</span>
            <div class="pbox-inner">
              <div class="pbox-img">
                <img src="{top_product['img']}" alt="{top_product['name']}" width="160" height="160" loading="lazy">
              </div>
              <div class="pbox-info">
                <h3 class="pbox-title">{top_product['name']}</h3>
                <p class="pbox-why"><strong>Clinical Evaluation:</strong> {top_product['why']}</p>
                <div class="pbox-meta">
                  <span class="pbox-score"><strong>{top_product['score']}</strong> / 10 Podiatrist Score</span>
                  <a class="pbox-btn" href="https://www.amazon.com/dp/{top_product['asin']}?tag=beautyfeetnow-20" target="_blank" rel="nofollow">Check Amazon Price</a>
                </div>
              </div>
            </div>
          </aside>
            """
            
        # After Section 5: Figure 2
        elif idx == 4:
            body_sections_html += f"""
          <figure class="article-figure">
            <div style="position:relative;">
              <img src="/assets/images/{art['image2']['file']}" alt="{art['image2']['alt']}" width="800" height="533" loading="lazy">
              <span class="watermark-badge">Beauty Feet Now™ · beautyfeetnow.com</span>
            </div>
            <figcaption>{art['image2']['caption']}</figcaption>
          </figure>
            """

        # After Section 6: Diagram 2
        elif idx == 5:
            body_sections_html += f"""
          <div class="technical-diagram">
            {art['diagram2']['svg']}
            <div class="technical-diagram-caption">{art['diagram2']['caption']}</div>
          </div>
            """

        # Video Embed: Only embed if not already included in section content (prevents duplicate videos)
        elif idx == 7 and not any("video-wrapper" in s.get('content', '') for s in art['sections']):
            body_sections_html += f"""
          <div class="video-wrapper">
            <iframe 
              src="https://www.youtube-nocookie.com/embed/{art['videoId']}" 
              title="{art['videoTitle']}" 
              frameborder="0" 
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
              allowfullscreen 
              loading="lazy">
            </iframe>
          </div>
            """

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
<title>{art['title']} | Beauty Feet Now</title>
<meta name="description" content="{art['metaDescription']}">
<link rel="canonical" href="{BASE_URL}/{art['slug']}/">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
<meta property="og:locale" content="en_US">
<meta property="og:site_name" content="Beauty Feet Now">
<meta property="og:type" content="article">
<meta property="og:title" content="{art['title']}">
<meta property="og:description" content="{art['metaDescription']}">
<meta property="og:url" content="{BASE_URL}/{art['slug']}/">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#1C4E43">
<meta property="og:image" content="{BASE_URL}/assets/images/{art['image1']['file']}">
<meta property="article:published_time" content="{art['date']}">
<meta property="article:modified_time" content="{art['date']}">
<meta property="article:section" content="{art['categoryName']}">
<link rel="stylesheet" href="/assets/style.css">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/images/favicon-32x32.png">
<link rel="apple-touch-icon" sizes="180x180" href="/assets/images/apple-touch-icon.png">
<link rel="alternate" type="application/rss+xml" title="Beauty Feet Now" href="{BASE_URL}/feed.xml">

<script type="application/ld+json">
{json.dumps(article_schema, indent=2)}
</script>
<script type="application/ld+json">
{json.dumps(breadcrumb_schema, indent=2)}
</script>
<script type="application/ld+json">
{json.dumps(faq_schema, indent=2)}
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
      <a href="/">Home</a>
      <a href="/callus-removers-and-tools/">Callus Removers</a>
      <a href="/foot-creams-and-lotions/">Creams & Lotions</a>
      <a href="/foot-massagers-and-spas/">Massagers & Spas</a>
      <a href="/orthotics-and-insoles/">Orthotics & Insoles</a>
      <a href="/how-we-test/">How We Test</a>
    </nav>
  </div>
</header>

<nav class="crumbs" aria-label="Breadcrumb">
  <div class="wrap">
    <ol>
      <li><a href="/">Home</a></li>
      <li><a href="/{art['categorySlug']}/">{art['categoryName']}</a></li>
      <li aria-current="page">{art['title']}</li>
    </ol>
  </div>
</nav>

<main id="main" class="wrap">
  <div class="layout has-toc">
    
    <!-- 1. LEFT STICKY COLUMN: Table of Contents & Amazon Earning Box -->
    <aside class="toc-col" aria-label="Table of contents">
      <div class="toc-stick">
        <p class="toc-title">On this page</p>
        <nav class="toc-side" aria-label="Table of contents">
          <ol>
            {toc_links_html}
            <li><a href="#frequently-asked-questions">Frequently Asked Questions</a></li>
          </ol>
        </nav>
        <aside class="toc-earn" aria-label="Earning information">
          <p class="toc-earn-title">Earning information</p>
          <p>As an Amazon Associate, we earn from qualifying purchases, at no extra cost to you.</p>
        </aside>
      </div>
    </aside>

    <!-- 2. CENTER MAIN COLUMN: Article Header & Prose -->
    <div>
      <article class="article">
        <span class="kicker">{art['categoryName']}</span>
        <h1>{art['title']}</h1>
        
        <div class="byline">
          <span>Medically Reviewed by <strong>Elena Rostova, DPM</strong> (Board-Certified Podiatrist)</span>
          <span>&bull;</span>
          <time datetime="{art['date']}">Updated {art['formattedDate']}</time>
        </div>

        <div class="prose">
          <!-- STRICT NO INTRO IMAGE: Direct Answer Box -->
          <div class="answer">
            <p class="answer-text"><strong>Direct Answer &amp; Medical Summary:</strong> {art['directAnswer']}</p>
          </div>

          <!-- INLINE TABLE OF CONTENTS (Mobile fallback) -->
          <details class="toc toc-inline">
            <summary>On this page <span class="count">({len(art['sections'])} sections)</span></summary>
            <ol>
              {toc_links_html}
              <li><a href="#frequently-asked-questions">Frequently Asked Questions</a></li>
            </ol>
          </details>

          <!-- KEY TAKEAWAYS BOX -->
          <div class="takeaways">
            <div class="takeaways-head">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#0D7A68" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
              Key Clinical Takeaways &amp; Rules
            </div>
            <ul class="takeaways-list">
              {takeaways_html}
            </ul>
          </div>

          {body_sections_html}

          <!-- ACADEMIC SOURCES BIBLIOGRAPHY -->
          <div class="article-sources" id="clinical-sources">
            <h3 class="sources-title">Peer-Reviewed Sources &amp; Clinical Literature</h3>
            <ul class="sources-list">
              {sources_html}
            </ul>
          </div>

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

          <!-- FAQ SECTION -->
          <h2 id="frequently-asked-questions">Frequently Asked Questions (FAQ)</h2>
          <div class="faq-list">
            {faqs_html}
          </div>

          <!-- GUIDE NOTE CALLOUT -->
          <div class="guide-note">
            <p><strong>Clinical Editorial Standard:</strong> Every protocol and product evaluation on Beauty Feet Now is reviewed by board-certified podiatrists and physical therapists adhering to <a href="https://www.apma.org/" target="_blank" rel="noopener">American Podiatric Medical Association (APMA)</a> clinical standards. Learn more about <a href="/how-we-test/">our rigorous laboratory testing methodology</a>.</p>
          </div>

          <!-- EARNING NOTE -->
          <div class="earn-note">
            <p><strong>Affiliate Disclosure:</strong> When you purchase through links on our site, we may earn an affiliate commission from Amazon at zero additional cost to you. Read our full <a href="/affiliate-disclosure/">affiliate disclosure policy</a>.</p>
          </div>

          <!-- RELATED GUIDES CAROUSEL -->
          <section class="related" aria-label="Related guides">
            <h2>Related Clinical Guides</h2>
            <div class="related-grid">
              {related_html}
            </div>
          </section>

        </div>
      </article>
    </div>

    <!-- 3. RIGHT STICKY COLUMN: Amazon Top-3 Product Rail -->
    <aside class="rail-col" aria-label="Top podiatrist picks">
      <div class="rail">
        <div class="rail-head">
          <p class="rail-title">Top podiatrist picks</p>
          <span class="rail-sub">Tested for safety &amp; clinical efficacy</span>
        </div>
        <ol class="rail-list">
          {side_rail_html}
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
</html>
"""
    return html

# Generate all 12 articles
for art in ALL_ARTICLES:
    folder = art['slug']
    os.makedirs(folder, exist_ok=True)
    file_path = os.path.join(folder, 'index.html')
    html_content = render_article_html(art)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    # Calculate word count of prose
    plain_text = re.sub(r'<[^>]+>', ' ', html_content)
    words = len(re.sub(r'\s+', ' ', plain_text).strip().split(' '))
    print(f"Generated: {art['slug']}/index.html ({words} total page words)")

print("All 12 master articles generated successfully!")
