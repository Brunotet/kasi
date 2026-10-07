#!/usr/bin/env python3
"""Generates the whole Kasisite site (HTML, sitemap, robots, llms.txt, README) into the repo root.

Usage:  python3 tools/build.py
Add a blog post:  edit tools/posts.py, then run this script and commit the result.
"""
import html
import json
import sys
from pathlib import Path
from urllib.parse import quote

sys.path.insert(0, str(Path(__file__).resolve().parent))
from posts import POSTS  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://kasisite.co.za"
WA_NUMBER = "27794584983"
PHONE_DISPLAY = "+27 79 458 4983"
PHONE_E164 = "+27794584983"
HOURS = "Monday to Friday, 08:00 to 17:00"
BUILD_DATE = "2026-10-07"
OG_IMAGE = SITE + "/assets/img/og.png"

WA_ICON = (
    '<svg viewBox="0 0 24 24" aria-hidden="true" fill="currentColor"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967'
    '-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788'
    '-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371'
    '-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372'
    '-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625'
    '.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421'
    ' 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436'
    '-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297'
    'A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 '
    '005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/></svg>'
)

LOGO_MARK = (
    '<svg class="logo-mark" viewBox="0 0 32 32" aria-hidden="true"><rect x="1.5" y="1.5" width="29" height="29" rx="5" '
    'fill="#ffd21f" stroke="#0d1b3e" stroke-width="3"/><path d="M11 7v18M11 17.5 20 8.5M14.5 14.5 21 25" fill="none" '
    'stroke="#0d1b3e" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
)


def wa(message: str) -> str:
    return f"https://wa.me/{WA_NUMBER}?text={quote(message)}"


WA_GENERAL = wa("Hi Kasisite, I would like a website for my business.")
WA_BLOG = wa("Hi Kasisite, I read your website cost guide and I would like a website for my business.")
WA_STARTER = wa("Hi Kasisite, I am interested in the Starter plan.")
WA_BUSINESS = wa("Hi Kasisite, I am interested in the Business plan.")
WA_ECOM = wa("Hi Kasisite, I am interested in the Ecommerce plan.")
WA_CASE = wa("Hi Kasisite, I saw your work and I would like a website like that.")

NAV = [("Pricing", "/pricing/"), ("Our work", "/work/"), ("Blog", "/blog/"), ("About", "/about/"), ("Contact", "/contact/")]

ORG = {
    "@context": "https://schema.org",
    "@type": "ProfessionalService",
    "@id": SITE + "/#business",
    "name": "Kasisite",
    "url": SITE + "/",
    "logo": SITE + "/assets/img/logo.png",
    "image": OG_IMAGE,
    "description": "Fast, mobile-friendly website design for small businesses across South Africa. Fixed prices from R1 499.",
    "telephone": PHONE_E164,
    "areaServed": {"@type": "Country", "name": "South Africa"},
    "priceRange": "R1499-R3499",
    "knowsLanguage": "en",
}
WEBSITE = {
    "@context": "https://schema.org",
    "@type": "WebSite",
    "@id": SITE + "/#website",
    "url": SITE + "/",
    "name": "Kasisite",
    "inLanguage": "en-ZA",
    "publisher": {"@id": SITE + "/#business"},
}


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def ldjson(obj) -> str:
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/") + "</script>"


def breadcrumb_schema(crumbs):
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": name, "item": SITE + path}
            for i, (name, path) in enumerate(crumbs)
        ],
    }


def crumbs_html(crumbs):
    items = []
    for i, (name, path) in enumerate(crumbs):
        if i == len(crumbs) - 1:
            items.append(f'<li aria-current="page">{esc(name)}</li>')
        else:
            items.append(f'<li><a href="{path}">{esc(name)}</a></li>')
    return f'<nav class="crumbs" aria-label="Breadcrumb"><ol>{"".join(items)}</ol></nav>'


def header(current: str) -> str:
    links = "".join(
        f'<a href="{p}"{" aria-current=\"page\"" if current.startswith(p) else ""}>{n}</a>' for n, p in NAV
    )
    return f"""<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap">
    <a class="logo" href="/" aria-label="Kasisite home">{LOGO_MARK}kasisite</a>
    <nav class="nav" aria-label="Main">{links}</nav>
    <a class="btn btn-wa header-cta" href="{WA_GENERAL}">{WA_ICON}WhatsApp us</a>
  </div>
</header>"""


