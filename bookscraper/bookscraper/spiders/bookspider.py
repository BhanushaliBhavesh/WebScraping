import scrapy


class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    def parse(self, response):
        books = response.css('article.product_pod')
        
        for book in books:
                    

            next_book_url = book.css('h3 a').attrib['href']
            if 'catalogue/' in next_book_url:
                book_url = "https://books.toscrape.com/"+next
            else:
                book_url = "https://books.toscrape.com/catalogue/"+next

            yield response.follow(book_url,callback = self.bookparse)
            



    def bookparse(self,response):
        pass
           



