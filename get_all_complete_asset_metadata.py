import requests
import json
import time
import random
from tqdm import tqdm


# This script should be run after get_all_basic_asset_metadata.py. It requires an instantiated asset_metadata.json file with all asset IDs.
# Once done, you should run claim_all_assets.py if you intend on downloading all files. Quixel will refuse file download requests without proper ownership.
# After you've claimed all assets and downloaded full metadata for each asset, you may finally proceed to run download_all_assets.py.


def query_quixel_asset(asset):
    while True:
        response = requests.get(f"https://quixel.com/v1/assets/{asset}")

        if response.status_code != 200:
            print(f"\nEncountered error with asset {asset}! (Recieved status code {response.status_code} from Quixel server)")
            print("Waiting 5 seconds and retrying.")
            time.sleep(5)
        else:
            try:
                json_response = response.json()

                return json_response
            except json.JSONDecodeError:
                print(f"Error on decode! Here is the response: {response}")
                print("Waiting 5 seconds and retrying.")
                time.sleep(5)


def get_metadata(asset_metadata):
    print(f"{asset_metadata["total"]} total assets in asset metadata. Beginning download.")
    print("There is an artificial, random delay of between 0.1 and 1 second between each request to reduce load on the Quixel servers, so expect to wait several hours.\n")


    for asset_id in tqdm(asset_metadata["asset_metadata"].keys()):
        response = query_quixel_asset(asset_id)

        if response != {}:
            asset_metadata["asset_metadata"][asset_id]["full_metadata"] = response
            time.sleep(round(random.uniform(0.1, 1), 2))
        else:
            print(f"\nSomething pretty weird has happened. If you are seeing this message, then Quixel probably messed something up with asset {asset_id}. Let me know on Github!")
            input("Press enter to proceed once you have read this message.")


    print(f"\nComplete asset metadata downloaded for {asset_metadata["total"]} assets!")
    print("Saving to asset_metadata.json... (this will take a while and produce a huge file!)")


    with open("asset_metadata.json", "w", encoding="utf-8") as f:
        json.dump(asset_metadata, f, ensure_ascii=False, indent=4)


    print("\nSaved! If you want to download all files, then make sure to run claim_all_assets.py first to add all assets to your account! Quixel will refuse file download requests without proper ownership.")
    print("Once you've done that, you can run download_all_assets.py.")


asset_metadata = None

try:
    with open("asset_metadata.json", "r", encoding="utf-8") as f:
        asset_metadata = json.load(f)
except FileNotFoundError:
    print("Couldn't find asset_metadata.json! Have you run get_all_basic_asset_metadata.py yet?\n")
    input("Press Enter to exit...")

if asset_metadata:
    get_metadata(asset_metadata)