def footer() -> str:
    foot_links = "".join(f'<li><a href="{p}">{n}</a></li>' for n, p in NAV)
    return f"""<footer class="site-footer">
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <a class="logo" href="/" aria-label="Kasisite home">{LOGO_MARK}kasisite</a>
        <p class="measure">Fast, fixed-price websites for small businesses across South Africa. Built remotely, paid in two halves, live in 7 days.</p>
      </div>
      <div>
        <h2>Pages</h2>
        <ul>{foot_links}</ul>
      </div>
      <div>
        <h2>Talk to us</h2>
        <ul>
          <li><a href="{WA_GENERAL}">WhatsApp {PHONE_DISPLAY}</a></li>
          <li><a href="tel:{PHONE_E164}">Call {PHONE_DISPLAY}</a></li>
          <li>{HOURS}</li>
        </ul>
      </div>
    </div>
    <p class="legal">&copy; 2026 Kasisite. Web design for South African businesses.</p>
  </div>
</footer>
<a class="float-wa" href="{WA_GENERAL}">{WA_ICON}Chat on WhatsApp</a>"""


def page(path, title, desc, body, current="", schemas=None, og_type="website", noindex=False, crumbs=None):
    """Write one page. path is a URL path such as '/pricing/'; '/' writes index.html, '/404.html' is written as is."""
    canonical = SITE + path
    schemas = list(schemas or [])
    if path == "/":
        schemas = [ORG, WEBSITE] + schemas
    else:
        schemas = [ORG] + schemas
    if crumbs:
        schemas.append(breadcrumb_schema(crumbs))
    robots = "noindex, follow" if noindex else "index, follow, max-image-preview:large"
    canonical_tag = "" if noindex else f'<link rel="canonical" href="{canonical}">\n'
    doc = f"""<!doctype html>
<html lang="en-ZA">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="{robots}">
{canonical_tag}<meta name="theme-color" content="#ffd21f">
<meta property="og:site_name" content="Kasisite">
<meta property="og:locale" content="en_ZA">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{OG_IMAGE}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{OG_IMAGE}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="preload" href="/assets/fonts/archivo-wdth.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/css/style.css">
{chr(10).join(ldjson(s) for s in schemas)}
</head>
<body>
{header(current)}
<main id="main">
{body}
</main>
{footer()}
</body>
</html>
"""
    if path == "/":
        out = ROOT / "index.html"
    elif path.endswith(".html"):
        out = ROOT / path.lstrip("/")
    else:
        out = ROOT / path.strip("/") / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(doc, encoding="utf-8")
    return out


def inner_head(crumbs, h1, lede=""):
    lede_html = f'<p class="lede">{lede}</p>' if lede else ""
    return f"""<section class="page-head wall-yellow">
  <div class="wrap">
    {crumbs_html(crumbs)}
    <h1>{h1}</h1>
    {lede_html}
  </div>
</section>"""


def cta_band(heading="Ready to get your business online?", text="Message us on WhatsApp, tell us what your business does, and we will reply within 1 business day.", link=None):
    link = link or WA_GENERAL
    return f"""<section class="section wall-yellow band-top">
  <div class="wrap">
    <h2>{heading}</h2>
    <p class="lede">{text}</p>
    <div class="btn-row">
      <a class="btn btn-wa" href="{link}">{WA_ICON}Chat on WhatsApp</a>
      <a class="btn btn-line" href="tel:{PHONE_E164}">Call {PHONE_DISPLAY}</a>
    </div>
  </div>
</section>"""


