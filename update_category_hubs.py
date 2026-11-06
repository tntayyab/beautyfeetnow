# update_category_hubs.py
# Generates all 4 Category Hub Pages with 400-600 words of clinical intro prose,
# local WebP thumbnails, responsive hamburger nav, icon suite, and YMYL compliance.

import os, re

BASE_URL = "https://beautyfeetnow.com"

CATEGORIES = [
    {
        "slug": "callus-removers-and-tools",
        "title": "Callus Removers & Exfoliation Tools",
        "metaDescription": "Clinical guide to electric foot callus removers, nano-glass files, and medical debridement tools. Compare rotational torque, quartz grit safety, and APMA-aligned protocols.",
        "kicker": "Category Hub · Clinical Biomechanics",
        "h1": "Callus Removers & Mechanical Exfoliation Tools",
        "lead": "Evidence-based clinical protocols and lab-tested reviews for managing plantar hyperkeratosis, calcaneal fissures, and stubborn corns safely at home without tissue trauma.",
        "introProse": """
          <div class="category-clinical-intro" style="margin:2rem 0;padding:1.75rem;background:#f8fafc;border:1px solid #e2e8f0;border-left:4px solid #0d7a68;border-radius:8px;line-height:1.7;color:#334155;">
            <h2 style="font-size:1.35rem;margin-top:0;color:#1e293b;">The Biomechanics of Plantar Hyperkeratosis &amp; Rotary Debridement Safety</h2>
            <p>Plantar calluses and intractable plantar keratoses (IPKs) develop when excessive compressive vertical forces and transverse frictional shear act on the plantar skin. During normal ambulation, ground reaction forces can exceed twice an individual's body weight during terminal stance. When abnormal gait mechanics—such as overpronation, hallux limitus, or rigid pes cavus—concentrate these forces onto focal points like the sub-metatarsal heads or the posterior calcaneal border, the basal layer of the epidermis responds defensively. Keratinocyte proliferation accelerates, causing the stratum corneum to thicken into dense, cross-linked plates of dead tissue.</p>
            <p>While physiological calluses act as biological shields against blisters, excessive hyperkeratosis loses all tissue elasticity. Under sustained hydraulic pressure from the calcaneal fat pad, thick heel plaques split open into painful calcaneal fissures. If untreated, these fissures can breach the dermal-epidermal junction, causing bleeding, agonizing pain with every heel strike, and introducing dangerous entry pathways for bacterial pathogens such as <em>Staphylococcus aureus</em> and fungal dermatophytes.</p>
            <p>Modern clinical podiatry strongly advises against outdated, hazardous home remedies such as razor blades, Credo knives, or coarse metal cheese-grater rasps. These cutting instruments lack depth control and frequently cause deep micro-lacerations that lead to severe soft-tissue infections, particularly in individuals with diabetes or peripheral vascular disease. Instead, computerized rotary electric callus removers and micro-etched Czech nano-glass files have become the gold standard for home maintenance. Operating between 1,800 and 2,400 RPM with micro-mineral quartz heads, these modern tools pulverize dead keratin into a fine dust via micro-fractional abrasion, safeguarding viable underlying dermal structures.</p>
            <p>Explore our laboratory-tested reviews and clinical how-to guides below to select the safest, most effective debridement equipment for your specific skin type and mobility level.</p>
          </div>
        """,
        "articles": [
            {
                "slug": "best-electric-callus-removers",
                "tag": "Roundup Guide · 8 Top Picks",
                "title": "8 Best Electric Callus Removers for Smooth Feet (2026)",
                "desc": "Compare top electric foot grinders by motor rotational RPM, mineral quartz grit coarseness, battery longevity, and IPX7 water resistance for effortless callus removal.",
                "img": "/assets/images/products/amope-pedi-perfect.webp?v=2.0",
                "date": "November 4, 2026"
            },
            {
                "slug": "how-to-use-electric-callus-remover-safely",
                "tag": "Clinical Protocol",
                "title": "How to Use an Electric Callus Remover Safely: Podiatrist Protocol (2026)",
                "desc": "Step-by-step clinical protocol to safely operate an electric foot file without frictional burns, over-thinning, or tissue laceration.",
                "img": "/assets/images/electric-callus-safe-use.webp",
                "date": "November 4, 2026"
            },
            {
                "slug": "nano-glass-foot-file-vs-electric-callus-remover",
                "tag": "Comparative Analysis",
                "title": "Nano Glass Foot File vs Electric Callus Remover: Which Removes Hard Skin Faster?",
                "desc": "Detailed dermatological comparison of micro-etched tempered nano-glass files versus motorized rotary diamond crystal files for hard skin removal.",
                "img": "/assets/images/nano-glass-friction.webp",
                "date": "November 4, 2026"
            },
            {
                "slug": "why-do-foot-calluses-keep-coming-back",
                "tag": "Etiology & Prevention",
                "title": "Why Do Foot Calluses Keep Coming Back? Gait & Biomechanical Causes",
                "desc": "Uncover the root biomechanical factors driving recurring plantar calluses, from subtalar overpronation and gait asymmetry to unsupportive footwear.",
                "img": "/assets/images/callus-causes-gait.webp",
                "date": "November 4, 2026"
            }
        ]
    },
    {
        "slug": "foot-creams-and-lotions",
        "title": "Foot Creams, Balms & Keratolytic Lotions",
        "metaDescription": "Clinical guide to medical foot creams containing 20% to 40% urea, salicylic acid, and ceramides. Discover dermatologically validated treatments for deep cracked heels and severe xerosis.",
        "kicker": "Category Hub · Cutaneous Pharmacology",
        "h1": "Foot Creams, Balms & Keratolytic Lotions",
        "lead": "Dermatological formulations and clinical protocols for restoring the cutaneous moisture barrier, dissolving dense keratin, and sealing deep calcaneal fissures.",
        "introProse": """
          <div class="category-clinical-intro" style="margin:2rem 0;padding:1.75rem;background:#f8fafc;border:1px solid #e2e8f0;border-left:4px solid #0d7a68;border-radius:8px;line-height:1.7;color:#334155;">
            <h2 style="font-size:1.35rem;margin-top:0;color:#1e293b;">Cutaneous Pharmacology: Keratolytic Science &amp; Epidermal Barrier Repair</h2>
            <p>The skin covering the human heel is structurally unlike any other surface on the body. It contains zero sebaceous glands, meaning it cannot produce natural sebum to maintain surface lubrication and suppleness. Instead, it relies entirely on eccrine perspiration and intracellular lipid bilayers (composed of a precise stoichiometric balance of ceramides, cholesterol, and free fatty acids) to prevent transepidermal water loss (TEWL) and preserve cutaneous elasticity.</p>
            <p>Under daily ambulatory weight-bearing, vertical impact forces flatten the subcutaneous calcaneal fat pad, stretching the overlying stratum corneum laterally. If the skin is dehydrated (calcaneal xerosis), it loses its tensile compliance. Rather than flexing, the hardened stratum corneum fractures along mechanical stress lines, producing deep, agonizing fissures that can bleed and become chronically infected. Standard cosmetic body lotions containing water, mineral oil, or low-grade glycerin cannot penetrate this hardened protein barrier.</p>
            <p>Medical resolution requires topical <strong>keratolytics</strong>, predominantly medical-grade <strong>urea (carbamide)</strong>. At therapeutic concentrations between 20% and 40%, urea alters the hydrogen bonds of keratin proteins, drawing water into compacted corneocytes and activating natural proteolytic enzymes that dissolve desmosomal cell bridges. When combined with lipid-soluble salicylic acid (BHA) to unclog pores or lactic acid (AHA) to stimulate endogenous ceramide synthesis, high-potency foot creams restore normal epidermal shedding and close painful fissures within 7 to 14 days of nightly occlusion therapy.</p>
            <p>Browse our peer-reviewed product roundups and dermatological comparison guides below to determine whether your skin requires a 20% or 40% urea regimen, acid peeling, or overnight occlusive salves.</p>
          </div>
        """,
        "articles": [
            {
                "slug": "best-cracked-heel-creams-with-urea",
                "tag": "Roundup Guide · 8 Top Picks",
                "title": "8 Best Cracked Heel Creams with Urea for Severe Fissures (2026)",
                "desc": "Compare medical-grade 20% to 40% urea heel creams and therapeutic balms evaluated for keratolytic potency, fast fissure closure, and skin barrier repair.",
                "img": "/assets/images/products/purorganica-urea-40.webp?v=2.0",
                "date": "November 4, 2026"
            },
            {
                "slug": "urea-cream-20-vs-40-percent-difference",
                "tag": "Pharmacological Guide",
                "title": "Urea Cream 20% vs 40%: Which Strength Do Your Cracked Heels Need?",
                "desc": "Understand the critical clinical difference between 20% urea for daily hydration versus 40% urea for intensive keratolytic debridement of thick plaques.",
                "img": "/assets/images/urea-concentration-skin.webp",
                "date": "November 4, 2026"
            },
            {
                "slug": "how-to-heal-deep-cracked-heels-overnight",
                "tag": "Clinical Treatment Protocol",
                "title": "How to Heal Deep Cracked Heels Overnight: Podiatrist Protocol (2026)",
                "desc": "The definitive clinical overnight occlusion protocol using high-strength urea, emollient ointments, and breathable 100% cotton socks for immediate fissure relief.",
                "img": "/assets/images/cracked-heel-recovery.webp",
                "date": "November 4, 2026"
            },
            {
                "slug": "salicylic-acid-vs-lactic-acid-for-rough-feet",
                "tag": "Dermatological Comparison",
                "title": "Salicylic Acid vs Lactic Acid Foot Peels: Which Exfoliates Hard Skin Better?",
                "desc": "Comparative analysis of beta-hydroxy acid (salicylic) and alpha-hydroxy acid (lactic) mechanisms for dissolving stubborn calluses and restoring smooth skin.",
                "img": "/assets/images/salicylic-vs-lactic-feet.webp",
                "date": "November 4, 2026"
            }
        ]
    },
    {
        "slug": "foot-massagers-and-spas",
        "title": "Foot Massagers, Heated Spas & Neuropathy Devices",
        "metaDescription": "Clinical guide to heated shiatsu foot massagers, dynamic air compression boots, and hydrotherapy spas for plantar fasciitis, heel spurs, and neuropathy relief.",
        "kicker": "Category Hub · Physical Medicine & Rehabilitation",
        "h1": "Foot Massagers, Heated Spas & Neuropathy Devices",
        "lead": "Biomechanical evaluations and physical therapy protocols for relieving plantar fascial tension, boosting microcirculation, and alleviating nocturnal burning foot pain.",
        "introProse": """
          <div class="category-clinical-intro" style="margin:2rem 0;padding:1.75rem;background:#f8fafc;border:1px solid #e2e8f0;border-left:4px solid #0d7a68;border-radius:8px;line-height:1.7;color:#334155;">
            <h2 style="font-size:1.35rem;margin-top:0;color:#1e293b;">Physical Modalities: Myofascial Release, Thermal Vasodilation &amp; Venous Return</h2>
            <p>The human foot is an extraordinary anatomical structure comprising 26 bones, 33 joints, and over 100 muscles, tendons, and ligaments. In conditions such as plantar fasciitis, chronic lower leg fatigue, and peripheral neuropathy, the plantar aponeurosis and intrinsic musculature become contracted and ischemic. Under the biomechanical windlass mechanism, tension across the plantar fascia increases during every step. When repetitive micro-trauma exceeds the regenerative capacity of collagen fibers, degenerative enthesopathy occurs at the medial calcaneal tubercle.</p>
            <p>At night, when the foot rests in a naturally plantarflexed posture, the injured fascia shortens and tightens. Upon taking the first morning steps, the sudden elongation of this contracted tissue causes sharp, stabbing pain (post-static dyskinesia). Therapeutic mechanical interventions—combining motorized rotational shiatsu kneading, rhythmic pneumatic air compression, and controlled infrared heating—address this pathological cycle directly.</p>
            <p>Deep-tissue shiatsu nodes apply cross-friction myofascial release across the medial arch, realigning disorganized collagen fibers and breaking down fibrotic scar adhesions. Concurrently, dynamic pneumatic compression cuffs stimulate the distal venous pump, flushing stagnant, edema-rich interstitial fluid out of the plantar vault and back into the circulatory system. Soothing infrared thermotherapy (104&deg;F to 118&deg;F) promotes microvascular vasodilation, flooding avascular fascial tissues with oxygenated blood, reparative fibroblasts, and metabolic nutrients to accelerate recovery.</p>
            <p>Explore our laboratory-tested equipment comparisons and clinical guidance below to find the ideal heated massager or hydrotherapy spa for your specific symptoms.</p>
          </div>
        """,
        "articles": [
            {
                "slug": "best-heated-foot-massagers-for-plantar-fasciitis",
                "tag": "Roundup Guide · 7 Top Picks",
                "title": "7 Best Heated Foot Massagers for Plantar Fasciitis Pain Relief (2026)",
                "desc": "Compare top heated electric foot massagers evaluated for rotational shiatsu node depth, infrared thermal stability, and multi-chamber air compression.",
                "img": "/assets/images/products/miko-shiatsu-massager.webp?v=2.0",
                "date": "November 4, 2026"
            },
            {
                "slug": "how-often-should-you-use-a-foot-massager",
                "tag": "Clinical Protocol",
                "title": "How Often Should You Use a Heated Foot Massager for Plantar Fasciitis?",
                "desc": "Clinical guidelines on daily session frequency, duration limits, and intensity progression to prevent fascial micro-trauma and bruising.",
                "img": "/assets/images/foot-massager-routine.webp",
                "date": "November 4, 2026"
            },
            {
                "slug": "shiatsu-vs-air-compression-foot-massager",
                "tag": "Comparative Analysis",
                "title": "Shiatsu vs Air Compression Foot Massagers: Which Relieves Heel Spurs and Neuropathy?",
                "desc": "Detailed clinical comparison of rotational deep-tissue shiatsu kneading versus pneumatic squeeze compression for heel spur pain and neuropathy.",
                "img": "/assets/images/shiatsu-vs-air-compression.webp",
                "date": "November 4, 2026"
            },
            {
                "slug": "why-do-feet-burn-at-night-causes-and-relief",
                "tag": "Neurological Diagnostics",
                "title": "Why Do Feet Burn at Night? Grierson-Gopalan Syndrome Causes & Relief Strategies",
                "desc": "Understand why feet burn and tingle at bedtime, from small fiber peripheral neuropathy and vitamin B deficiencies to circulatory pooling, with relief protocols.",
                "img": "/assets/images/burning-feet-night-relief.webp",
                "date": "November 4, 2026"
            }
        ]
    },
    {
        "slug": "orthotics-and-insoles",
        "title": "Orthotic Insoles, Arch Supports & Alignment",
        "metaDescription": "Clinical guide to rigid and semi-custom orthotic insoles for flat feet, overpronation, and plantar fasciitis. Compare arch stiffness, heel cup depth, and kinetic chain alignment.",
        "kicker": "Category Hub · Lower Extremity Biomechanics",
        "h1": "Orthotic Insoles, Arch Supports & Kinetic Alignment",
        "lead": "Biomechanical evaluations and gait analysis protocols for correcting pes planus, stabilizing the subtalar joint, and relieving knee and lower back pain.",
        "introProse": """
          <div class="category-clinical-intro" style="margin:2rem 0;padding:1.75rem;background:#f8fafc;border:1px solid #e2e8f0;border-left:4px solid #0d7a68;border-radius:8px;line-height:1.7;color:#334155;">
            <h2 style="font-size:1.35rem;margin-top:0;color:#1e293b;">Biomechanical Motion Control: Subtalar Neutral &amp; Kinetic Chain Realignment</h2>
            <p>Pes planus (flat feet)—whether congenital or acquired through adult posterior tibial tendon dysfunction (PTTD)—is one of the primary drivers of lower extremity pain syndromes. In a mechanically aligned foot, the subtalar joint pronates slightly upon initial ground contact to absorb heel strike shock, then resupinates into a rigid lever for propulsion during toe-off. In flat feet, however, the foot remains hyper-pronated throughout midstance. The calcaneus everts, the talar head drops medially and plantarward, and the navicular bone collapses toward the ground.</p>
            <p>This rearfoot instability has severe kinetic consequences throughout the entire body. Excessive pronation forces the tibia to rotate internally, altering patellofemoral tracking in the knee, contributing to iliotibial band (ITB) friction syndrome, anterior pelvic tilt, and compensatory lumbar lordosis. Furthermore, continuous tensile traction on the plantar fascia and Achilles tendon leads to chronic micro-tearing and debilitating heel spurs.</p>
            <p>The solution is not merely placing a soft foam cushion under the arch. Soft foam collapses under body weight, offering zero control over bone alignment. True corrective orthotics utilize <strong>tri-planar rearfoot motion control</strong>. By featuring a deep, semi-rigid calcaneal heel cup, the insole encapsulates the heel fat pad directly beneath the calcaneus, preventing rearfoot eversion and holding the subtalar joint in neutral. When the heel bone is stabilized, the medial longitudinal and transverse metatarsal arches are supported dynamically, restoring natural gait efficiency and eliminating pain throughout the lower kinetic chain.</p>
            <p>Explore our gait analysis evaluations, laboratory in-shoe pressure tests, and clinical selection guides below to identify the ideal orthotic insoles for your footwear and arch profile.</p>
          </div>
        """,
        "articles": [
            {
                "slug": "best-orthotic-insoles-for-flat-feet",
                "tag": "Roundup Guide · 8 Top Picks",
                "title": "9 Best Orthotic Insoles for Flat Feet & Overpronation (2026)",
                "desc": "Compare top-rated rigid and semi-rigid orthotic arch supports evaluated for calcaneal eversion control, heel cup depth, and kinetic chain alignment.",
                "img": "/assets/images/products/superfeet-green-insole.webp?v=2.0",
                "date": "November 4, 2026"
            },
            {
                "slug": "rigid-vs-soft-orthotic-insoles-plantar-fasciitis",
                "tag": "Biomechanical Study",
                "title": "Rigid vs Soft Orthotic Insoles: Which Relieves Plantar Fasciitis Pain Faster?",
                "desc": "Biomechanical study comparing rigid TPU plastic shells versus soft memory foam insoles for arch unloading, pronation correction, and pain relief.",
                "img": "/assets/images/rigid-vs-soft-orthotics.webp",
                "date": "November 4, 2026"
            },
            {
                "slug": "how-to-tell-if-you-have-flat-feet-or-high-arches",
                "tag": "Diagnostic Guide",
                "title": "How to Tell If You Have Flat Feet or High Arches: The 3-Step Wet Paper Footprint Test",
                "desc": "Accurately determine your foot arch type at home with the 3-step wet paper footprint test, mirror assessment, and shoe wear pattern inspection.",
                "img": "/assets/images/flat-feet-vs-high-arches.webp",
                "date": "November 4, 2026"
            },
            {
                "slug": "signs-you-need-custom-orthotics-vs-otc-insoles",
                "tag": "Clinical Consultation Guide",
                "title": "Signs You Need Custom Orthotics vs OTC Insoles: Podiatrist Diagnostic Guide",
                "desc": "Clinical criteria and gait signs that indicate when over-the-counter insoles are insufficient and prescription medical custom orthotics are required.",
                "img": "/assets/images/custom-vs-otc-orthotics.webp",
                "date": "November 4, 2026"
            }
        ]
    }
]

