const fs = require('fs');
const path = require('path');
const articles = require('./articles_data.js');

const BASE_URL = 'https://beautyfeetnow.com';

function ensureDir(dir) {
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
}

ensureDir(path.join(__dirname, 'src', 'content', 'articles'));

// Helper for HTML escaping
function escapeHtml(str) {
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

// Side Rail products mapping by category
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

console.log('Generating 12 Master Articles...');

articles.forEach(art => {
  // 1. Save JSON data
  const jsonPath = path.join(__dirname, 'src', 'content', 'articles', `${art.slug}.json`);
  fs.writeFileSync(jsonPath, JSON.stringify(art, null, 2), 'utf8');

  // 2. Prepare HTML directory
  const pageDir = path.join(__dirname, art.slug);
  ensureDir(pageDir);

  const sideRail = sideRailData[art.categorySlug] || sideRailData['callus-removers-and-tools'];

  // Build FAQ Schema
  const faqSchema = {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": art.faqs.map(f => ({
      "@type": "Question",
      "name": f.q,
      "acceptedAnswer": {
        "@type": "Answer",
        "text": f.a
      }
    }))
  };

  // Build Article Schema
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

  // Build Breadcrumb Schema
  const breadcrumbSchema = {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      { "@type": "ListItem", "position": 1, "name": "Home", "item": `${BASE_URL}/` },
      { "@type": "ListItem", "position": 2, "name": art.categoryName, "item": `${BASE_URL}/${art.categorySlug}/` },
      { "@type": "ListItem", "position": 3, "name": art.title, "item": `${BASE_URL}/${art.slug}/` }
    ]
  };

  // Build Table Rows
  const tableHeadersHtml = art.table.headers.map(h => `<th>${h}</th>`).join('');
  const tableRowsHtml = art.table.rows.map(r => `<tr>${r.map(c => `<td>${c}</td>`).join('')}</tr>`).join('');

  // Build FAQs HTML
  const faqsHtml = art.faqs.map(f => `
        <details>
          <summary>${f.q}</summary>
          <div><p>${f.a}</p></div>
        </details>`).join('');

  // Build Takeaways List
  const takeawaysHtml = art.takeaways.map(t => `<li>${t}</li>`).join('');

  // Build Side Rail HTML
  const sideRailHtml = sideRail.map(p => `
          <li class="rail-row">
            <span class="rail-rank">${p.rank}</span>
            <img src="${p.img}" alt="${p.name}" width="60" height="60" loading="lazy">
            <div class="rail-body">
              <a class="rail-name" href="https://www.amazon.com/dp/${p.asin}?tag=beautyfeetnow-20" target="_blank" rel="nofollow">${p.name}</a>
              <div class="rail-meta">
                <span class="rail-score">Score: <b>${p.score}</b></span>
                <a class="rail-go" href="https://www.amazon.com/dp/${p.asin}?tag=beautyfeetnow-20" target="_blank" rel="nofollow">Buy</a>
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
    <!-- Center Article Prose -->
    <article class="article">
      <div class="prose">
        <span class="kicker">${art.categoryName}</span>
        <h1>${art.title}</h1>
        
        <div class="meta">
          <span>By <strong>Elena Rostova</strong> (Podiatry &amp; Skincare Specialist)</span>
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

        <!-- INLINE TABLE OF CONTENTS -->
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

    <!-- Right Sticky Product Rail -->
    <aside class="rail-col" aria-label="Sidebar">
      <div class="rail">
        <div class="rail-title">Top Recommended Tools</div>
        <ul class="rail-list">
          ${sideRailHtml}
        </ul>
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
  console.log(`Generated: ${art.slug}/index.html`);
});

// Update sitemap.xml with all 12 articles
const allUrls = [
  { loc: `${BASE_URL}/`, priority: '1.0', changefreq: 'daily' },
  { loc: `${BASE_URL}/callus-removers-and-tools/`, priority: '0.8', changefreq: 'weekly' },
  { loc: `${BASE_URL}/foot-creams-and-lotions/`, priority: '0.8', changefreq: 'weekly' },
  { loc: `${BASE_URL}/foot-massagers-and-spas/`, priority: '0.8', changefreq: 'weekly' },
  { loc: `${BASE_URL}/orthotics-and-insoles/`, priority: '0.8', changefreq: 'weekly' },
  { loc: `${BASE_URL}/best-electric-callus-removers/`, priority: '0.9', changefreq: 'weekly' },
  { loc: `${BASE_URL}/best-cracked-heel-creams-with-urea/`, priority: '0.9', changefreq: 'weekly' },
  { loc: `${BASE_URL}/best-heated-foot-massagers-for-plantar-fasciitis/`, priority: '0.9', changefreq: 'weekly' }
];

articles.forEach(art => {
  allUrls.push({ loc: `${BASE_URL}/${art.slug}/`, priority: '0.9', changefreq: 'weekly' });
});

['about-us', 'how-we-test', 'contact-us', 'privacy-policy', 'terms-of-service', 'affiliate-disclosure'].forEach(leg => {
  allUrls.push({ loc: `${BASE_URL}/${leg}/`, priority: '0.4', changefreq: 'monthly' });
});

const sitemapXml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${allUrls.map(u => `  <url>
    <loc>${u.loc}</loc>
    <lastmod>2026-11-04T15:00:00+00:00</lastmod>
    <changefreq>${u.changefreq}</changefreq>
    <priority>${u.priority}</priority>
  </url>`).join('\n')}
</urlset>`;

fs.writeFileSync(path.join(__dirname, 'sitemap.xml'), sitemapXml, 'utf8');
console.log('Updated sitemap.xml with', allUrls.length, 'URLs');

// Update feed.xml with all articles
const feedXml = `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>Beauty Feet Now</title>
    <link>${BASE_URL}/</link>
    <description>The Authority on Healthy, Beautiful &amp; Pain-Free Feet</description>
    <language>en-us</language>
${articles.map(art => `    <item>
      <title>${escapeHtml(art.title)}</title>
      <link>${BASE_URL}/${art.slug}/</link>
      <description>${escapeHtml(art.metaDescription)}</description>
      <pubDate>Wed, 04 Nov 2026 15:00:00 GMT</pubDate>
    </item>`).join('\n')}
  </channel>
</rss>`;

fs.writeFileSync(path.join(__dirname, 'feed.xml'), feedXml, 'utf8');
console.log('Updated feed.xml with 12 articles');

// Update each category page with its 3 new articles
const catSlugs = [
  'callus-removers-and-tools',
  'foot-creams-and-lotions',
  'foot-massagers-and-spas',
  'orthotics-and-insoles'
];

catSlugs.forEach(slug => {
  const catArticles = articles.filter(a => a.categorySlug === slug);
  const catPagePath = path.join(__dirname, slug, 'index.html');
  if (!fs.existsSync(catPagePath)) return;

  let catHtml = fs.readFileSync(catPagePath, 'utf8');
  
  const cardsHtml = catArticles.map(a => `
        <li>
          <article class="card">
            <span class="card-pic">
              <img src="/assets/images/${a.image1.file}" alt="${escapeHtml(a.title)}" width="88" height="88" loading="lazy">
            </span>
            <div class="card-body">
              <span class="tag">${a.categoryName}</span>
              <h3><a href="/${a.slug}/">${a.title}</a></h3>
              <p>${a.metaDescription}</p>
              <time datetime="2026-11-04">Updated November 4, 2026</time>
            </div>
          </article>
        </li>`).join('');

  // Append new cards inside <ul class="cards">
  catHtml = catHtml.replace('</ul>', `${cardsHtml}\n      </ul>`);
  fs.writeFileSync(catPagePath, catHtml, 'utf8');
  console.log(`Updated category page: ${slug}/index.html`);
});

console.log('All builds completed successfully!');