def plans_html():
    return f"""<div class="plans">
  <article class="plan">
    <h3>Starter</h3>
    <p class="who">A simple site for a portfolio, a photographer or a small business that rarely changes.</p>
    <p class="price"><span class="amount">R1&nbsp;499</span><span class="unit">once off</span></p>
    <p class="price-then none">No monthly fee</p>
    <ul>
      <li>Up to 5 pages</li>
      <li>Hosting included</li>
      <li>Free domain and SSL certificate for the first year</li>
      <li>WhatsApp button on every page</li>
      <li>One round of changes before launch</li>
      <li>Live in 7 days</li>
      <li class="no">No SEO work, blog or edits after launch. Edits are quoted one by one.</li>
    </ul>
    <a class="btn btn-wa" href="{WA_STARTER}">{WA_ICON}Choose Starter</a>
  </article>
  <article class="plan feature">
    <span class="badge">Most popular</span>
    <h3>Business</h3>
    <p class="who">For a growing business that wants to keep improving and ranking on Google.</p>
    <p class="price"><span class="amount">R1&nbsp;199</span><span class="unit">once off</span></p>
    <p class="price-then">then R499 a month</p>
    <ul>
      <li class="plus">Everything in Starter</li>
      <li>Up to 10 pages</li>
      <li>SEO: page titles and descriptions, sitemap, speed checks and a monthly search report</li>
      <li>Up to 4 small edits a month (text, photos or prices), done within 2 working days</li>
      <li>One blog post a month, 500 to 600 words, which you approve before it goes live</li>
      <li>WhatsApp support Monday to Friday, 08:00 to 17:00, with replies within 1 business day</li>
      <li>We set up your Google Business Profile if you do not have one</li>
      <li>Up to 2 custom business emails</li>
      <li>Live in 7 days</li>
    </ul>
    <a class="btn" href="{WA_BUSINESS}">{WA_ICON}Choose Business</a>
  </article>
  <article class="plan">
    <h3>Ecommerce</h3>
    <p class="who">An online shop where customers pay by payment link or order on WhatsApp.</p>
    <p class="price"><span class="amount">R3&nbsp;499</span><span class="unit">once off</span></p>
    <p class="price-then">then R599 a month</p>
    <ul>
      <li class="plus">Everything in Business</li>
      <li>Up to 50 products. We load the first 10 and you add the rest</li>
      <li>Payment links (Yoco or PayFast) and WhatsApp orders</li>
      <li>Unlimited pages</li>
      <li>Built on WordPress</li>
      <li>Live in 2 to 4 weeks</li>
    </ul>
    <a class="btn btn-wa" href="{WA_ECOM}">{WA_ICON}Choose Ecommerce</a>
  </article>
</div>
<p class="plan-note">All prices are in rand and fixed. Pay 50% to start and 50% when the site is finished.</p>"""


def phone(kind, small=True):
    if kind == "a":
        inner = ('<b>Thulani Phone &amp; PC Repair</b><span class="hd">Cracked screen? Locked phone?</span>'
                 '<span class="sub">Screens, unlocking, motherboard and PC repair.</span><span class="pill">WhatsApp now</span>'
                 '<span class="blk tall"></span><span class="blk"></span>')
    else:
        inner = ('<b>Kgotsobela Consortium</b><span class="hd">Industrial &amp; commercial HVAC, done right.</span>'
                 '<span class="sub">Installation, maintenance and repair.</span><span class="pill">Get a quote</span>'
                 '<span class="blk tall"></span><span class="blk"></span>')
    cls = "phone phone-a" if kind == "a" else "phone phone-b"
    if not small:
        cls += " phone-big"
    return f'<div class="{cls}" role="img" aria-label="Simplified preview of the website"><div class="scr">{inner}</div></div>'


