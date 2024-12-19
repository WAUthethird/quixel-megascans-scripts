import requests
import json
import time
import random
from pathlib import Path
from tqdm import tqdm


# This script should be run with a COMPLETE asset_metadata.json file in the directory you wish to download images to. Simply copy it from the directory this script is in.
# Note that this script is SEPARATE from download_all_assets.py. It only downloads the preview images made available for each asset. (not textures!)
# If you want a complete archive, be sure to run this script as well. The downloaded .zip files do include a preview image, but Quixel typically provides more than that for each asset.


def download_image_set(uri_list, image_path):
    for uri in tqdm(uri_list, position=1, leave=False):
        response = requests.get(f"https://ddinktqu5prvc.cloudfront.net/{uri}", stream=True)

        if response.status_code != 200:
            try:
                json_response = response.json()
                print(f"\nEncountered error {response.status_code} with image {uri}! Here is the response from the Quixel server: {json_response}")
            except json.JSONDecodeError:
                print(f"\nEncountered error while downloading image {uri}! (Recieved status code {response.status_code} and response {response} from Quixel server)")

            print("Waiting 5 seconds and retrying.")
            time.sleep(5)
        else:
            new_image_path = image_path / uri

            new_image_path.parent.mkdir(exist_ok=True, parents=True)

            with open(new_image_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=(1024*1024)*8):
                    f.write(chunk)
        
        time.sleep(round(random.uniform(0.1, 1), 2))


def download_all_images(asset_metadata, image_path, folder_names):
    asset_images_to_download = sorted(list(set(folder_names) ^ set(asset_metadata["asset_metadata"].keys())))
    
    print(f"\n{asset_metadata["total"]} total assets in asset metadata.")
    print(f"{len(folder_names)} total asset image sets downloaded.")
    print(f"{len(asset_images_to_download)} total asset image sets not yet downloaded.")

    for asset in tqdm(asset_images_to_download):
        uri_list = [image["uri"].removeprefix("/quixel-megascans-assets/") for image in asset_metadata["asset_metadata"][asset]["full_metadata"]["previews"]["images"] if image["uri"].endswith(".png")]

        download_image_set(uri_list, image_path)
        
    print(f"\nFinished downloading {len(asset_images_to_download)} image sets!")


image_path = Path(input("Enter the FULL path of the folder you want to download images to: "))
asset_metadata = None

try:
    with open(image_path / "asset_metadata.json", "r", encoding="utf-8") as f:
        asset_metadata = json.load(f)
except FileNotFoundError:
    print(f"\n\nCouldn't find asset_metadata.json in the directory you selected, {image_path}")
    print("\nFor a proper archive, this program utilizes an asset_metadata.json file in the same directory as the image sets to determine where and how to download image sets.")
    print(f"\nSo, to run this program, simply copy your COMPLETE (basic metadata will not work!) asset_metadata.json file (made using get_all_complete_asset_metadata.py) to {image_path}\n")
    input("Press Enter to exit...")

folder_names = sorted([folder.name for folder in image_path.iterdir() if folder.is_dir()])

if asset_metadata:
    download_all_images(asset_metadata, image_path, folder_names)