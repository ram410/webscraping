import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from urllib.parse import urljoin
from time import sleep


class JobCrawler(scrapy.Spider):
    name = 'jobs'
    start_urls = [
        'https://internshala.com/internships/android-internship',
    ]

    def parse(self, response):
        Base_URL = 'https://internshala.com/internships'
        for article in response.css('div.company'):
            href = article.css('h4 > a::attr(href)').extract()
            url_str = ''.join(map(str, href))
            job_url = urljoin(Base_URL, url_str)
            request = scrapy.Request(url=job_url, callback=self.parse_job)
            yield request
            sleep(2)
    def parse_job(self, response):
        job = response.css('div.internship_list_container')
        yield {
            'title': job.css('span.profile_on_detail_page::text').get(),
            'company_name': job.css('a.link_display_like_text::text').get().strip(),
            'location of work': job.css('a.location_link::text').get(),
            'stipend': job.css('td.stipend_container_table_cell::text').getall()[1],
            'link': job.css('h5 > a::attr(href)').get()

        }