# ---------------------------------------------------------------- pages
def build_home():
    body = f"""<section class="hero wall-yellow">
  <div class="wrap hero-grid">
    <div>
      <h1>Websites that bring customers to your door</h1>
      <p class="lede">Kasisite builds fast, mobile-friendly websites for small businesses across South Africa. Pick a plan, message us on WhatsApp and go live in 7 days.</p>
      <div class="btn-row">
        <a class="btn btn-wa" href="{WA_GENERAL}">{WA_ICON}Chat on WhatsApp</a>
        <a class="btn btn-line" href="/pricing/">See prices</a>
      </div>
    </div>
    <div class="tag">
      <p class="from">Websites from</p>
      <span class="amount">R1&nbsp;499</span>
      <p class="notes">Starter plan: 5 pages, hosting, and a free domain and SSL certificate for the first year.</p>
    </div>
  </div>
</section>
<div class="strip"><div class="wrap"><p>Mechanics. Caterers. Barbers. Builders. Photographers. Repair shops. Your business.</p></div></div>

<section class="section wall-chalk">
  <div class="wrap">
    <h2>What you get on every site</h2>
    <div class="facts">
      <div class="fact"><h3>A WhatsApp button on every page</h3><p>Customers message you in one tap. There are no forms to fill in, so no enquiry gets lost.</p></div>
      <div class="fact"><h3>Fast on any phone</h3><p>Pages are light, so they open quickly on cheap phones and slow data.</p></div>
      <div class="fact"><h3>Ready for Google</h3><p>Every page has its own title and description, a clean structure and a sitemap, so Google can read and list it.</p></div>
      <div class="fact"><h3>A fixed price, paid in two halves</h3><p>You know the cost before we start. Pay 50% to begin and 50% when the site is finished.</p></div>
    </div>
  </div>
</section>

<section class="section wall-yellow band-top">
  <div class="wrap">
    <h2>Real businesses, already online</h2>
    <p class="lede">We have built more than five websites for business owners. Here are two that are live today.</p>
    <div class="proof-grid">
      <article class="proof">
        <div>{phone("a")}</div>
        <div>
          <h3>Thulani Phone &amp; PC Repair</h3>
          <p class="where">Phone and PC repair, Kanyamazane</p>
          <p class="said">Thulani said the site lets him show off his business and build trust faster.</p>
          <div class="text-links"><a href="/work/thulani-phone-repair/">Read the case study</a><a href="https://thukzinmobilerepair.co.za/" target="_blank" rel="noopener">Visit the live site</a></div>
        </div>
      </article>
      <article class="proof">
        <div>{phone("b")}</div>
        <div>
          <h3>Kgotsobela Consortium</h3>
          <p class="where">HVAC engineering, Mbombela</p>
          <p class="said">Kgotsobela said the site is exactly what he imagined, and he is getting new clients every month.</p>
          <div class="text-links"><a href="/work/kgotsobela-consortium/">Read the case study</a><a href="https://kgotsobelaconsortium.co.za/" target="_blank" rel="noopener">Visit the live site</a></div>
        </div>
      </article>
    </div>
  </div>
</section>

<section class="section wall-ink">
  <div class="wrap">
    <h2>How it works</h2>
    <div class="steps">
      <div class="step"><h3>Message us on WhatsApp</h3><p>Tell us what your business does and which plan you want. Send your logo and photos if you have them.</p></div>
      <div class="step"><h3>We build your site</h3><p>Starter and Business sites go live in 7 days. Online shops take 2 to 4 weeks.</p></div>
      <div class="step"><h3>You pay in two halves</h3><p>Pay 50% to start. Pay the other 50% when the site is finished.</p></div>
    </div>
  </div>
</section>

<section class="section wall-cobalt" id="plans">
  <div class="wrap">
    <h2>Pick your plan</h2>
    <p class="lede">Fixed prices, written limits, no surprises.</p>
    {plans_html()}
  </div>
</section>

{cta_band()}"""
    page("/", "Website Design South Africa from R1 499 | Kasisite",
         "Affordable, fast websites for South African small businesses. Live in 7 days, WhatsApp button on every page, SEO on the Business plan. From R1 499.",
         body, current="/")


