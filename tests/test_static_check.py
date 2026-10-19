import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from static_check import check_html

class StaticCheckTests(unittest.TestCase):
    def test_good_html_has_no_warnings(self):
        html='''<!doctype html><html lang="ru"><head><title>Дизайн</title>
        <meta name="viewport" content="width=device-width, initial-scale=1"></head>
        <body><main><form><label for="q">Поиск</label><input id="q" name="q"/>
        <button type="submit">Искать</button></form>
        <a href="/about">О нас</a><img src="a.webp" alt="Иллюстрация"></main></body></html>'''
        result=check_html(html)
        self.assertFalse(result['errors'])
        self.assertFalse(result['warnings'])
    def test_bad_html_detected(self):
        html='''<html><body><div id="x"></div><div id="x"></div>
        <button></button><img src="bad.png"><input name="email">
        <a href="javascript:alert('x')">go</a></body></html>'''
        report=check_html(html)
        self.assertIn('duplicate id: x',report['errors'])
        self.assertIn('javascript: URL in link',report['errors'])
        self.assertTrue(any('alt' in w for w in report['warnings']))
        self.assertTrue(any('accessible' in w for w in report['warnings']))
        self.assertTrue(any('lang' in w for w in report['warnings']))
        self.assertTrue(any('name' in w for w in report['warnings']))
    def test_wrapping_label(self):
        html='''<html lang="en"><head><title>Test</title><meta name="viewport" content="width=device-width"></head>
        <body><main><label>Search <input name="query"></label></main></body></html>'''
        self.assertEqual(check_html(html)['warnings'],[])

if __name__=='__main__':unittest.main()
