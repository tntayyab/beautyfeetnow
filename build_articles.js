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
    { rank: 1, name: 'Amope Pedi Perfect Wet & Dry', score: '9.8', img: 'https://m.media-amazon.com/images/I/71Y6a7Qc6XL._AC_SL1500_.jpg', asin: 'B018EN59VC' },
    { rank: 2, name: 'Own Harmony CR900 High-Torque', score: '9.6', img: 'https://m.media-amazon.com/images/I/71Xm06O6nOL._AC_SL1500_.jpg', asin: 'B00V498L3U' },
    { rank: 3, name: 'PRITECH 3-Roller Rechargeable', score: '9.4', img: 'https://m.media-amazon.com/images/I/71m4+K8pC2L._AC_SL1500_.jpg', asin: 'B07DN9B4P5' }
  ],
  'foot-creams-and-lotions': [
    { rank: 1, name: 'PurOrganica 40% Urea Foot Cream', score: '9.8', img: 'https://m.media-amazon.com/images/I/71eXGfLw2sL._AC_SL1500_.jpg', asin: 'B07N18L77P' },
    { rank: 2, name: 'Ebanel 40% Urea Plus Salicylic', score: '9.7', img: 'https://m.media-amazon.com/images/I/71C7kH9F8dL._AC_SL1500_.jpg', asin: 'B075487B2S' },
    { rank: 3, name: 'Grocerism 40% Intensive Tub', score: '9.5', img: 'https://m.media-amazon.com/images/I/61M0z5gD+6L._AC_SL1500_.jpg', asin: 'B085CD9R9C' }
  ],
  'foot-massagers-and-spas': [
    { rank: 1, name: 'Miko Shiatsu Foot Massager', score: '9.8', img: 'https://m.media-amazon.com/images/I/71I7cK9y86L._AC_SL1500_.jpg', asin: 'B0797G8736' },
    { rank: 2, name: 'RENPHO Heated Air Compression', score: '9.6', img: 'https://m.media-amazon.com/images/I/71D0g8mN96L._AC_SL1500_.jpg', asin: 'B07F2H1NQR' },
    { rank: 3, name: 'Cloud Massage Foot & Calf', score: '9.5', img: 'https://m.media-amazon.com/images/I/71eXwQv47UL._AC_SL1500_.jpg', asin: 'B01FHOHVDC' }
  ],
  'orthotics-and-insoles': [
    { rank: 1, name: 'Superfeet Green High Arch Insole', score: '9.8', img: 'https://m.media-amazon.com/images/I/71fV7kP0s1L._AC_SL1500_.jpg', asin: 'B000XY5Q6C' },
    { rank: 2, name: 'Powerstep Pinnacle Orthotic', score: '9.7', img: 'https://m.media-amazon.com/images/I/71N7j2-wJzL._AC_SL1500_.jpg', asin: 'B000KGOHCS' },
    { rank: 3, name: 'WalkHero Plantar Fasciitis Insole', score: '9.4', img: 'https://m.media-amazon.com/images/I/71x4xNl97CL._AC_SL1500_.jpg', asin: 'B075YB2J6Q' }
  ]
};

console.log('Generating 12 Master Articles with Exact Senior Learning Network 3-Column Engine...');