def build_pricing():
    crumbs = [("Home", "/"), ("Pricing", "/pricing/")]
    offers = [
        {"@type": "Offer", "name": "Starter", "description": "Up to 5 pages, hosting, free domain and SSL for the first year, WhatsApp button.",
         "price": "1499", "priceCurrency": "ZAR"},
        {"@type": "Offer", "name": "Business", "description": "Up to 10 pages, SEO, 4 small edits a month, monthly blog post, support, Google Business Profile setup, 2 custom emails.",
         "priceSpecification": [
             {"@type": "UnitPriceSpecification", "name": "Once-off fee", "price": 1199, "priceCurrency": "ZAR"},
             {"@type": "UnitPriceSpecification", "name": "Monthly fee", "price": 499, "priceCurrency": "ZAR",
              "referenceQuantity": {"@type": "QuantitativeValue", "value": 1, "unitCode": "MON"}}]},
        {"@type": "Offer", "name": "Ecommerce", "description": "Everything in Business plus up to 50 products, payment links and WhatsApp orders.",
         "priceSpecification": [
             {"@type": "UnitPriceSpecification", "name": "Once-off fee", "price": 3499, "priceCurrency": "ZAR"},
             {"@type": "UnitPriceSpecification", "name": "Monthly fee", "price": 599, "priceCurrency": "ZAR",
              "referenceQuantity": {"@type": "QuantitativeValue", "value": 1, "unitCode": "MON"}}]},
    ]
    service = {
        "@context": "https://schema.org", "@type": "Service", "name": "Website design for small businesses",
        "provider": {"@id": SITE + "/#business"}, "areaServed": {"@type": "Country", "name": "South Africa"},
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Kasisite website plans", "itemListElement": offers},
    }
    body = f"""{inner_head(crumbs, "Website design prices in South Africa", "Three fixed-price plans. Every limit is written down, so you know what you get before you pay.")}
<section class="section wall-cobalt">
  <div class="wrap">
    {plans_html()}
  </div>
</section>
<section class="section wall-chalk">
  <div class="wrap">
    <h2>Questions people ask</h2>
    <div class="faq">
      <div><h3>How long does it take?</h3><p>Starter and Business sites go live in 7 days. Ecommerce sites take 2 to 4 weeks.</p></div>
      <div><h3>How do I pay?</h3><p>You pay 50% to start and 50% when the site is finished.</p></div>
      <div><h3>What do I need to send you?</h3><p>Send your business name, what you sell or do, your logo and your photos on WhatsApp. We build the pages from that.</p></div>
      <div><h3>What is the difference between Starter and Business?</h3><p>Starter is a finished website with no monthly fee, ideal when your content rarely changes. Business adds SEO, monthly edits, a monthly blog post and support, to help you grow on Google.</p></div>
      <div><h3>Will my site rank on Google?</h3><p>Nobody can promise page one. Every site is built with the technical foundations Google needs. On the Business plan we keep improving them every month, and we publish new content that people search for.</p></div>
      <div><h3>How do shop orders and payments work?</h3><p>On the Ecommerce plan, customers pay through a payment link (Yoco or PayFast) or send their order on WhatsApp.</p></div>
    </div>
  </div>
</section>
{cta_band("Not sure which plan fits?", "Tell us about your business on WhatsApp and we will point you to the right one.")}"""
    page("/pricing/", "Website Design Prices South Africa: R1 499 to R3 499 | Kasisite",
         "Fixed-price website plans for South African businesses: Starter R1 499, Business R1 199 then R499 a month, Ecommerce R3 499 then R599 a month.",
         body, current="/pricing/", schemas=[service], crumbs=crumbs)


def build_work():
    crumbs = [("Home", "/"), ("Our work", "/work/")]
    body = f"""{inner_head(crumbs, "Websites we have built", "Two live sites from business owners in Mpumalanga. Open them on your phone and see how they feel.")}
<section class="section wall-chalk">
  <div class="wrap">
    <div class="proof-grid">
      <article class="proof">
        <div>{phone("a")}</div>
        <div>
          <h2 style="font-size:1.8rem">Thulani Phone &amp; PC Repair</h2>
          <p class="where">Phone and PC repair, Kanyamazane</p>
          <p class="said">A one-page site for a repair workshop, with WhatsApp and call buttons throughout.</p>
          <div class="text-links"><a href="/work/thulani-phone-repair/">Read the case study</a><a href="https://thukzinmobilerepair.co.za/" target="_blank" rel="noopener">Visit the live site</a></div>
        </div>
      </article>
      <article class="proof">
        <div>{phone("b")}</div>
        <div>
          <h2 style="font-size:1.8rem">Kgotsobela Consortium</h2>
          <p class="where">HVAC engineering, Mbombela</p>
          <p class="said">A five-page site for an HVAC company, with a quote button on WhatsApp.</p>
          <div class="text-links"><a href="/work/kgotsobela-consortium/">Read the case study</a><a href="https://kgotsobelaconsortium.co.za/" target="_blank" rel="noopener">Visit the live site</a></div>
        </div>
      </article>
    </div>
  </div>
</section>
{cta_band("Want a site like these?", "Message us on WhatsApp and we will tell you which plan fits your business.", WA_CASE)}"""
    page("/work/", "Our Work: Websites for South African Businesses | Kasisite",
         "See websites Kasisite has built for South African business owners, including a phone repair shop and an HVAC company in Mpumalanga.",
         body, current="/work/", crumbs=crumbs)


