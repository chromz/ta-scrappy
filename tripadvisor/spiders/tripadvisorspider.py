# -*- coding: utf-8 -*-
"""
    Class that reprsents a scrappy spider
"""

import scrapy
from tripadvisor.items import Review


class TripAdvisorReview(scrapy.Spider):
    name = "tripadvisor"
    start_urls = ["https://www.tripadvisor.com/Hotels-g292006-Guatemala_City_Guatemala_Department-Hotels.html"]

    def parse(self, response):
        urls = []
        for href in response.css("div.meta_listing::attr(data-url)").getall():
            if href not in urls:
                urls.append(href)
                yield response.follow(href, callback=self.parse_review)

        next_page = response.css("a.nav.next::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse_review)

    def parse_review(self, response):
        sub_div = response.css("div.location-review-review-list-parts-SingleReview__mainCol--1hApa")

        for review in sub_div:
            contents = review.css(
                "q.location-review-review-list-parts-ExpandableReview__reviewText--gOmRC span::text"
            ).get()
            content = str(contents.encode("utf-8"), "utf-8")
            ratings = review.css("span.ui_bubble_rating").xpath("@*").get()
            rating = int(ratings.split(' ')[-1].replace('bubble_', ''))

            yield Review(
                rating=rating,
                review=content,
            )
        next_page = response.css("a.nav.next::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse_review)
