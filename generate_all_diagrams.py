# -*- coding: utf-8 -*-
"""
Render all 24 technical diagrams across all 12 articles into real raster WebP and PNG images.
Embeds the official Beauty Feet Now logo (assets/logo.png) in the top right badge.
Zero selectable or copyable text!
"""

import os
import re
import base64
import subprocess
from PIL import Image

import cat1_data
import cat2_data
import cat3_data
import cat4_data

os.makedirs('assets/images/diagrams', exist_ok=True)

# Read official logo
with open('assets/logo.png', 'rb') as f:
    logo_b64 = base64.b64encode(f.read()).decode('utf-8')
logo_uri = f"data:image/png;base64,{logo_b64}"

all_articles = cat1_data.ARTICLES + cat2_data.ARTICLES + cat3_data.ARTICLES + cat4_data.ARTICLES
print(f"Total articles to process diagrams for: {len(all_articles)}")

edge_exe = 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'

pattern = r'<g transform="translate\(5\d0,\s*1[4-8]\)">[\s\S]*?</g>'
badge_replacement = f'''<g transform="translate(560, 14)">
    <rect width="200" height="36" rx="8" fill="#FFFFFF" stroke="#38BDF8" stroke-width="1.5" opacity="0.95"/>
    <image href="{logo_uri}" x="12" y="6" width="176" height="24" preserveAspectRatio="xMidYMid meet"/>
  </g>'''

diagram_count = 0

for art in all_articles:
    slug = art['slug']
    for d_idx, d_key in [(1, 'diagram1'), (2, 'diagram2')]:
        diagram_count += 1
        svg = art[d_key]['svg']
        # Replace the watermark text with real official logo badge
        svg_mod = re.sub(pattern, badge_replacement, svg)
        
        # HTML wrapper for rendering
        html_content = f'''<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  html, body {{
    margin: 0;
    padding: 0;
    width: 800px;
    height: 370px;
    overflow: hidden;
    background: #0F172A;
  }}
  svg {{
    display: block;
    width: 800px;
    height: 370px;
  }}
</style>
</head>
<body>
{svg_mod}
</body>
</html>'''
        
        temp_html = f"temp_diag_{slug}_{d_idx}.html"
        temp_png = f"assets/images/diagrams/{slug}-diagram{d_idx}.png"
        webp_path = f"assets/images/diagrams/{slug}-diagram{d_idx}.webp"
        
        with open(temp_html, 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        cmd = [
            edge_exe,
            '--headless',
            '--hide-scrollbars',
            '--window-size=800,370',
            f'--screenshot={os.path.abspath(temp_png)}',
            'file:///' + os.path.abspath(temp_html).replace('\\', '/')
        ]
        
        subprocess.run(cmd, capture_output=True)
        
        if os.path.exists(temp_png):
            im = Image.open(temp_png)
            im_cropped = im.crop((0, 0, 800, 370))
            im_cropped.save(temp_png, 'PNG', optimize=True)
            im_cropped.save(webp_path, 'WEBP', quality=92)
            print(f"[{diagram_count}/24] Rendered: {webp_path} ({os.path.getsize(webp_path)} bytes)")
        else:
            print(f"FAILED to render: {temp_png}")
            
        if os.path.exists(temp_html):
            os.remove(temp_html)

print("All diagrams rendered successfully into WebP and PNG!")