def case_page(slug, name, kind, lede, business_p, built, said, live_url, stats, desc, title):
    crumbs = [("Home", "/"), ("Our work", "/work/"), (name, f"/work/{slug}/")]
    built_li = "".join(f"<li>{b}</li>" for b in built)
    stat_html = "".join(f'<div class="stat"><b>{k}</b><span>{v}</span></div>' for k, v in stats)
    body = f"""{inner_head(crumbs, esc(name), lede)}
<section class="section wall-chalk">
  <div class="wrap two-col">
    <div class="prose">
      <h2>The business</h2>
      <p>{business_p}</p>
      <h2>What we built</h2>
      <ul>{built_li}</ul>
      <h2>What the owner said</h2>
      <p>{said}</p>
      <p><a href="{live_url}" target="_blank" rel="noopener">Visit the live site</a> or <a href="/work/">see all our work</a>.</p>
      <div class="stat-row">{stat_html}</div>
    </div>
    <div>
      {phone(kind, small=False)}
      <p class="caption">A simplified preview. Open the live site to see the real thing.</p>
    </div>
  </div>
</section>
{cta_band("Want a site like this?", "Message us on WhatsApp and tell us about your business.", WA_CASE)}"""
    page(f"/work/{slug}/", title, desc, body, current="/work/", crumbs=crumbs,
         schemas=[{"@context": "https://schema.org", "@type": "WebPage", "name": title, "url": f"{SITE}/work/{slug}/",
                   "isPartOf": {"@id": SITE + "/#website"}, "about": name}])


def build_cases():
    case_page(
        "thulani-phone-repair", "Thulani Phone & PC Repair", "a",
        "A one-page website that shows a repair workshop in Kanyamazane at its best and sends customers straight to WhatsApp.",
        "Thulani repairs phones and computers in Kanyamazane (Lekazi), Mbombela. He fixes screens, unlocks phones, repairs motherboards at chip level, replaces batteries and charging ports, repairs PCs and laptops, and sells tested unlocked phones.",
        ["One page with a clear section for each of the six services.",
         "A gallery of real repair work and two repair videos, so customers see the workshop before they visit.",
         "A phones-for-sale section where each phone has its own WhatsApp link.",
         "WhatsApp and call buttons throughout the page, plus a map and opening hours.",
         "Page title, description and social sharing tags written around Kanyamazane, Lekazi and Mbombela."],
        "Thulani said the site lets him show off his business and build trust faster.",
        "https://thukzinmobilerepair.co.za/",
        [("Business", "Phone and PC repair"), ("Place", "Kanyamazane (Lekazi), Mbombela"), ("Site", "One page, WhatsApp in every section")],
        "How Kasisite built a fast one-page website for Thulani Phone & PC Repair in Kanyamazane, with WhatsApp and call buttons throughout.",
        "Thulani Phone & PC Repair Case Study | Kasisite",
    )
    case_page(
        "kgotsobela-consortium", "Kgotsobela Consortium", "b",
        "A five-page website for an HVAC and mechanical engineering company in Mbombela, with a quote button on WhatsApp.",
        "Kgotsobela Consortium installs, maintains and repairs industrial and commercial heating, ventilation, air conditioning and refrigeration systems for clients across Mpumalanga. The company was founded in 2012.",
        ["Five pages: Home, About, Services, Projects and Contact.",
         "A services page covering twelve services, with service cards on the home page that each open WhatsApp with a ready-made quote message.",
         "A photo gallery of the team, the vans and the work on site.",
         "A Get a quote button in the header and at the end of the page.",
         "Page titles and descriptions written around HVAC in Mbombela and Mpumalanga."],
        "Kgotsobela said the site is exactly what he imagined, and he is getting new clients every month.",
        "https://kgotsobelaconsortium.co.za/",
        [("Business", "HVAC and mechanical engineering"), ("Place", "Mbombela, Mpumalanga"), ("Site", "Five pages, quote on WhatsApp")],
        "How Kasisite built a five-page website for Kgotsobela Consortium, an HVAC company in Mbombela, with a WhatsApp quote button.",
        "Kgotsobela Consortium HVAC Website Case Study | Kasisite",
    )


