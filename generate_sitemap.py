# generate_sitemap.py
import datetime

BASE_URL = "https://beautyfeetnow.com"
today = datetime.date.today().isoformat()

pages = [
    ('/', '1.0', 'daily'),
    ('/page/2/', '0.7', 'weekly'),
    ('/callus-removers-and-tools/', '0.8', 'weekly'),
    ('/foot-creams-and-lotions/', '0.8', 'weekly'),
    ('/foot-massagers-and-spas/', '0.8', 'weekly'),
    ('/orthotics-and-insoles/', '0.8', 'weekly'),
    ('/best-electric-callus-removers/', '0.9', 'weekly'),
    ('/best-cracked-heel-creams-with-urea/', '0.9', 'weekly'),
    ('/best-heated-foot-massagers-for-plantar-fasciitis/', '0.9', 'weekly'),
    ('/best-orthotic-insoles-for-flat-feet/', '0.9', 'weekly'),
    ('/how-to-use-electric-callus-remover-safely/', '0.9', 'weekly'),
    ('/nano-glass-foot-file-vs-electric-callus-remover/', '0.9', 'weekly'),
    ('/why-do-foot-calluses-keep-coming-back/', '0.9', 'weekly'),
    ('/urea-cream-20-vs-40-percent-difference/', '0.9', 'weekly'),
    ('/how-to-heal-deep-cracked-heels-overnight/', '0.9', 'weekly'),
    ('/salicylic-acid-vs-lactic-acid-for-rough-feet/', '0.9', 'weekly'),
    ('/how-often-should-you-use-a-foot-massager/', '0.9', 'weekly'),
    ('/shiatsu-vs-air-compression-foot-massager/', '0.9', 'weekly'),
    ('/why-do-feet-burn-at-night-causes-and-relief/', '0.9', 'weekly'),
    ('/rigid-vs-soft-orthotic-insoles-plantar-fasciitis/', '0.9', 'weekly'),
    ('/how-to-tell-if-you-have-flat-feet-or-high-arches/', '0.9', 'weekly'),
    ('/signs-you-need-custom-orthotics-vs-otc-insoles/', '0.9', 'weekly'),
    ('/how-we-test/', '0.7', 'monthly'),
    ('/about-us/', '0.7', 'monthly'),
    ('/editorial-policy/', '0.6', 'monthly'),
    ('/contact/', '0.6', 'monthly'),
    ('/affiliate-disclosure/', '0.5', 'monthly'),
    ('/privacy-policy/', '0.5', 'monthly'),
    ('/terms-of-service/', '0.5', 'monthly'),
]

xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for path, pri, freq in pages:
    xml.append('  <url>')
    xml.append(f'    <loc>{BASE_URL}{path}</loc>')
    xml.append(f'    <lastmod>{today}</lastmod>')
    xml.append(f'    <changefreq>{freq}</changefreq>')
    xml.append(f'    <priority>{pri}</priority>')
    xml.append('  </url>')
xml.append('</urlset>')

with open('sitemap.xml', 'w', encoding='utf-8') as f:
    f.write('\n'.join(xml) + '\n')

print(f"Generated sitemap.xml with {len(pages)} URLs!")
