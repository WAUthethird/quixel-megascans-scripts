import requests
import json
import time
from pathlib import Path


# Self explanatory. If you're having issues claiming or downloading an asset because it doesn't exist anymore, this script can help get rid of that error.


update_basic_stats = True # Set to False if you don't want the stats at the top of your metadata file to be updated.


def query_quixel_page():
    while True:
        params = {"limit": 1,
                  "page": 1}

        response = requests.get("https://quixel.com/v1/assets", params=params)

        if response.status_code != 200:
            print(f"\nEncountered error! (Recieved status code {response.status_code} from Quixel server)")
            print("Waiting 5 seconds and retrying.")
            time.sleep(5)
        else:
            return response.json()


def save_asset_metadata(asset_metadata, asset_path):
    with open(asset_path / "asset_metadata.json", "w", encoding="utf-8") as f:
        json.dump(asset_metadata, f, ensure_ascii=False, indent=4)


def remove_asset_metadata(asset_metadata, asset_path):
    assets = input('\nEnter the ID of the asset(s) you want to delete metadata for, separated by commas (no spaces!) if multiple: ')

    for asset in assets.split(","):
        del asset_metadata["asset_metadata"][asset]
    
    if update_basic_stats:
        basic_stats = query_quixel_page() # Update basic stats (at top of metadata)

        asset_metadata["total"] = basic_stats["total"]
        asset_metadata["facets"] = basic_stats["facets"]

    save_asset_metadata(asset_metadata, asset_path)

    print('\nAsset(s) deleted and metadata saved!')


asset_path = Path(input("Enter the FULL path of the folder asset_metadata.json is in: "))
asset_metadata = None

try:
    with open(asset_path / "asset_metadata.json", "r", encoding="utf-8") as f:
        asset_metadata = json.load(f)
except FileNotFoundError:
    print(f"\n\nCouldn't find asset_metadata.json in the directory you selected, {asset_path}")
    input("Press Enter to exit...")

if asset_metadata:
    remove_asset_metadata(asset_metadata, asset_path)