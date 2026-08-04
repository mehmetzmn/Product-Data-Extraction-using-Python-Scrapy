import scrapy
import json


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
        # Convert response body to a python dictionary
        json_data = json.loads(response.body)

        # Get the list of parts from the "data" key
        parts_list = json_data.get("data", [])
        self.logger.info(f"Found {len(parts_list)} parts in the list API")

        # Loop through the parts
        for part in parts_list:
            part_id = part.get("id")

            if part_id:
                # Construct the Detail API URL for each part
                detail_url = f"https://dataportal.eplan.com/api/parts/{part_id}?context=detail"

                # Send a new request to the Detail API and pass the response to 'parse_detail' method
                yield scrapy.Request(
                    url=detail_url,
                    callback=self.parse_detail
                )

                # Break after the first time just for testing and inspecting the structure
                break

    def parse_detail(self, response):
        # This method handles the response from the Detail API
        self.logger.info(f"Successfully reached Detail API: {response.url}")

        # Save ONE detail response to inspect its structure
        file_name = "single_detail_response.json"
        with open(file_name, "wb") as f:
            f.write(response.body)

        self.logger.info(f"Saved detail data to: {file_name}")
