from urllib.parse import quote_plus as urlquote_plus, urljoin

import scrapy

from feeds.loaders import FeedEntryItemLoader
from feeds.spiders import FeedsSpider


class UbupComSpider(FeedsSpider):
    name = "ubup.com"
    allowed_domains = ["ubup.com"]
    # Don't filter duplicates.
    # This spider produces feeds with potentially overlapping items.
    custom_settings = {"DUPEFILTER_CLASS": "scrapy.dupefilters.BaseDupeFilter"}

    _title = "ubup"
    _subtitle = "Deutschlands größter Second Hand-Onlineshop für Mode & Accessoires"
    _base_url = "https://www.{}".format(name)
    _icon = "https://www.{}/images/favicon.ico".format(name)
    _scrape_pages = 3

    def start_requests(self):
        links = self.settings.get("FEEDS_SPIDER_UBUP_COM_LINKS")
        if links:
            links = links.split()
        else:
            links = ["katalog?sortiertnach=neueste"]

        for link in links:
            yield scrapy.Request(
                urljoin(self._base_url, link),
                meta={"dont_cache": True, "path": urlquote_plus(link)},
            )

    def feed_headers(self):
        return []

    def parse(self, response):
        if len(response.css(".thumbnail")) == 0:
            self.logger.info("No items found.")
            return

        for item in response.css(".thumbnail"):
            il = FeedEntryItemLoader(selector=item, base_url=self._base_url)
            il.add_css("title", ".item_brand_text ::text")
            il.add_css("title", ".item-title ::text")
            il.add_css("title", ".current-price ::text")
            il.add_value(
                "link",
                response.urljoin(item.css(".item-link::attr(href)").extract_first()),
            )
            image_url = item.css(".item-image::attr(style)").re_first("'([^']+)'")
            il.add_value("content_html", '<img src="{}">'.format(image_url))
            il.add_css("content_html", ".item-des-container")
            il.add_value("path", response.meta["path"])
            yield il.load_item()

        page = int(response.css(".pagination .active a::text").extract_first())
        if page == 1:
            yield self.generate_feed_header(
                title=response.css("title ::text").re_first(
                    "(ubup | .*) Second Hand kaufen"
                ),
                link=response.url,
                path=response.meta["path"],
            )
        if page < self._scrape_pages:
            next_page = response.css(
                ".pagination .active + li a::attr(href)"
            ).extract_first()
            if next_page:
                yield scrapy.Request(
                    response.urljoin(next_page),
                    meta={"dont_cache": True, "path": response.meta["path"]},
                )