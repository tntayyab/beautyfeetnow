const fs = require('fs');
const path = require('path');
const articles = require('./articles_data.js');

const categories = [
  {
    slug: 'callus-removers-and-tools',
    name: 'Callus Removers and Tools',
    heading: 'Callus Removers & Exfoliation Tools',
    lead: 'Compare electric callus removers, nano-glass foot files, pumice stones, and replacement rollers by motor torque, grit coarseness, and skin safety.',
    roundup: {
      slug: 'best-electric-callus-removers',
      title: '8 Best Electric Callus Removers for Smooth Feet (2026)',
      desc: 'Compare top electric foot grinders by motor RPM, roller coarseness, battery runtime, and water resistance for effortless callus removal.',
      img: 'https://m.media-amazon.com/images/I/71Y6a7Qc6XL._AC_SL1500_.jpg',
      tag: 'Roundup Guide'
    }
  },
  {
    slug: 'foot-creams-and-lotions',
    name: 'Foot Creams and Lotions',
    heading: 'Foot Creams, Salves & Urea Balms',
    lead: 'Compare dermatological 20% to 40% urea foot creams, keratolytic salicylic salves, and intensive cracked heel balms for dry, fissured feet.',
    roundup: {
      slug: 'best-cracked-heel-creams-with-urea',
      title: '8 Best Cracked Heel Creams with Urea (2026)',
      desc: 'Evaluate top clinical cracked heel balms by urea concentration, keratolytic speed, lipid restoration, and overnight fissure healing.',
      img: 'https://m.media-amazon.com/images/I/71eXGfLw2sL._AC_SL1500_.jpg',
      tag: 'Roundup Guide'
    }
  },
  {
    slug: 'foot-massagers-and-spas',
    name: 'Foot Massagers and Spas',
    heading: 'Foot Massagers, Spas & Acupressure',
    lead: 'Compare deep-kneading shiatsu foot massagers, heated air compression devices, and therapeutic foot spas for chronic plantar fasciitis and fatigue relief.',
    roundup: {
      slug: 'best-heated-foot-massagers-for-plantar-fasciitis',
      title: '7 Best Heated Foot Massagers for Plantar Fasciitis (2026)',
      desc: 'Tested evaluations of deep-kneading shiatsu nodes, infrared heating elements, and pneumatic compression boots for acute heel pain relief.',
      img: 'https://m.media-amazon.com/images/I/71I7cK9y86L._AC_SL1500_.jpg',
      tag: 'Roundup Guide'
    }
  },
  {
    slug: 'orthotics-and-insoles',
    name: 'Orthotics and Insoles',
    heading: 'Orthotics, Insoles & Arch Supports',
    lead: 'Compare podiatrist-grade rigid and semi-rigid orthotic inserts, plantar fasciitis heel cups, and cushioning insoles by arch height and shock absorption.',
    roundup: {
      slug: 'best-orthotic-insoles-for-flat-feet',
      title: '8 Best Orthotic Insoles for Flat Feet (2026)',
      desc: 'Biomechanical evaluations of rigid arch cradles, deep heel cups, and shock-absorbing metatarsal pads for collapsed arches and overpronation.',
      img: 'https://m.media-amazon.com/images/I/71fV7kP0s1L._AC_SL1500_.jpg',
      tag: 'Roundup Guide'
    }
  }
];

