import scrapy
from bookscraper.items import BookItem

class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    def parse(self, response):
       
       
        books = response.css('article.product_pod')
        
        for book in books:
                    

            next_book_url = book.css('h3 a').attrib['href']
            if 'catalogue/' in next_book_url:
                book_url = "https://books.toscrape.com/"+next_book_url
            else:
                book_url = "https://books.toscrape.com/catalogue/"+next_book_url

            yield response.follow(book_url,callback = self.bookparse)


#
#        
#        next_page = response.xpath("//li[@class='next']/a/@href").get()
#

#        if next_page is not None:
#
#            if 'catalogue/' in next_page:
#                    next_page_url = "https://books.toscrape.com/"+next_page
#            else:
#                    next_page_url = "https://books.toscrape.com/catalogue/"+next_page
#            
#            yield response.follow(next_page_url,callback = self.parse)
#

    def bookparse(self,response):
        
       
        table = response.xpath("//table[@class = 'table table-striped']")
        
        book_item = BookItem()


        book_item['url'] = response.url
        book_item['title'] = response.xpath("//div/h1/text()").get()
        book_item['category'] = response.xpath("//li[@class='active'] //preceding-sibling::li[1]/a/text()").get()
        book_item['stars'] = response.xpath("//p[contains(@class, 'star-rating')]/@class").get()
        book_item['product_description'] = response.xpath("//div[@id = 'product_description'] //following-sibling::p/text()").get()
        book_item['upc'] = table.xpath("//tr[1]/td[1]/text()").get()
        book_item['product_type'] = table.xpath("//tr[2]/td[1]/text()").get()
        book_item['price_execluding_tax'] = table.xpath("//tr[3]/td[1]/text()").get()
        book_item['price_including_tax'] = table.xpath("//tr[4]/td[1]/text()").get()
        book_item['tax'] = table.xpath("//tr[5]/td[1]/text()").get()
        book_item['availablity'] = table.xpath("//tr[6]/td[1]/text()").get()
        book_item['number_of_reviews'] = table.xpath("//tr[7]/td[1]/text()").get()
    

        yield book_item