def render_category_html(cat):
    # Chips for other 3 categories
    other_cats = [c for c in CATEGORIES if c['slug'] != cat['slug']]
    chips_html = "".join([f'<li><a class="chip" href="/{c["slug"]}/"><b>{c["title"].split("&")[0].strip()}</b></a></li>' for c in other_cats])

    # Article Cards
    cards_html = "".join([f"""
        <li>
          <article class="card">
            <span class="card-pic">
              <img src="{a['img']}" alt="{a['title']}" width="120" height="120" loading="lazy" decoding="async" style="border-radius:6px;object-fit:cover;">
            </span>
            <div class="card-body">
              <span class="tag">{a['tag']}</span>
              <h2><a href="/{a['slug']}/">{a['title']}</a></h2>
              <p>{a['desc']}</p>
              <time datetime="2026-11-04">Updated {a['date']}</time>
            </div>
          </article>
        </li>""" for a in cat['articles']])

    # Active Nav state
    nav_links = [
        ('/callus-removers-and-tools/', 'Callus Removers'),
        ('/foot-creams-and-lotions/', 'Creams &amp; Lotions'),
        ('/foot-massagers-and-spas/', 'Massagers &amp; Spas'),
        ('/orthotics-and-insoles/', 'Orthotics &amp; Insoles'),
        ('/how-we-test/', 'How We Test')
    ]
    cat_url = f"/{cat['slug']}/"
    nav_html = "".join([f'<a href="{url}"{" aria-current=\"page\"" if url == cat_url else ""}>{label}</a>' for url, label in nav_links])

    html = f"""<!doctype html>
<html lang="en-US">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{cat['title']} | Beauty Feet Now</title>
<meta name="description" content="{cat['metaDescription']}">
<link rel="canonical" href="{BASE_URL}/{cat['slug']}/">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
<meta property="og:locale" content="en_US">
<meta property="og:site_name" content="Beauty Feet Now">
<meta property="og:type" content="website">
<meta property="og:title" content="{cat['title']} | Beauty Feet Now">
<meta property="og:description" content="{cat['metaDescription']}">
<meta property="og:url" content="{BASE_URL}/{cat['slug']}/">
<meta property="og:image" content="{BASE_URL}/assets/images/og-share-card.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#1C4E43">
<link rel="stylesheet" href="/assets/style.css">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/images/favicon-32x32.png">
<link rel="apple-touch-icon" sizes="180x180" href="/assets/images/apple-touch-icon.png">
<link rel="alternate" type="application/rss+xml" title="Beauty Feet Now" href="{BASE_URL}/feed.xml">

<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "CollectionPage",
  "name": "{cat['title']}",
  "description": "{cat['metaDescription']}",
  "url": "{BASE_URL}/{cat['slug']}/",
  "publisher": {{
    "@type": "Organization",
    "name": "Beauty Feet Now",
    "logo": {{
      "@type": "ImageObject",
      "url": "{BASE_URL}/assets/logo.png"
    }}
  }}
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
      {nav_html}
    </nav>
  </div>
</header>

<main id="main" class="wrap">
  <nav class="crumbs sr-only" aria-label="Breadcrumb">
    <ol>
      <li><a href="/">Home</a></li>
      <li aria-current="page">{cat['title']}</li>
    </ol>
  </nav>

  <div class="hero">
    <span class="kicker">{cat['kicker']}</span>
    <h1>{cat['h1']}</h1>
    <p class="lead">{cat['lead']}</p>
    <nav aria-label="Related topics">
      <ul class="chips">
        {chips_html}
      </ul>
    </nav>
  </div>

  {cat['introProse']}

  <div class="layout">
    <div>
      <ul class="cards">
        {cards_html}
      </ul>
    </div>

    <aside class="sidebar" aria-label="About this collection">
      <div class="box">
        <div class="box-head">Podiatric Clinical Standard</div>
        <p>Every equipment review and protocol in this category is evaluated by board-certified podiatric physicians adhering to American Podiatric Medical Association (APMA) clinical standards.</p>
        <p>We test motor torque, skin friction thermal limits, keratolytic trans-epidermal water loss, and in-shoe pressure redistribution.</p>
        <a class="btn btn-sm" href="/how-we-test/">How We Test &rarr;</a>
      </div>

      <div class="box">
        <div class="box-head">Medical Disclaimer</div>
        <p>Content is for educational and informational purposes only. Always consult a licensed podiatrist or healthcare professional regarding persistent pain or diabetic foot concerns.</p>
        <a class="btn btn-sm" href="/editorial-policy/">Editorial Standards &rarr;</a>
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
    print("Generating all 4 expanded Category Hub Pages...")
    for cat in CATEGORIES:
        os.makedirs(cat['slug'], exist_ok=True)
        file_path = os.path.join(cat['slug'], 'index.html')
        html = render_category_html(cat)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        # Word count check
        plain = re.sub(r'<[^>]+>', ' ', html)
        words = len([w for w in plain.split() if len(w) > 1])
        print(f"Generated /{cat['slug']}/ -> {words} words")

if __name__ == '__main__':
    main()