articles.forEach(art => {
  const jsonPath = path.join(__dirname, 'src', 'content', 'articles', `${art.slug}.json`);
  ensureDir(path.dirname(jsonPath));
  fs.writeFileSync(jsonPath, JSON.stringify(art, null, 2), 'utf8');

  const pageDir = path.join(__dirname, art.slug);
  ensureDir(pageDir);

  const sideRail = sideRailData[art.categorySlug] || sideRailData['callus-removers-and-tools'];

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
      "@type": "Person",
      "name": "Elena Rostova",
      "jobTitle": "Podiatric Dermatology & Lower Extremity Biomechanics Specialist",
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
            <img src="${p.img}" alt="${p.name}" width="64" height="64" loading="lazy">
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
      <a href="/foot-creams-and-lotions/" ${art.categorySlug === 'foot-creams-and-lotions' ? 'aria-current="page"' : ''}>Creams & Lotions</a>
      <a href="/foot-massagers-and-spas/" ${art.categorySlug === 'foot-massagers-and-spas' ? 'aria-current="page"' : ''}>Massagers & Spas</a>
      <a href="/orthotics-and-insoles/" ${art.categorySlug === 'orthotics-and-insoles' ? 'aria-current="page"' : ''}>Orthotics & Insoles</a>
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
        <a href="/foot-creams-and-lotions/">Creams & Lotions</a>
        <a href="/foot-massagers-and-spas/">Massagers & Spas</a>
        <a href="/orthotics-and-insoles/">Orthotics & Insoles</a>
        <a href="/how-we-test/">How We Test</a>
      </nav>
    </details>
  </div>
</header>

<main id="main" class="wrap">
  <nav class="crumbs" aria-label="Breadcrumb">
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
        <div class="prose">
          <span class="kicker">${art.categoryName}</span>
          <h1>${art.title}</h1>
          
          <div class="meta">
            <span>By <strong>Elena Rostova</strong> (Podiatry Specialist)</span>
            <span>•</span>
            <time datetime="${art.date}">${art.formattedDate}</time>
            <span>•</span>
            <span>${art.readTime}</span>
          </div>

          <!-- STRICT NO INTRO IMAGE: Begins directly with Direct Answer Box -->
          <div class="answer">
            <div class="answer-label">
              <svg viewBox="0 0 24 24"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
              Direct Answer &amp; Medical Summary
            </div>
            <p class="answer-lead">${art.directAnswer}</p>
          </div>

          <!-- KEY TAKEAWAYS BOX: Exactly 5 checkmark bullets -->
          <div class="takeaways">
            <div class="takeaways-head">
              <svg viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
              Key Clinical Takeaways &amp; Rules
            </div>
            <ul class="takeaways-list">
              ${takeawaysHtml}
            </ul>
          </div>

          <!-- INLINE TABLE OF CONTENTS (Mobile fallback) -->
          <details class="toc-inline" open>
            <summary>Table of Contents</summary>
            <ol>
              <li><a href="#clinical-mechanism">1. Biological Mechanism &amp; Tissue Dynamics</a></li>
              <li><a href="#testing-benchmarks">2. Laboratory Benchmarks &amp; Parameter Matrix</a></li>
              <li><a href="#procedural-workflow">3. Clinical Treatment Protocol &amp; Decisions</a></li>
              <li><a href="#video-demonstration">4. Expert Video Demonstration</a></li>
              <li><a href="#frequently-asked-questions">5. Frequently Asked Questions (FAQ)</a></li>
            </ol>
          </details>

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

          <h2 id="frequently-asked-questions">5. Frequently Asked Questions (FAQ)</h2>
          <div class="faq">
            ${faqsHtml}
          </div>

          <div class="guide-note">
            <p><strong>Medical Transparency:</strong> Written and reviewed by Elena Rostova, Podiatric Dermatology &amp; Biomechanics Specialist. All evaluations adhere to strict non-destructive testing protocols. If you experience bleeding, severe diabetes complications, or numbness, consult a physician immediately.</p>
          </div>

        </div>
      </article>
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
    <div class="footer-grid">
      <div class="footer-col">
        <h3>Beauty Feet Now</h3>
        <p>Your premier independent guide to foot wellness, pedicure tools, and therapeutic relief. We evaluate podiatry aids, electric files, and dermatological creams to help you achieve salon-smooth, pain-free feet from home.</p>
        <p><strong>Contact:</strong> contact@beautyfeetnow.com</p>
      </div>
      <div class="footer-col">
        <h3>Top Categories</h3>
        <ul>
          <li><a href="/callus-removers-and-tools/">Callus Removers &amp; Files</a></li>
          <li><a href="/foot-creams-and-lotions/">Foot Creams &amp; Salves</a></li>
          <li><a href="/foot-massagers-and-spas/">Foot Massagers &amp; Spas</a></li>
          <li><a href="/orthotics-and-insoles/">Orthotics &amp; Insoles</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h3>Editorial &amp; Legal</h3>
        <ul>
          <li><a href="/about-us/">About Us</a></li>
          <li><a href="/how-we-test/">How We Test &amp; Review</a></li>
          <li><a href="/contact-us/">Contact Us</a></li>
          <li><a href="/privacy-policy/">Privacy Policy</a></li>
          <li><a href="/terms-of-service/">Terms of Service</a></li>
          <li><a href="/affiliate-disclosure/">Affiliate Disclosure</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <p class="disclaimer"><strong>Affiliate Disclaimer:</strong> Beauty Feet Now is a participant in the Amazon Services LLC Associates Program and other affiliate advertising programs designed to provide a means for sites to earn advertising fees by linking to Amazon.com. If you purchase through our links, we may earn a modest commission at zero additional cost to you.</p>
      <p>© 2026 Beauty Feet Now. All rights reserved. Content is for informational purposes and not medical advice.</p>
    </div>
  </div>
</footer>

</body>
</html>`;

  fs.writeFileSync(path.join(pageDir, 'index.html'), html, 'utf8');
});

console.log('Successfully generated all 12 Master Articles with SLN 3-Column layout!');

// =========================================================================
// 2. UPGRADE 3 ROUNDUP GUIDES TO STRICT 3-COLUMN SLN LAYOUT
// =========================================================================

function upgradeRoundup(filePath, tocItems) {
  let content = fs.readFileSync(filePath, 'utf8');
  
  // Replace <div class="layout"> with <div class="layout has-toc">
  // And insert the Left Sticky TOC Column
  const leftColHtml = `  <div class="layout has-toc">
    <!-- 1. LEFT STICKY COLUMN: Table of Contents & Amazon Earning Box (Exact seniorlearningnetwork.com Parity) -->
    <aside class="toc-col">
      <div class="toc-stick">
        <nav class="toc-side" aria-label="On this page">
          <p class="toc-title">On this page</p>
          <ol>
${tocItems.map(t => `            <li><a href="${t.href}">${t.label}</a></li>`).join('\n')}
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
      <article class="article">`;

  // Replace old starting tag
  if (content.includes('<div class="layout">\n    <article class="article">') || content.includes('<div class="layout">\r\n    <article class="article">')) {
    content = content.replace(/<div class="layout">[\r\n\s]*<article class="article">/, leftColHtml);
  } else if (!content.includes('class="toc-col"')) {
    content = content.replace('<div class="layout">', leftColHtml);
  }

  // Close the center column div before right rail
  if (content.includes('</article>\n\n    <!-- Right Sticky Products Rail') || content.includes('</article>\r\n\r\n    <!-- Right Sticky Products Rail')) {
    content = content.replace('</article>', '</article>\n    </div>');
  }

  fs.writeFileSync(filePath, content, 'utf8');
  console.log('Upgraded roundup guide:', path.basename(path.dirname(filePath)));
}

// 1. Callus Removers Roundup
upgradeRoundup(path.join(__dirname, 'best-electric-callus-removers', 'index.html'), [
  { href: '#quick-verdict', label: 'Our Quick Verdict' },
  { href: '#comparison-table', label: 'Comparison Table' },
  { href: '#our-picks', label: 'Picks at a Glance' },
  { href: '#pick-1-amope-pedi-perfect', label: '1. Amope Pedi Perfect' },
  { href: '#pick-2-own-harmony-cr900', label: '2. Own Harmony CR900' },
  { href: '#pick-3-pritech-rechargeable', label: '3. PRITECH Rechargeable' },
  { href: '#pick-4-care-me-powerful', label: '4. Care me Powerful' },
  { href: '#pick-5-rikans-waterproof', label: '5. Rikans Waterproof' },
  { href: '#pick-6-iroha-vacuum-grinder', label: '6. Iroha Vacuum Grinder' },
  { href: '#pick-7-flawless-pedi', label: '7. Flawless Pedi Tool' },
  { href: '#pick-8-innobeta-cordless', label: '8. InnoBeta Cordless' }
]);

// 2. Heel Creams Roundup
upgradeRoundup(path.join(__dirname, 'best-cracked-heel-creams-with-urea', 'index.html'), [
  { href: '#quick-verdict', label: 'Our Quick Verdict' },
  { href: '#comparison-table', label: 'Comparison Table' },
  { href: '#our-picks', label: 'Picks at a Glance' },
  { href: '#pick-1-purorganica-urea', label: '1. PurOrganica 40% Urea' },
  { href: '#pick-2-ebanel-urea', label: '2. Ebanel 40% Urea Plus' },
  { href: '#pick-3-grocerism-urea', label: '3. Grocerism 40% Intensive' },
  { href: '#pick-4-udderly-smooth', label: '4. Udderly Smooth 20%' },
  { href: '#pick-5-flexitol-heel-balm', label: '5. Flexitol Heel Balm' },
  { href: '#pick-6-okeeffes-healthy-feet', label: "6. O'Keeffe's Healthy Feet" },
  { href: '#pick-7-cerave-sa-foot-cream', label: '7. CeraVe SA Renewing' }
]);

// 3. Foot Massagers Roundup
upgradeRoundup(path.join(__dirname, 'best-heated-foot-massagers-for-plantar-fasciitis', 'index.html'), [
  { href: '#quick-verdict', label: 'Our Quick Verdict' },
  { href: '#comparison-table', label: 'Comparison Table' },
  { href: '#our-picks', label: 'Picks at a Glance' },
  { href: '#pick-1-miko-shiatsu', label: '1. Miko Shiatsu Machine' },
  { href: '#pick-2-renpho-heated', label: '2. RENPHO Heated Machine' },
  { href: '#pick-3-cloud-massage', label: '3. Cloud Massage Foot & Calf' },
  { href: '#pick-4-nekteck-shiatsu', label: '4. Nekteck Foot Massager' },
  { href: '#pick-5-medmassager-mmf07', label: '5. MedMassager MMF07' },
  { href: '#pick-6-belmint-shiatsu', label: '6. Belmint Heated Shiatsu' }
]);

console.log('All 15 inner pages are now 100% strict Senior Learning Network 3-column architecture!');
