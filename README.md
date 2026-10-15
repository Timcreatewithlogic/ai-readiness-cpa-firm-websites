# Can ChatGPT and Perplexity read CPA firm websites? 200 US firms checked (October 2026)

Original data collected by [createwithlogic](https://createwithlogic.com) on October 13, 2026.
Full write-up with context and sources: **https://createwithlogic.com/ai-readiness-cpa-firm-websites**

## What we checked

On October 13, 2026 we pulled CPA firms with a website from Google Maps in Austin, Dallas, Houston, Miami, Atlanta, Charlotte, Phoenix, Denver, Nashville and Seattle: 200 unique websites, 184 of them reachable.

For each site we:

1. read `robots.txt` with Python's standard parser (`urllib.robotparser`) for seven crawlers: OAI-SearchBot, ChatGPT-User, GPTBot, PerplexityBot, ClaudeBot, bingbot and Googlebot,
2. loaded the home page without running JavaScript and counted the visible words,
3. looked for structured data (JSON-LD) that names the firm as an organization or local business.

We loaded pages with almost no text again in a real browser to see what JavaScript adds. On October 14, 2026 we read the 184 robots.txt files again with a parser that follows the robots.txt standard, RFC 9309 ([Protego](https://github.com/scrapy/protego)), with the same counts for all seven crawlers.

## Results (184 reachable sites)

| Check | Result |
|---|---|
| Sites that block OAI-SearchBot or ChatGPT-User | 0 of 184 (0%) |
| Sites that block GPTBot (OpenAI training) | 25 of 184 (13.6%) |
| Sites that block PerplexityBot (Perplexity search) | 24 of 184 (13.0%), all on one platform |
| Home page empty without JavaScript | 3 of 184 (1.6%) |
| No structured data naming the firm | 65 of 184 (35%), corrected October 15, 2026 |

Per crawler: [`data/robots_txt_blocks_by_crawler.csv`](data/robots_txt_blocks_by_crawler.csv)

**Correction, October 15, 2026.** Our first count read the JSON-LD `@type` only when it was a single string, as in `"@type": "AccountingService"`, and checked only the first eight types of a page in alphabetical order. It missed types written as a list, such as `"@type": ["AccountingService", "LocalBusiness"]`. On October 15 we loaded the 82 sites counted without such markup again, one request per site: 17 name the firm in a list of types. Every type we had stored for them was still there two days after the first count, so we read the difference as an error in our count, not as changes to the sites. The one site we could not load again stays as first counted. Corrected result: 65 of 184 (35%) instead of 82 (45%). `scan/check_site.py` reads both forms since then.

**ChatGPT is allowed in everywhere.** None of the 184 sites blocked OAI-SearchBot (the crawler OpenAI documents for surfacing websites in ChatGPT search) or ChatGPT-User (which opens pages for a user). Blocking GPTBot is a separate choice about model training. A firm can block GPTBot and still show up in ChatGPT search.

**One in eight sites is closed to Perplexity search.** All 24 sites that disallow PerplexityBot run on the same website platform for accounting firms and share one robots.txt. It lists the crawlers it allows and ends with a rule that blocks every crawler not on the list. PerplexityBot is not on the list. Two lines in robots.txt fix it, and the platform has to add them or let the firm do so.

**Three home pages are blank without JavaScript.** They show no text without JavaScript and 300 to 550 words in a browser. Vercel and MERJ reported on December 17, 2024 that none of the major AI crawlers rendered JavaScript. In our own server logs on October 14, 2026, OpenAI's search crawler ran the JavaScript on 4 of the 7 pages it fetched, and ChatGPT-User, PerplexityBot and GPTBot showed no sign of it ([details and raw data](https://createwithlogic.com/do-ai-crawlers-render-javascript)).

## What Google's AI cites for "best CPA in [city]"

The same day we asked Google, from the US, "best accountant for small business in [city]" and "best CPA firm in [city]" for 20 large US cities and collected the AI Overviews: 32 answers, 25 with sources. Counts: [`data/ai_overview_sources.csv`](data/ai_overview_sources.csv)

- Google cited Yelp's search page for the city in 15 of 25 (60%) and its own business listings in 10 (40%).
- The 17 firms Google's AI named with a rating and a review count had a median of 85 reviews at 4.9 stars. The median across all 200 firms in the sample was 30 Google reviews.
- For "best real estate agent in [city]" (15 AI Overviews with sources), Google cited its own business listings in 13 and RealTrends rankings in 7.

These are small samples from one day and one engine, so read the shares as a direction. The website checks follow fixed rules, and anyone can repeat them.

Same method for 197 US real estate agent websites (October 14, 2026): https://github.com/Timcreatewithlogic/ai-readiness-real-estate-agent-websites. There, 23 of 189 checked sites (12%) turned a request without JavaScript away, most of them with a Cloudflare check page, against 13 of 200 CPA firm websites (6.5%) a day earlier.

## Check your own site

```bash
pip install protego   # optional: reads robots.txt per RFC 9309, as Google and Bing do
python3 scan/check_site.py https://www.yourfirm.com
```

The script loads your home page once without JavaScript, says whether a firewall turned the request away, reads your robots.txt for the AI and search crawlers listed above (plus Perplexity-User, Claude-SearchBot, Claude-User and Google-Extended), counts the words a crawler sees and lists the JSON-LD types it finds. It sends two GET requests, nothing else.

Or by hand: open `yourdomain.com/robots.txt`. If it ends with `User-agent: *` and `Disallow: /`, check that PerplexityBot, OAI-SearchBot, ChatGPT-User, Claude-SearchBot, Claude-User, bingbot and Googlebot are named above that line.

Without installing anything: paste your robots.txt into the free [AI crawler checker](https://createwithlogic.com/ai-crawler-checker). It reads the file the same way, in your browser, and shows the line that decides for each crawler.

For the rest of the picture, what ChatGPT, Gemini and Perplexity answer for your city and what your Google profile shows, there is a free [AI visibility check](https://createwithlogic.com/free-ai-visibility-check) by email.

## Free webinar, October 22, 2026

Free live webinar on Thursday, October 22, 2026, 12:00 PM ET, for US accountants, CPA and tax firms and real estate agents: how ChatGPT and other AI search tools decide which firms to recommend, and how a firm gets found there. Every registered firm gets this check and an AI answer check before the session.
Details and registration: **https://createwithlogic.com/ai-visibility-webinar**

More: [How to get your business recommended by ChatGPT: the 2026 data](https://createwithlogic.com/how-to-get-recommended-by-chatgpt) · [AI visibility for accounting firms](https://createwithlogic.com/ai-visibility-for-accounting-firms) · [GEO for accounting firms, explained with data](https://createwithlogic.com/geo-for-accounting-firms) · [The AI visibility audit for accounting firms](https://createwithlogic.com/ai-visibility-audit)

## Sources

- OpenAI: overview of OpenAI crawlers (OAI-SearchBot, ChatGPT-User, GPTBot): https://developers.openai.com/api/docs/bots
- Perplexity: Perplexity crawlers (PerplexityBot, Perplexity-User): https://docs.perplexity.ai/guides/bots
- Anthropic: how Anthropic crawls the web (ClaudeBot, Claude-User, Claude-SearchBot): https://support.claude.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler
- Vercel: The rise of the AI crawler, December 17, 2024: https://vercel.com/blog/the-rise-of-the-ai-crawler
- BrightLocal: AI directory sources, 60,970 checks, August 26, 2026: https://www.brightlocal.com/resources/ai-directory-sources/
- IETF: RFC 9309, Robots Exclusion Protocol, September 2022: https://www.rfc-editor.org/rfc/rfc9309

## License

Data and text: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Please cite as "createwithlogic, AI readiness of US CPA firm websites, October 13, 2026" with a link to https://createwithlogic.com/ai-readiness-cpa-firm-websites. Code in `scan/`: MIT, see [LICENSE](LICENSE).
