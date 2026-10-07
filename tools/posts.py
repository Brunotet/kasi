"""Blog posts for Kasisite.

To add a post: append a dict to POSTS, then run `python3 tools/build.py`.
Fields: slug (URL part), title (the H1), description (meta description, under 155 characters),
date (YYYY-MM-DD), body (HTML for the article body; use <h2>, <p>, <ul><li>).
Newest post first.
"""

POSTS = [
    {
        "slug": "website-cost-south-africa",
        "title": "How much does a website cost in South Africa?",
        "description": "What small business websites cost in South Africa in 2026, what quotes often leave out, and what to ask before you pay.",
        "date": "2026-10-07",
        "body": """
<p>A simple small business website in South Africa costs from about R1 500 to R15 000 or more, depending on who builds it and what is included. An online shop costs more. The number on the quote matters less than what the quote leaves out.</p>

<h2>What do agencies charge?</h2>
<p>Prices published by South African web design agencies in 2026 fall into three bands:</p>
<ul>
<li>Monthly plans from about R299 a month. Check what happens to the site if you stop paying.</li>
<li>Custom builds from about R10 000. Professional business sites are often quoted at R15 000 or more.</li>
<li>Online shops from about R15 000, rising to R200 000 for complex stores.</li>
</ul>
<p>These figures come from agency price lists we reviewed in 2026. Treat them as starting points, not quotes.</p>

<h2>What should a small business website include?</h2>
<p>Before you compare prices, make sure every quote covers the basics:</p>
<ul>
<li>A domain name, such as yourbusiness.co.za.</li>
<li>Hosting, so the site stays online.</li>
<li>An SSL certificate. This is the padlock that stops browsers warning visitors the site is not secure.</li>
<li>A design that works well on a phone, because most South Africans browse on one.</li>
<li>A clear way to contact you. For many businesses that is a WhatsApp button on every page.</li>
<li>Basic search setup: a title and description for every page, and a sitemap so Google can read the site.</li>
</ul>

<h2>What usually costs extra?</h2>
<p>Ask about each of these, because they are where a cheap quote becomes an expensive year:</p>
<ul>
<li>Renewing the domain name every year.</li>
<li>Business email addresses, such as info@yourbusiness.co.za.</li>
<li>Changes after the site goes live.</li>
<li>Writing blog posts.</li>
<li>Ongoing SEO work to help you rank on Google.</li>
</ul>

<h2>Is a once-off price or a monthly price better?</h2>
<p>A once-off price suits a site that rarely changes, such as a photographer's portfolio. You pay once and the site does its job.</p>
<p>A monthly price suits a business that wants to grow on Google. The monthly fee pays for updates, new blog posts and regular search work, so the site keeps improving instead of standing still.</p>

<h2>What should you ask before you pay?</h2>
<ul>
<li>Is the price fixed, or can it change once work starts?</li>
<li>Who owns the domain name?</li>
<li>What happens to my site if I stop paying the monthly fee?</li>
<li>How many changes are included after launch, and how fast are they done?</li>
<li>How quickly does the site open on a cheap phone with slow data?</li>
</ul>

<h2>What does Kasisite charge?</h2>
<p>Kasisite has three fixed-price plans, each paid in two halves: 50% to start and 50% when the site is finished.</p>
<ul>
<li><strong>Starter, R1 499 once off.</strong> Up to 5 pages, hosting, a free domain and SSL certificate for the first year, and a WhatsApp button. Live in 7 days.</li>
<li><strong>Business, R1 199 once off then R499 a month.</strong> Up to 10 pages, SEO, up to 4 small edits a month, one blog post a month, support, and more. Live in 7 days.</li>
<li><strong>Ecommerce, R3 499 once off then R599 a month.</strong> Everything in Business, plus up to 50 products with payment links and WhatsApp orders. Live in 2 to 4 weeks.</li>
</ul>
<p>See exactly what each plan includes on the <a href="/pricing/">pricing page</a>, or <a href="%%WA_BLOG%%">message us on WhatsApp</a> and tell us what your business needs.</p>
""",
    },
]