def build_about():
    crumbs = [("Home", "/"), ("About", "/about/")]
    body = f"""{inner_head(crumbs, "A web design studio for South African businesses", "Kasisite builds simple, fast websites at fixed prices, so small businesses can show up online without the agency price tag.")}
<section class="section wall-chalk">
  <div class="wrap">
    <div class="prose">
      <h2>Who we are</h2>
      <p>Kasisite is a South African web design studio. We build fast websites for small businesses and work remotely with clients across the country. We have built more than five websites for business owners, including <a href="/work/thulani-phone-repair/">Thulani Phone &amp; PC Repair</a> and <a href="/work/kgotsobela-consortium/">Kgotsobela Consortium</a>.</p>
      <h2>How we work</h2>
      <ul>
        <li>Everything happens on WhatsApp. You message us, we reply within 1 business day.</li>
        <li>Prices are fixed and written down before we start.</li>
        <li>Starter and Business sites go live in 7 days. Online shops take 2 to 4 weeks.</li>
        <li>You pay 50% to start and 50% when the site is finished.</li>
      </ul>
      <h2>Why Kasisite?</h2>
      <p>Kasi is South African slang for neighbourhood. Small businesses in every neighbourhood deserve a website that looks as good as their work, and a price they can afford.</p>
      <div class="btn-row"><a class="btn btn-wa" href="{WA_GENERAL}">{WA_ICON}Chat on WhatsApp</a><a class="btn btn-line" href="/pricing/">See prices</a></div>
    </div>
  </div>
</section>"""
    page("/about/", "About Kasisite: Web Design for South African Businesses",
         "Kasisite is a South African web design studio. Fixed prices, WhatsApp-first service, and websites that go live in 7 days.",
         body, current="/about/", crumbs=crumbs)


def build_contact():
    crumbs = [("Home", "/"), ("Contact", "/contact/")]
    body = f"""{inner_head(crumbs, "Message us on WhatsApp", "It is the fastest way to reach us. Tell us what your business does and which plan you like.")}
<section class="section wall-chalk">
  <div class="wrap">
    <div class="prose">
      <div class="btn-row" style="margin-top:0"><a class="btn btn-wa" href="{WA_GENERAL}">{WA_ICON}Chat on WhatsApp</a><a class="btn btn-line" href="tel:{PHONE_E164}">Call {PHONE_DISPLAY}</a></div>
      <h2>Opening hours</h2>
      <p>{HOURS}. We reply to every message within 1 business day.</p>
      <h2>What to send us</h2>
      <ul>
        <li>Your business name and what you do or sell.</li>
        <li>Your logo and photos, if you have them.</li>
        <li>The plan you like, or ask us which one fits.</li>
      </ul>
      <h2>Where we work</h2>
      <p>We work remotely with clients across all of South Africa.</p>
    </div>
  </div>
</section>"""
    page("/contact/", "Contact Kasisite: WhatsApp +27 79 458 4983",
         "Message Kasisite on WhatsApp to get a website for your business. We reply within 1 business day, Monday to Friday.",
         body, current="/contact/", crumbs=crumbs)


def fmt_date(iso: str) -> str:
    y, m, d = iso.split("-")
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    return f"{int(d)} {months[int(m) - 1]} {y}"


def build_blog():
    crumbs = [("Home", "/"), ("Blog", "/blog/")]
    items = "".join(
        f"""<article class="post-item"><p class="meta">{fmt_date(p['date'])}</p><h2><a href="/blog/{p['slug']}/">{esc(p['title'])}</a></h2><p>{esc(p['description'])}</p></article>"""
        for p in POSTS
    )
    body = f"""{inner_head(crumbs, "Website tips for small businesses", "Plain advice on getting your business online and found on Google in South Africa.")}
<section class="section wall-chalk">
  <div class="wrap"><div class="post-list">{items}</div></div>
</section>"""
    page("/blog/", "Blog: Website Tips for South African Small Businesses | Kasisite",
         "Plain advice on website costs, getting found on Google and growing a small business online in South Africa.",
         body, current="/blog/", crumbs=crumbs)

    for p in POSTS:
        pc = [("Home", "/"), ("Blog", "/blog/"), (p["title"], f"/blog/{p['slug']}/")]
        article = {
            "@context": "https://schema.org", "@type": "BlogPosting", "headline": p["title"], "description": p["description"],
            "datePublished": p["date"], "dateModified": p["date"], "image": OG_IMAGE, "inLanguage": "en-ZA",
            "mainEntityOfPage": f"{SITE}/blog/{p['slug']}/",
            "author": {"@id": SITE + "/#business"}, "publisher": {"@id": SITE + "/#business"},
        }
        content = p["body"].replace("%%WA_BLOG%%", WA_BLOG)
        body = f"""{inner_head(pc, esc(p['title']))}
<section class="section wall-chalk">
  <div class="wrap">
    <div class="prose">
      <p class="meta">Published {fmt_date(p['date'])} by Kasisite</p>
      {content}
    </div>
  </div>
</section>
{cta_band()}"""
        page(f"/blog/{p['slug']}/", f"{p['title']} | Kasisite", p["description"], body, current="/blog/",
             schemas=[article], og_type="article", crumbs=pc)


