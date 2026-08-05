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

        # TODO:
        # 1. Extract the JSON
        json_data = json.loads(response.body)

        # 2. Extract data from path inside the JSON

        # data block
        data_block = json_data.get("data", {})
        # attributes block
        attributes_block = data_block.get("attributes", {})
        # relationships block
        relationships_block = data_block.get("relationships", {})

        part_number = attributes_block.get("part_number", {})
        designation = attributes_block.get("designation", {}).get("en_US", {})
        description = attributes_block.get("description", {}).get("en_US", {})

        manufacturer_id = relationships_block.get(
            "manufacturer", {}).get("data",  {}).get("id", {})
        top_product_group_id = relationships_block.get(
            "product_top_group", {}).get("data", {}).get("id", {})
        mid_product_group_id = relationships_block.get(
            "product_group", {}).get("data", {}).get("id", {})
        sub_product_group_id = relationships_block.get(
            "product_sub_group", {}).get("data", {}).get("id", {})

        included_list = json_data.get("included", [])
        id_to_name_map = {}

        for item in included_list:
            item_id = item.get("id")
            item_type = item.get("type", "")
            item_attrs = item.get("attributes", {})

            if item_type == "manufacturers":
                id_to_name_map[item_id] = item_attrs.get(
                    "long_name") or item_attrs.get("short_name")
            elif item_type == "eplan_catalog_entries":
                id_to_name_map[item_id] = item_attrs.get(
                    "name", {})

        manufacturer_name = id_to_name_map.get(
            manufacturer_id, manufacturer_id)

        top_product_name = id_to_name_map.get(
            top_product_group_id, top_product_group_id)
        mid_product_name = id_to_name_map.get(
            mid_product_group_id, mid_product_group_id)
        sub_product_name = id_to_name_map.get(
            sub_product_group_id, sub_product_group_id)

        product_group = f"{top_product_name} - {mid_product_name} - {sub_product_name}"

        yield {
            "Part Number": part_number,
            "Manufacturer": manufacturer_name,
            "Designation": designation,
            "Description": description,
            "Product Group": product_group
        }
