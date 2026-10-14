"""Check how AI and search crawlers see a website.

Reads robots.txt for the AI and search crawlers, counts the visible words on the home page
without running JavaScript and lists the JSON-LD types. Two GET requests per site, nothing else.

Usage: python3 check_site.py https://www.yourfirm.com [https://another-site.com ...]
Standard library only (Python 3.9+).
"""
import re
import ssl
import sys
import urllib.error
import urllib.request
import urllib.robotparser
from urllib.parse import urlparse

BROWSER = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
           '(KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36')

# (crawler, operator, what it is used for). The October 2026 study used the first seven.
CRAWLERS = [
    ('OAI-SearchBot', 'OpenAI', 'ChatGPT search'),
    ('ChatGPT-User', 'OpenAI', 'opens pages for a ChatGPT user'),
    ('GPTBot', 'OpenAI', 'model training'),
    ('PerplexityBot', 'Perplexity', 'Perplexity search'),
    ('ClaudeBot', 'Anthropic', 'model training'),
    ('bingbot', 'Microsoft', 'Bing search and Copilot'),
    ('Googlebot', 'Google', 'Google Search, AI Overviews, AI Mode'),
    ('Perplexity-User', 'Perplexity', 'opens pages for a Perplexity user'),
    ('Claude-SearchBot', 'Anthropic', 'Claude search'),
    ('Claude-User', 'Anthropic', 'opens pages for a Claude user'),
    ('Google-Extended', 'Google', 'Gemini training (does not affect Search)'),
]

ORG_TYPES = {'Organization', 'LocalBusiness', 'AccountingService', 'ProfessionalService', 'FinancialService',
             'LegalService', 'Corporation', 'RealEstateAgent'}


def fetch(url, limit=1_500_000):
    req = urllib.request.Request(url, headers={'User-Agent': BROWSER, 'Accept': 'text/html,*/*',
                                               'Accept-Language': 'en-US'})
    try:
        with urllib.request.urlopen(req, timeout=15, context=ssl.create_default_context()) as r:
            return r.status, r.read(limit).decode('utf-8', 'replace')
    except urllib.error.HTTPError as e:
        return e.code, ''
    except Exception as e:
        return None, type(e).__name__


def words_without_js(html):
    h = re.sub(r'(?is)<(script|style|noscript|template|svg|head)[^>]*>.*?</\1>', ' ', html)
    h = re.sub(r'(?s)<!--.*?-->', ' ', h)
    t = re.sub(r'<[^>]+>', ' ', h)
    t = re.sub(r'&[a-z#0-9]+;', ' ', t)
    return len(re.findall(r'[A-Za-z]{2,}', t))


def jsonld_types(html):
    blocks = re.findall(r'(?is)<script[^>]+ld\+json[^>]*>(.*?)</script>', html)
    return sorted(set(re.findall(r'"@type"\s*:\s*"([A-Za-z]+)"', ' '.join(blocks))))


def check(site):
    u = urlparse(site if site.startswith('http') else 'https://' + site)
    base = f'{u.scheme}://{u.netloc}'
    status, html = fetch(base + '/')
    rb_status, robots = fetch(base + '/robots.txt', 300_000)
    rp = urllib.robotparser.RobotFileParser()
    rp.parse(robots.splitlines() if rb_status == 200 else [])

    print(f'\n{base}  (home page HTTP {status}, robots.txt HTTP {rb_status})')
    for name, operator, purpose in CRAWLERS:
        allowed = rb_status != 200 or rp.can_fetch(name, base + '/')
        print(f'  {"allowed" if allowed else "BLOCKED":8} {name:17} {operator:11} {purpose}')
    if status == 200:
        words = words_without_js(html)
        types = jsonld_types(html)
        print(f'  Words on the home page without JavaScript: {words}'
              + ('  <- AI crawlers that do not run JavaScript see an empty page' if words < 50 else ''))
        print(f'  JSON-LD types: {", ".join(types) or "none"}'
              + ('' if set(types) & ORG_TYPES else '  <- nothing names the business'))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    for s in sys.argv[1:]:
        check(s)
