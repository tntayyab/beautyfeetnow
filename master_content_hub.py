# -*- coding: utf-8 -*-
"""
Master Content Hub for BeautyFeetNow.com
Aggregates all drafted batches into a single authoritative dictionary.
Provides instant lookup by slug or id for autonomous publishing.
"""

import sys
sys.path.insert(0, '.')

def get_all_drafts():
    all_drafts = {}
    batches = [
        'drafts_callus_batch1',
        'drafts_creams_batch1',
        'drafts_massagers_batch1',
        'drafts_orthotics_batch1',
        'drafts_specialty_batch1',
    ]
    for mod_name in batches:
        try:
            mod = __import__(mod_name)
            articles = getattr(mod, 'DRAFTS', getattr(mod, 'ARTICLES', []))
            for art in articles:
                slug = art.get('slug')
                if slug:
                    all_drafts[slug] = art
        except Exception as e:
            print(f"Warning: could not import {mod_name}: {e}")
    return all_drafts

if __name__ == '__main__':
    drafts = get_all_drafts()
    print(f"Master Content Hub loaded: {len(drafts)} complete master articles ready for automated publishing.")
    for slug, d in list(drafts.items())[:5]:
        print(f"  - {slug} ({len(d.get('sections', []))} sections, {len(d.get('faqs', []))} FAQs)")
