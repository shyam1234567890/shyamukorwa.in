#!/usr/bin/env python3
"""Pre-publish check: every relative file the page references must exist, and every project card must be intact."""
import re,sys,os
root=sys.argv[1];html=open(os.path.join(root,'index.html'),encoding='utf-8').read()
bad=[]
refs=set(re.findall(r'(?:src|href|poster)="((?!data:|https?:|mailto:|#|tel:)[^"]+)"',html))
for r in sorted(refs):
    if r.startswith('javascript'):continue
    if not os.path.exists(os.path.join(root,r)):bad.append('missing file: '+r)
cards=re.findall(r'<article class="work__card[^"]*"[^>]*data-title="([^"]*)"',html)
print('cards:',len(cards));[print('  -',c) for c in cards]
for need in ['Mantra Surf Club','SAMUL','Tide and Trail','Better Funding','District','absolute','Bhudrishya','Fiber Sheet','Resort Ready','R. Garg']:
    if not any(need in c for c in cards):bad.append('missing project card: '+need)
for m in re.finditer(r'<article class="work__card[^"]*"[^>]*data-title="([^"]*)".*?</article>',html,re.S):
    a=m.group(0)
    if '<div class="work__media"' not in a:bad.append('card without cover: '+m.group(1))
    if 'work__pages' not in a:bad.append('card without gallery: '+m.group(1))
if len(html)>16*1024*1024:bad.append('index.html is over 16MB (%.1f MB)'%(len(html)/1e6))
print('index.html %.1f MB, %d relative refs checked'%(len(html)/1e6,len(refs)))
if bad:print('\nPROBLEMS:');[print(' !',b) for b in bad];sys.exit(1)
print('OK')
