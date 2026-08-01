import scrapy


class EplanSpiderSpider(scrapy.Spider):
    name = "eplan_spider"
    allowed_domains = ["dataportal.eplan.com"]

    # First test URL
    # start_urls = ["https://dataportal.eplan.com/parts/list?page=1&perpage=200"]

    #  GET API
    start_urls = [
        "https://dataportal.eplan.com/api/parts?page%5Boffset%5D=0&page%5Blimit%5D=200&sort=-download_count&fuzziness=1&context=list"
    ]

    def parse(self, response):
        # Log basic response info
        self.logger.info("*" * 50)
        self.logger.info(f"Status code: {response.status}")
        self.logger.info(f"Response URL: {response.url}")
        self.logger.info("*" * 50)

        # raw HTML file name
        # file_name = "eplan_raw_response.html"

        # Save the response as a JSON file inspect the data structure
        file_name = "api_response.json"

        # save the response body
        with open(file_name, "wb") as f:
            f.write(response.body)

        self.logger.info(f"Raw HTML successfully saved to: {file_name}")