categories.forEach(cat => {
  const catArticles = articles.filter(a => a.categorySlug === cat.slug);
  const otherCats = categories.filter(c => c.slug !== cat.slug);

  const chipsHtml = otherCats.map(c => `<li><a class="chip" href="/${c.slug}/"><b>${c.name}</b></a></li>`).join('');

  const roundupCard = `
        <li>
          <article class="card">
            <span class="card-pic">
              <img src="${cat.roundup.img}" alt="${cat.roundup.title}" width="120" height="120" loading="lazy" decoding="async">
            </span>
            <div class="card-body">
              <span class="tag">${cat.roundup.tag}</span>
              <h2><a href="/${cat.roundup.slug}/">${cat.roundup.title}</a></h2>
              <p>${cat.roundup.desc}</p>
              <time datetime="2026-11-04">Updated November 4, 2026</time>
            </div>
          </article>
        </li>`;

  const articlesCards = catArticles.map(a => `
        <li>
          <article class="card">
            <span class="card-pic">
              <img src="/assets/images/${a.image1.file}" alt="${a.title}" width="120" height="120" loading="lazy" decoding="async">
            </span>
            <div class="card-body">
              <span class="tag">${cat.name}</span>
              <h2><a href="/${a.slug}/">${a.title}</a></h2>
              <p>${a.metaDescription}</p>
              <time datetime="${a.date}">Updated ${a.formattedDate}</time>
            </div>
          </article>
        </li>`).join('');

  const latestGuides = [
    { title: 'How to Use an Electric Callus Remover Safely', slug: 'how-to-use-electric-callus-remover-safely' },
    { title: 'Urea Cream 20% vs 40%: Key Differences', slug: 'urea-cream-20-vs-40-percent-difference' },
    { title: 'How Often Should You Use a Foot Massager?', slug: 'how-often-should-you-use-a-foot-massager' },
    { title: 'Rigid vs Soft Orthotic Insoles for Plantar Fasciitis', slug: 'rigid-vs-soft-orthotic-insoles-plantar-fasciitis' },
    { title: 'How to Heal Deep Cracked Heels Overnight', slug: 'how-to-heal-deep-cracked-heels-overnight' }
  ].map(g => `<li><a href="/${g.slug}/">${g.title}</a></li>`).join('');

  const html = `<!doctype html>
<html lang="en-US">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${cat.heading} | Beauty Feet Now</title>
<meta name="description" content="${cat.lead}">
<link rel="canonical" href="https://beautyfeetnow.com/${cat.slug}/">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
<meta property="og:locale" content="en_US">
<meta property="og:site_name" content="Beauty Feet Now">
<meta property="og:type" content="website">
<meta property="og:title" content="${cat.heading} | Beauty Feet Now">
<meta property="og:description" content="${cat.lead}">
<meta property="og:url" content="https://beautyfeetnow.com/${cat.slug}/">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#1C4E43">
<link rel="stylesheet" href="/assets/style.css">
<link rel="icon" href="/favicon.png" type="image/png">
<link rel="apple-touch-icon" href="/favicon.png">
<link rel="alternate" type="application/rss+xml" title="Beauty Feet Now" href="https://beautyfeetnow.com/feed.xml">

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://beautyfeetnow.com/" },
    { "@type": "ListItem", "position": 2, "name": "${cat.name}", "item": "https://beautyfeetnow.com/${cat.slug}/" }
  ]
}
</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>

<header class="site-header">
  <div class="wrap">
    <a class="logo" href="/" aria-label="Beauty Feet Now">
      <img src="/assets/logo.png" alt="Beauty Feet Now" width="220" height="33">
    </a>
    <nav class="nav" aria-label="Main">
      <a href="/callus-removers-and-tools/" ${cat.slug === 'callus-removers-and-tools' ? 'aria-current="page"' : ''}>Callus Removers</a>
      <a href="/foot-creams-and-lotions/" ${cat.slug === 'foot-creams-and-lotions' ? 'aria-current="page"' : ''}>Creams &amp; Lotions</a>
      <a href="/foot-massagers-and-spas/" ${cat.slug === 'foot-massagers-and-spas' ? 'aria-current="page"' : ''}>Massagers &amp; Spas</a>
      <a href="/orthotics-and-insoles/" ${cat.slug === 'orthotics-and-insoles' ? 'aria-current="page"' : ''}>Orthotics &amp; Insoles</a>
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
      <li aria-current="page">${cat.name}</li>
    </ol>
  </nav>

  <div class="hero">
    <span class="kicker">Category Hub</span>
    <h1>${cat.heading}</h1>
    <p class="lead">${cat.lead}</p>
    <nav aria-label="Related topics">
      <ul class="chips">
        ${chipsHtml}
      </ul>
    </nav>
  </div>

  <div class="layout">
    <div>
      <ul class="cards">
        ${roundupCard}
        ${articlesCards}
      </ul>
    </div>

    <aside class="side" aria-label="Sidebar">
      <div class="box">
        <h2>Categories</h2>
        <ul>
          <li><a href="/callus-removers-and-tools/">Callus Removers &amp; Tools</a></li>
          <li><a href="/foot-creams-and-lotions/">Foot Creams &amp; Lotions</a></li>
          <li><a href="/foot-massagers-and-spas/">Foot Massagers &amp; Spas</a></li>
          <li><a href="/orthotics-and-insoles/">Orthotics &amp; Insoles</a></li>
        </ul>
      </div>

      <div class="box">
        <h2>Latest guides</h2>
        <ul>
          ${latestGuides}
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

  fs.writeFileSync(path.join(__dirname, cat.slug, 'index.html'), html, 'utf8');
  console.log(`✓ Built Strict SLN Category Hub: /${cat.slug}/`);
});

console.log('\nAll 4 Category Hubs generated with 100% Strict Senior Learning Network Parity!');