def build_404():
    body = f"""<section class="section wall-yellow notfound">
  <div class="wrap">
    <h1>That page does not exist</h1>
    <p class="lede">The link may be old or mistyped. Go back to the home page, or message us on WhatsApp.</p>
    <div class="btn-row"><a class="btn" href="/">Back to home</a><a class="btn btn-wa" href="{WA_GENERAL}">{WA_ICON}Chat on WhatsApp</a></div>
  </div>
</section>"""
    page("/404.html", "Page not found | Kasisite", "This page could not be found.", body, noindex=True)


# ---------------------------------------------------------------- technical files
def build_files():
    urls = [("/", "1.0"), ("/pricing/", "0.9"), ("/work/", "0.7"), ("/work/thulani-phone-repair/", "0.6"),
            ("/work/kgotsobela-consortium/", "0.6"), ("/about/", "0.5"), ("/contact/", "0.5"), ("/blog/", "0.7")]
    urls += [(f"/blog/{p['slug']}/", "0.8") for p in POSTS]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for path, prio in urls:
        lastmod = BUILD_DATE
        for p in POSTS:
            if path == f"/blog/{p['slug']}/":
                lastmod = p["date"]
        sm.append(f"  <url><loc>{SITE}{path}</loc><lastmod>{lastmod}</lastmod><priority>{prio}</priority></url>")
    sm.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(sm) + "\n", encoding="utf-8")

    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n", encoding="utf-8")
    (ROOT / "CNAME").write_text("kasisite.co.za\n", encoding="utf-8")
    (ROOT / ".nojekyll").write_text("", encoding="utf-8")
    (ROOT / "favicon.svg").write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect x="1.5" y="1.5" width="29" height="29" rx="5" '
        'fill="#ffd21f" stroke="#0d1b3e" stroke-width="3"/><path d="M11 7v18M11 17.5 20 8.5M14.5 14.5 21 25" fill="none" '
        'stroke="#0d1b3e" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/></svg>\n', encoding="utf-8")

    post_lines = "\n".join(f"- [{p['title']}]({SITE}/blog/{p['slug']}/): {p['description']}" for p in POSTS)
    llms = f"""# Kasisite

> Kasisite is a South African web design studio. It builds fast, mobile-friendly websites for small businesses at fixed prices, working remotely with clients across South Africa.

## Plans (prices in South African rand)
- Starter: R1 499 once off. Up to 5 pages, hosting, free domain and SSL for the first year, WhatsApp button. Live in 7 days.
- Business: R1 199 once off, then R499 a month. Up to 10 pages, SEO, up to 4 small edits a month, one blog post a month, WhatsApp support, Google Business Profile setup, up to 2 custom business emails. Live in 7 days.
- Ecommerce: R3 499 once off, then R599 a month. Everything in Business plus up to 50 products, payment links and WhatsApp orders. Live in 2 to 4 weeks.
- Payment: 50% to start and 50% when the site is finished.

## Pages
- [Pricing]({SITE}/pricing/)
- [Our work]({SITE}/work/)
- [About]({SITE}/about/)
- [Contact]({SITE}/contact/)

## Blog
{post_lines}

## Contact
- WhatsApp: {PHONE_DISPLAY}
- Hours: {HOURS}
"""
    (ROOT / "llms.txt").write_text(llms, encoding="utf-8")


def main():
    build_home()
    build_pricing()
    build_work()
    build_cases()
    build_about()
    build_contact()
    build_blog()
    build_404()
    build_files()
    print("Built Kasisite site into", ROOT)


if __name__ == "__main__":
    main()
