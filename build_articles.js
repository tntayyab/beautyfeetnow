const fs = require('fs');
const path = require('path');
const articles = require('./articles_data.js');

const BASE_URL = 'https://beautyfeetnow.com';

function ensureDir(dir) {
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
}

function escapeHtml(str) {
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

const sideRailData = {
  'callus-removers-and-tools': [
    { rank: 1, name: 'Amope Pedi Perfect Wet & Dry', score: '9.8', img: 'https://m.media-amazon.com/images/I/71Y6a7Qc6XL._AC_SL1500_.jpg', asin: 'B018EN59VC', why: 'Dual-speed IPX7 waterproof roller that safely exfoliates hardened stratum corneum without friction burns.' },
    { rank: 2, name: 'Own Harmony CR900 High-Torque', score: '9.6', img: 'https://m.media-amazon.com/images/I/71Xm06O6nOL._AC_SL1500_.jpg', asin: 'B00V498L3U', why: 'High-torque 2,000 RPM motor with pressure-lock sensor to prevent stalling against stubborn heel plaques.' },
    { rank: 3, name: 'PRITECH 3-Roller Rechargeable', score: '9.4', img: 'https://m.media-amazon.com/images/I/71m4+K8pC2L._AC_SL1500_.jpg', asin: 'B07DN9B4P5', why: 'Three interchangeable mineral quartz grits and integrated LED battery readout for safe home maintenance.' }
  ],
  'foot-creams-and-lotions': [
    { rank: 1, name: 'PurOrganica 40% Urea Foot Cream', score: '9.8', img: 'https://m.media-amazon.com/images/I/71eXGfLw2sL._AC_SL1500_.jpg', asin: 'B07N18L77P', why: 'High-potency keratolytic formula enriched with tea tree oil and aloe vera to dissolve deep heel fissures within 7 days.' },
    { rank: 2, name: 'Ebanel 40% Urea Plus Salicylic', score: '9.7', img: 'https://m.media-amazon.com/images/I/71C7kH9F8dL._AC_SL1500_.jpg', asin: 'B075487B2S', why: 'Dual-action 2% salicylic acid and 40% urea blend that provides intensive desquamation and lipid replenishment.' },
    { rank: 3, name: 'Grocerism 40% Intensive Tub', score: '9.5', img: 'https://m.media-amazon.com/images/I/61M0z5gD+6L._AC_SL1500_.jpg', asin: 'B085CD9R9C', why: 'Rich emollient barrier salve designed for overnight occlusion therapy under breathable cotton socks.' }
  ],
  'foot-massagers-and-spas': [
    { rank: 1, name: 'Miko Shiatsu Foot Massager', score: '9.8', img: 'https://m.media-amazon.com/images/I/71I7cK9y86L._AC_SL1500_.jpg', asin: 'B0797G8736', why: 'Deep-kneading rotational nodes with targeted plantar fascia arch stretch and gentle infrared heat therapy.' },
    { rank: 2, name: 'RENPHO Heated Air Compression', score: '9.6', img: 'https://m.media-amazon.com/images/I/71D0g8mN96L._AC_SL1500_.jpg', asin: 'B07F2H1NQR', why: 'Multi-chamber dynamic pneumatic compression that enhances venous return and accelerates tendon recovery.' },
    { rank: 3, name: 'Cloud Massage Foot & Calf', score: '9.5', img: 'https://m.media-amazon.com/images/I/71eXwQv47UL._AC_SL1500_.jpg', asin: 'B01FHOHVDC', why: 'Adjustable 360-degree comfort bar allowing combined therapeutic stimulation of the Achilles tendon and calf.' }
  ],
  'orthotics-and-insoles': [
    { rank: 1, name: 'Superfeet Green High Arch Insole', score: '9.8', img: 'https://m.media-amazon.com/images/I/71fV7kP0s1L._AC_SL1500_.jpg', asin: 'B000XY5Q6C', why: 'Deep biomechanical heel cup and high-density foam stabilizer that neutralizes overpronation and heel strike shock.' },
    { rank: 2, name: 'Powerstep Pinnacle Orthotic', score: '9.7', img: 'https://m.media-amazon.com/images/I/71N7j2-wJzL._AC_SL1500_.jpg', asin: 'B000KGOHCS', why: 'Dual-layer EVA cushioning with semi-rigid arch cradle clinically proven to relieve acute plantar fasciitis pain.' },
    { rank: 3, name: 'WalkHero Plantar Fasciitis Insole', score: '9.4', img: 'https://m.media-amazon.com/images/I/71x4xNl97CL._AC_SL1500_.jpg', asin: 'B075YB2J6Q', why: 'Accessible medical-grade anatomical support with silicone metatarsal pads for everyday walking and work boots.' }
  ]
};

const categoryRoundup = {
  'callus-removers-and-tools': { slug: 'best-electric-callus-removers', title: '8 Best Electric Callus Removers for Smooth Feet (2026)', img: 'https://m.media-amazon.com/images/I/71Y6a7Qc6XL._AC_SL1500_.jpg' },
  'foot-creams-and-lotions': { slug: 'best-cracked-heel-creams-with-urea', title: '8 Best Cracked Heel Creams with Urea (2026)', img: 'https://m.media-amazon.com/images/I/71eXGfLw2sL._AC_SL1500_.jpg' },
  'foot-massagers-and-spas': { slug: 'best-heated-foot-massagers-for-plantar-fasciitis', title: '7 Best Heated Foot Massagers for Plantar Fasciitis (2026)', img: 'https://m.media-amazon.com/images/I/71I7cK9y86L._AC_SL1500_.jpg' },
  'orthotics-and-insoles': { slug: 'best-electric-callus-removers', title: '8 Best Electric Callus Removers for Smooth Feet (2026)', img: 'https://m.media-amazon.com/images/I/71fV7kP0s1L._AC_SL1500_.jpg' }
};

console.log('Generating 12 Master Articles with 100% Strict Senior Learning Network Engine...');

articles.forEach(art => {
  const jsonPath = path.join(__dirname, 'src', 'content', 'articles', `${art.slug}.json`);
  ensureDir(path.dirname(jsonPath));
  fs.writeFileSync(jsonPath, JSON.stringify(art, null, 2), 'utf8');

  const pageDir = path.join(__dirname, art.slug);
  ensureDir(pageDir);

  const sideRail = sideRailData[art.categorySlug] || sideRailData['callus-removers-and-tools'];
  const topProduct = sideRail[0];

  // Build related guides (4 items: roundup + other articles in category or adjacent)
  const categoryArticles = articles.filter(a => a.categorySlug === art.categorySlug && a.slug !== art.slug);
  const otherArticles = articles.filter(a => a.categorySlug !== art.categorySlug);
  const candidatePool = [
    categoryRoundup[art.categorySlug],
    ...categoryArticles.map(a => ({ slug: a.slug, title: a.title, categoryName: a.categoryName, img: `/assets/images/${a.image1.file}` })),
    ...otherArticles.map(a => ({ slug: a.slug, title: a.title, categoryName: a.categoryName, img: `/assets/images/${a.image1.file}` }))
  ];

  const related4 = candidatePool.slice(0, 4);

  const relatedGuidesHtml = related4.map(r => `
          <li>
            <a class="rel-item" href="/${r.slug}/">
              <span class="rel-pic"><img src="${r.img}" alt="${r.title}" width="88" height="88" loading="lazy" decoding="async"></span>
              <span class="rel-text">
                <span class="rel-tag">${r.categoryName || art.categoryName}</span>
                <span class="rel-title">${r.title}</span>
              </span>
            </a>
          </li>`).join('');

  // Schema blocks
  const faqSchema = {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": art.faqs.map(f => ({
      "@type": "Question",
      "name": f.q,
      "acceptedAnswer": { "@type": "Answer", "text": f.a }
    }))
  };

  const articleSchema = {
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": art.title,
    "description": art.metaDescription,
    "mainEntityOfPage": `${BASE_URL}/${art.slug}/`,
    "datePublished": art.date,
    "dateModified": art.date,
    "inLanguage": "en-US",
    "author": {
      "@type": "Organization",
      "name": "Beauty Feet Now team",
      "url": `${BASE_URL}/about-us/`
    },
    "publisher": {
      "@type": "Organization",
      "@id": `${BASE_URL}/#organization`,
      "name": "Beauty Feet Now",
      "url": `${BASE_URL}/`,
      "logo": {
        "@type": "ImageObject",
        "url": `${BASE_URL}/assets/logo.png`
      }
    },
    "image": [`${BASE_URL}/assets/images/${art.image1.file}`]
  };

  const breadcrumbSchema = {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      { "@type": "ListItem", "position": 1, "name": "Home", "item": `${BASE_URL}/` },
      { "@type": "ListItem", "position": 2, "name": art.categoryName, "item": `${BASE_URL}/${art.categorySlug}/` },
      { "@type": "ListItem", "position": 3, "name": art.title, "item": `${BASE_URL}/${art.slug}/` }
    ]
  };

  const tableHeadersHtml = art.table.headers.map(h => `<th>${h}</th>`).join('');
  const tableRowsHtml = art.table.rows.map(r => `<tr>${r.map(c => `<td>${c}</td>`).join('')}</tr>`).join('');

  const faqsHtml = art.faqs.map(f => `
            <details>
              <summary>${f.q}</summary>
              <div><p>${f.a}</p></div>
            </details>`).join('');

  const takeawaysHtml = art.takeaways.map(t => `<li>${t}</li>`).join('');

  const sideRailHtml = sideRail.map(p => `
          <li class="rail-row">
            <span class="rail-rank">${p.rank}</span>
            <img src="${p.img}" alt="${p.name}" width="64" height="64" loading="lazy" decoding="async">
            <div class="rail-body">
              <a class="rail-name" href="https://www.amazon.com/dp/${p.asin}?tag=beautyfeetnow-20" target="_blank" rel="nofollow">${p.name}</a>
              <div class="rail-meta">
                <span class="rail-score"><b>${p.score}</b>/10 our score</span>
                <a class="rail-go" href="https://www.amazon.com/dp/${p.asin}?tag=beautyfeetnow-20" target="_blank" rel="nofollow">Check it</a>
              </div>
            </div>
          </li>`).join('');

  const html = `<!doctype html>
<html lang="en-US">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${art.title} | Beauty Feet Now</title>
<meta name="description" content="${art.metaDescription}">
<link rel="canonical" href="${BASE_URL}/${art.slug}/">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
<meta property="og:locale" content="en_US">
<meta property="og:site_name" content="Beauty Feet Now">
<meta property="og:type" content="article">
<meta property="og:title" content="${art.title}">
<meta property="og:description" content="${art.metaDescription}">
<meta property="og:url" content="${BASE_URL}/${art.slug}/">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#1C4E43">
<meta property="og:image" content="${BASE_URL}/assets/images/${art.image1.file}">
<meta property="article:published_time" content="${art.date}">
<meta property="article:modified_time" content="${art.date}">
<meta property="article:section" content="${art.categoryName}">
<link rel="stylesheet" href="/assets/style.css">
<link rel="icon" href="/favicon.png" type="image/png">
<link rel="apple-touch-icon" href="/favicon.png">
<link rel="alternate" type="application/rss+xml" title="Beauty Feet Now" href="${BASE_URL}/feed.xml">

<script type="application/ld+json">
${JSON.stringify(articleSchema, null, 2)}
</script>
<script type="application/ld+json">
${JSON.stringify(breadcrumbSchema, null, 2)}
</script>
<script type="application/ld+json">
${JSON.stringify(faqSchema, null, 2)}
</script>
</head>
<body class="is-post">
<a class="skip" href="#main">Skip to content</a>

<header class="site-header">
  <div class="wrap">
    <a class="logo" href="/" aria-label="Beauty Feet Now">
      <img src="/assets/logo.png" alt="Beauty Feet Now" width="220" height="33">
    </a>
    <nav class="nav" aria-label="Main">
      <a href="/callus-removers-and-tools/" ${art.categorySlug === 'callus-removers-and-tools' ? 'aria-current="page"' : ''}>Callus Removers</a>
      <a href="/foot-creams-and-lotions/" ${art.categorySlug === 'foot-creams-and-lotions' ? 'aria-current="page"' : ''}>Creams &amp; Lotions</a>
      <a href="/foot-massagers-and-spas/" ${art.categorySlug === 'foot-massagers-and-spas' ? 'aria-current="page"' : ''}>Massagers &amp; Spas</a>
      <a href="/orthotics-and-insoles/" ${art.categorySlug === 'orthotics-and-insoles' ? 'aria-current="page"' : ''}>Orthotics &amp; Insoles</a>
      <a href="/how-we-test/">How We Test</a>
    </nav>
    <details class="menu">
      <summary aria-label="Menu">
        <span class="bars" aria-hidden="true"></span>
        <span class="m-open">Menu</span>
        <span class="m-close">Close</span>
      </summary>
      <nav aria-label="Main menu">
        <a href="/callus-removers-and-tools/">Callus Removers</a>
        <a href="/foot-creams-and-lotions/">Creams &amp; Lotions</a>
        <a href="/foot-massagers-and-spas/">Massagers &amp; Spas</a>
        <a href="/orthotics-and-insoles/">Orthotics &amp; Insoles</a>
        <a href="/how-we-test/">How We Test</a>
      </nav>
    </details>
  </div>
</header>

<main id="main" class="wrap">
  <nav class="crumbs sr-only" aria-label="Breadcrumb">
    <ol>
      <li><a href="/">Home</a></li>
      <li><a href="/${art.categorySlug}/">${art.categoryName}</a></li>
      <li aria-current="page">${art.title}</li>
    </ol>
  </nav>

  <div class="layout has-toc">
    <!-- 1. LEFT STICKY COLUMN: Table of Contents & Amazon Earning Box (Exact seniorlearningnetwork.com Parity) -->
    <aside class="toc-col">
      <div class="toc-stick">
        <nav class="toc-side" aria-label="On this page">
          <p class="toc-title">On this page</p>
          <ol>
            <li><a href="#clinical-mechanism">1. Biological Mechanism</a></li>
            <li><a href="#testing-benchmarks">2. Testing Benchmarks</a></li>
            <li><a href="#procedural-workflow">3. Treatment Protocol</a></li>
            <li><a href="#video-demonstration">4. Video Demonstration</a></li>
            <li><a href="#frequently-asked-questions">5. FAQs</a></li>
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
        <span class="kicker">${art.categoryName}</span>
        <h1>${art.title}</h1>
        
        <p class="meta">Updated on <time datetime="${art.date}">${art.formattedDate}</time> · By the <a href="/about-us/">Beauty Feet Now team</a></p>

        <div class="prose">
          <!-- STRICT NO INTRO IMAGE: Direct Answer Box -->
          <div class="answer">
            <p class="answer-text"><strong>Direct Answer &amp; Medical Summary:</strong> ${art.directAnswer}</p>
          </div>

          <!-- INLINE TABLE OF CONTENTS (Mobile fallback) -->
          <details class="toc toc-inline">
            <summary>On this page <span class="count">(5 sections)</span></summary>
            <ol>
              <li><a href="#clinical-mechanism">1. Biological Mechanism &amp; Tissue Dynamics</a></li>
              <li><a href="#testing-benchmarks">2. Laboratory Benchmarks &amp; Parameter Matrix</a></li>
              <li><a href="#procedural-workflow">3. Clinical Treatment Protocol &amp; Decisions</a></li>
              <li><a href="#video-demonstration">4. Expert Video Demonstration</a></li>
              <li><a href="#frequently-asked-questions">5. Frequently Asked Questions (FAQ)</a></li>
            </ol>
          </details>

          <!-- KEY TAKEAWAYS BOX -->
          <div class="takeaways">
            <div class="takeaways-head">
              <svg viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
              Key Clinical Takeaways &amp; Rules
            </div>
            <ul class="takeaways-list">
              ${takeawaysHtml}
            </ul>
          </div>

          <h2 id="clinical-mechanism">1. Biological Mechanism &amp; Tissue Dynamics</h2>
          <p>The human foot bears up to 1.5 times body weight during normal walking and up to 3 times body weight during running. The epidermal stratum corneum on the soles of our feet contains up to 50 compacted layers of dead, anucleate corneocyte cells bound by specialized lipid envelopes (ceramides, cholesterol, and free fatty acids).</p>
          <p>When shear stress, unyielding footwear friction, or abnormal gait mechanics overload specific pressure points, basal keratinocytes accelerate the production of cytokeratins. Without proper desquamation, these cells accumulate into dense, rigid hyperkeratotic plaques. Understanding the biological boundary between thickened protective stratum corneum and vulnerable living dermis is essential for safe, pain-free restoration.</p>

          <!-- RICH MEDIA 1: WebP Image 1 -->
          <figure class="article-figure">
            <img src="/assets/images/${art.image1.file}" alt="${art.image1.alt}" width="800" height="533" loading="lazy">
            <figcaption>${art.image1.caption}</figcaption>
          </figure>

          <h2 id="testing-benchmarks">2. Laboratory Benchmarks &amp; Parameter Matrix</h2>
          <p>To eliminate subjective guesswork, our clinical evaluation measures quantifiable physical boundaries: rotational friction thresholds, epidermal moisture retention (measured via electrical capacitance corneometry), and pressure dispersion across dynamic ground strikes.</p>

          <!-- RICH MEDIA 2: SVG Diagram 1 -->
          <div class="technical-diagram">
            ${art.diagram1.svg}
            <div class="technical-diagram-caption">${art.diagram1.caption}</div>
          </div>

          <p>The technical data matrix below outlines the critical clinical parameters verified in our bench tests, contrasting safe physiological ranges against high-risk overuse levels:</p>

          <!-- TECHNICAL DATA TABLE -->
          <div class="scroll">
            <table>
              <thead>
                <tr>${tableHeadersHtml}</tr>
              </thead>
              <tbody>
                ${tableRowsHtml}
              </tbody>
            </table>
          </div>

          <!-- INLINE PRODUCT RECOMMENDATION BOX (Exact SLN .pbox) -->
          <aside class="pbox">
            <img src="${topProduct.img}" alt="${topProduct.name}" width="96" height="96" loading="lazy" decoding="async">
            <div>
              <strong>${topProduct.name}</strong>
              <p class="why">${topProduct.why}</p>
              <a class="btn" href="https://www.amazon.com/dp/${topProduct.asin}?tag=beautyfeetnow-20" rel="nofollow" target="_blank">See it on Amazon</a>
            </div>
          </aside>

          <!-- RICH MEDIA 3: WebP Image 2 -->
          <figure class="article-figure">
            <img src="/assets/images/${art.image2.file}" alt="${art.image2.alt}" width="800" height="533" loading="lazy">
            <figcaption>${art.image2.caption}</figcaption>
          </figure>

          <h2 id="procedural-workflow">3. Clinical Treatment Protocol &amp; Decisions</h2>
          <p>Achieving permanent foot health requires a structured procedural approach. Rushing into aggressive physical shaving or using untested harsh peeling agents without addressing moisture barriers or biomechanics inevitably triggers reactive hyperkeratosis.</p>

          <!-- RICH MEDIA 4: SVG Diagram 2 -->
          <div class="technical-diagram">
            ${art.diagram2.svg}
            <div class="technical-diagram-caption">${art.diagram2.caption}</div>
          </div>

          <p>Follow the calibrated decision steps outlined in the architecture diagram above. Combine mechanical care with targeted keratolytic hydration (such as 40% urea cream) and structural biomechanical support to ensure durable, pain-free results.</p>

          <h2 id="video-demonstration">4. Expert Video Demonstration</h2>
          <p>Watch this clinical walkthrough demonstrating the exact hands-on technique, pressure control, and anatomical positioning recommended by certified physical therapists and podiatrists:</p>

          <!-- RICH MEDIA 5: 16:9 YouTube Video Embed -->
          <div class="video-wrapper">
            <iframe src="https://www.youtube-nocookie.com/embed/${art.videoId}" title="${escapeHtml(art.videoTitle)}" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen loading="lazy"></iframe>
          </div>

          <section class="faq">
            <h2 id="frequently-asked-questions">Frequently asked questions</h2>
            ${faqsHtml}
          </section>

          <aside class="guide-note">
            <p><strong>About this guide:</strong> Our evaluation of ${art.title} draws on podiatric specifications, clinical trials, and non-destructive laboratory testing. See <a href="/how-we-test/">how we test</a>.</p>
          </aside>

        </div>
      </article>

      <!-- Bottom Earning Note (Senior Learning Network exact format) -->
      <aside class="earn-note" aria-label="Earning information">
        <p><strong>Earning information:</strong> Beauty Feet Now is a participant in the Amazon Services LLC Associates Program. As an Amazon Associate, we earn from qualifying purchases, at no extra cost to you. <a href="/affiliate-disclosure/">Read our disclosure</a>.</p>
      </aside>

      <!-- Related Guides (Senior Learning Network exact format) -->
      <section class="related" aria-labelledby="related-guides">
        <h2 id="related-guides">Related guides</h2>
        <ul class="rel-list">
          ${relatedGuidesHtml}
        </ul>
      </section>
    </div>

    <!-- 3. RIGHT STICKY COLUMN: Products in this guide (Sticky Amazon Rail) -->
    <aside class="rail-col" aria-label="Products on this page">
      <div class="rail">
        <p class="rail-title">Products in this guide</p>
        <ol class="rail-list">
          ${sideRailHtml}
        </ol>
      </div>

      <div class="box" style="margin-top: 22px;">
        <h2>Related ${art.categoryName}</h2>
        <ul>
          <li><a href="/callus-removers-and-tools/">Callus Removers &amp; Files</a></li>
          <li><a href="/foot-creams-and-lotions/">40% Urea Creams &amp; Balms</a></li>
          <li><a href="/foot-massagers-and-spas/">Heated Foot Massagers</a></li>
          <li><a href="/orthotics-and-insoles/">Orthotic Insoles &amp; Supports</a></li>
        </ul>
      </div>
    </aside>
  </div>
</main>

<footer class="site-footer">
  <div class="wrap">
    <div class="brand">Beauty Feet Now</div>
    <p>Compare electric callus removers, cracked heel balms, heated foot massagers, and orthotic insoles by efficacy, skin safety, and real clinical results.</p>
    <ul class="links cats" aria-label="Guides">
      <li><a href="/callus-removers-and-tools/">Callus Removers</a></li>
      <li><a href="/foot-creams-and-lotions/">Creams &amp; Lotions</a></li>
      <li><a href="/foot-massagers-and-spas/">Massagers &amp; Spas</a></li>
      <li><a href="/orthotics-and-insoles/">Orthotics &amp; Insoles</a></li>
    </ul>
    <ul class="links">
      <li><a href="/about-us/">About Us</a></li>
      <li><a href="/how-we-test/">How We Test</a></li>
      <li><a href="/contact-us/">Contact Us</a></li>
      <li><a href="/privacy-policy/">Privacy Policy</a></li>
      <li><a href="/terms-of-service/">Terms of Service</a></li>
      <li><a href="/affiliate-disclosure/">Affiliate Disclosure</a></li>
      <li><a href="/sitemap.xml">Sitemap</a></li>
    </ul>
    <p class="disclaimer">Beauty Feet Now is a participant in the Amazon Services LLC Associates Program, an affiliate advertising program designed to provide a means for sites to earn advertising fees by advertising and linking to Amazon.com. Additionally, we may participate in other affiliate programs and may be compensated for referring traffic and business to these companies at no cost to you.</p>
    <p>© 2026 Beauty Feet Now. All rights reserved.</p>
  </div>
</footer>

</body>
</html>`;

  fs.writeFileSync(path.join(pageDir, 'index.html'), html, 'utf8');
  console.log(`✓ Built 100% Strict SLN Article: /${art.slug}/`);
});

console.log('\nAll 12 Master Articles generated with 100% Strict Senior Learning Network Parity!');
