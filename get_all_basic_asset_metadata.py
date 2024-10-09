import requests
import json
import math
import time
import random
from tqdm import tqdm


# Please run this script first to instantiate the asset_metadata.json file with necessary preparatory information.
# Once done, run claim_all_assets.py if you just want to claim every asset (add them to your account) or run get_all_complete_asset_metadata.py if you intend on downloading all files.


def query_quixel_page(limit, page):
    while True:
        params = {"limit": limit, # Max limit is 200
                  "page": page}

        response = requests.get("https://quixel.com/v1/assets", params=params)

        if response.status_code != 200:
            print(f"\nEncountered error with page {page}! (Recieved status code {response.status_code} from Quixel server)")
            print("Waiting 5 seconds and retrying.")
            time.sleep(5)
        else:
            return response.json()


# Get initial metadata
asset_metadata = query_quixel_page(1, 1)


# Set up dictionary
del asset_metadata["assets"]
del asset_metadata["page"]
del asset_metadata["pages"]
del asset_metadata["count"]
asset_metadata["asset_metadata"] = {}


total_assets = asset_metadata["total"]
pages = math.ceil(total_assets / 200) + 1 # 200 is the maximum page size, and pages start from 1


print(f"{total_assets} total assets detected.")
print(f"Downloading all basic metadata from {pages} pages with 200 items each.")
print("There is an artificial, random delay of between 0.1 and 1 second between each page fetch to reduce load on the Quixel servers, so please be patient!\n")


for page in tqdm(range(1, pages)):
    response = query_quixel_page(200, page)
    for asset in response["assets"]:
        asset_metadata["asset_metadata"][asset["id"]] = {"name": asset["name"]}
    time.sleep(round(random.uniform(0.1, 1), 2))


if len(asset_metadata["asset_metadata"]) == total_assets:
    print(f"\nSuccessfully downloaded IDs for {len(asset_metadata["asset_metadata"])} out of {total_assets} assets!")
else:
    print(f"\nOnly downloaded IDs for {len(asset_metadata["asset_metadata"])} out of {total_assets} assets! Something went wrong!")


with open("asset_metadata.json", "w", encoding="utf-8") as f:
    json.dump(asset_metadata, f, ensure_ascii=False, indent=4)


print("asset_metadata.json created! If you just want to add all assets to your account, run claim_all_assets.py next. If you want to download all files, run get_all_complete_asset_metadata.py next.")