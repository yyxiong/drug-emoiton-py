import scrapy

class Net39Spider(scrapy.Spider):
  name = 'net39'

  def start_requests(self):
    urls = [
      'http://quotes.toscrape.com/page/1/',
      'http://quotes.toscrape.com/page/2/',
    ]
    for url in urls:
      yield scrapy.Request(url=url, callback=self.parse)

  def parse(self, response):
    page = response.url.split("/")[-2]
    filename = 'quotes-%s.html' % page
    self.log('Saved file %s' % filename)