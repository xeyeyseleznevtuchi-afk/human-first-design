#!/usr/bin/env python3
"""Fast, dependency-free HTML preflight. Heuristics only: not a visual or security audit.
Usage: python3 scripts/static_check.py path/to/page.html [--json]
"""
from __future__ import annotations
import argparse
import json
from html.parser import HTMLParser
from pathlib import Path
from collections import Counter

class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tags=[]
        self.ids=[]
        self.labels=set()
        self.titles=0
        self.viewport=False
        self.html_lang=False
        self.main=0
        self.errors=[]
        self.warnings=[]
        self._label_depth=0
        self._input_records=[]
        self._buttons=[]
        self._button_stack=[]

    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        self.tags.append((tag,a))
        if a.get('id'): self.ids.append(a['id'])
        if tag=='html': self.html_lang=bool(a.get('lang','').strip())
        if tag=='title': self.titles+=1
        if tag=='main': self.main+=1
        if tag=='meta' and a.get('name','').lower()=='viewport': self.viewport=True
        if tag=='label':
            self._label_depth+=1
            if a.get('for'): self.labels.add(a['for'])
        if tag in ('input','textarea','select'):
            self._input_records.append((tag,a,self._label_depth>0))
        if tag=='img' and 'alt' not in a:
            self.warnings.append('img without alt: '+str(a.get('src',''))[:110])
        if tag=='a':
            href=(a.get('href') or '').strip()
            if not href or href=='#': self.warnings.append('anchor without real destination')
            if href.lower().startswith('javascript:'): self.errors.append('javascript: URL in link')
            if a.get('target')=='_blank' and 'noopener' not in (a.get('rel') or ''):
                self.warnings.append('target=_blank missing rel=noopener')
        if tag=='button':
            self._button_stack.append({'attrs':a,'text':''})
            if not a.get('type'): self.warnings.append('button missing explicit type')
    def handle_data(self,data):
        if self._button_stack: self._button_stack[-1]['text']+=data
    def handle_endtag(self,tag):
        if tag=='label' and self._label_depth: self._label_depth-=1
        if tag=='button' and self._button_stack: self._buttons.append(self._button_stack.pop())

    def finalize(self):
        dup=[name for name,n in Counter(self.ids).items() if n>1]
        for name in dup: self.errors.append('duplicate id: '+name)
        if not self.html_lang: self.warnings.append('html lang missing')
        if not self.titles: self.warnings.append('document title missing')
        if not self.viewport: self.warnings.append('viewport meta missing')
        if not self.main: self.warnings.append('main landmark missing')
        if self.main>1: self.warnings.append('more than one main landmark')
        for tag,a,wrapped in self._input_records:
            if a.get('type')=='hidden': continue
            if not (wrapped or (a.get('id') and a['id'] in self.labels) or
                    a.get('aria-label') or a.get('aria-labelledby')):
                self.warnings.append(f'{tag} missing explicit accessible label: '+str(a.get('name') or a.get('id') or 'unnamed'))
        for b in self._buttons:
            a=b['attrs']
            if not (b['text'].strip() or a.get('aria-label') or a.get('aria-labelledby') or a.get('title')):
                self.warnings.append('button may lack accessible name')
        return {'errors':self.errors,'warnings':self.warnings,
                'checked':'HTML markup heuristic; NOT browser, visual, security, contrast, or keyboard test'}

def check_html(s:str)->dict:
    p=PageParser();p.feed(s);p.close();return p.finalize()

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('html',type=Path)
    ap.add_argument('--json',action='store_true')
    opt=ap.parse_args()
    report=check_html(opt.html.read_text(encoding='utf-8'))
    if opt.json: print(json.dumps(report,ensure_ascii=False,indent=2))
    else:
        print('HTML heuristic preflight:',opt.html)
        for k in ('errors','warnings'):
            print(f'{k}: {len(report[k])}')
            for m in report[k]: print('  -',m)
        print(report['checked'])
    return 1 if report['errors'] else 0

if __name__=='__main__': raise SystemExit(main())
