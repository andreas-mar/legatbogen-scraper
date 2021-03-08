# Legatbogen Scraper

Scraper utilities for Legatbogen.dk, a Danish scholarship site. Site is parsed by accessing their sitemap through their robots.txt, and relevant pages are scraped using beautifulsoup4 and requests. get_all_links.py generates a complete mapping of all relevant links and parse_page.py contains a class for extracting relevant information. As of 08-03-2021, no request throttling is needed. Outputs a .xlsx file. App lacks tags and there are many missing or erroneous values, although this is largely on Legatbogen.dk's side.
