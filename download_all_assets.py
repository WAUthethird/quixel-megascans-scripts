import requests
import json
import time
import hashlib
import zipfile
from pathlib import Path
from tqdm import tqdm


# All possible component types: albedo, ao, brush, bump, cavity, curvature, diffuse, displacement, displacment, f, fuzz, gloss, mask, metalness, normal, normalbump, normalobject, occlusion, opacity, roughness, specular, thickness, translucency, transmission

# This script should be run with a COMPLETE asset_metadata.json file in the directory you wish to download assets to. Simply copy it from the directory this script is in. Also, be sure that you have claimed all assets.


def save_asset_metadata(asset_metadata, asset_path):
    with open(asset_path / "asset_metadata.json", "w", encoding="utf-8") as f:
        json.dump(asset_metadata, f, ensure_ascii=False, indent=4)


def save_checksums(checksums, asset_path):
    with open(asset_path / "checksums.json", "w", encoding="utf-8") as f:
        json.dump(checksums, f, ensure_ascii=False, indent=4)


def extract_token(token):
    if token.startswith("token:\""): # Copying from Firefox dev tools, remove extra json data
        token = token.removeprefix("token:\"")
        token = token.removesuffix("\"")
    elif token.startswith("{\"token\":\""): # Copying from Chrome dev tools, remove extra json data
        token = token.split("\":\"")[1].split("\",\"")[0]

    return token


def calculate_checksum(asset, asset_path):
    with open(asset_path / f"{asset}.zip", "rb", buffering=0) as f:
        checksum = hashlib.file_digest(f, "sha256").hexdigest()
    
    return checksum


def test_zip_file(asset, asset_path):
    try:
        zipped_file = zipfile.ZipFile(asset_path / f"{asset}.zip")
    except zipfile.BadZipfile as ex:
        return False

    zip_test = zipped_file.testzip()

    if zip_test is not None:
        return False
    else:
        return True


def download_quixel_asset(asset, asset_path, download_id):
    start_bytes = 0

    while True:
        headers = {"Range": f"bytes={start_bytes}-"}
        response = requests.get(f"https://assetdownloads.quixel.com/download/{download_id}?preserveStructure=true&url=https://quixel.com/v1/downloads", headers=headers, stream=True)

        if response.status_code != 200:
            try:
                json_response = response.json()
                print(f"\nEncountered error {response.status_code} with asset {asset}! Here is the response from the Quixel server: {json_response}")
            except json.JSONDecodeError:
                print(f"\nEncountered error while downloading asset {asset}! (Recieved status code {response.status_code} and response {response} from Quixel server)")

            print("Waiting 5 seconds and retrying.")
            time.sleep(5)
        else:
            asset_length = int(response.headers["Content-Length"])

            try:
                if start_bytes == 0:
                    file_mode = "wb"
                else:
                    file_mode = "ab"

                with open(asset_path / f"{asset}.zip", file_mode) as f:
                    asset_bar = tqdm(desc=f"Downloading asset: {asset}", total=asset_length, unit="B", unit_scale=True, position=1, leave=False)

                    asset_bar.update(start_bytes)

                    for chunk in response.iter_content(chunk_size=(1024*1024)*8):
                        f.write(chunk)
                        asset_bar.update(len(chunk))

                    asset_bar.close()

                if (asset_path / f"{asset}.zip").stat().st_size != asset_length:
                    print(f"\nDownload for asset {asset} was incomplete!")
                    print("Waiting 5 seconds and resuming.")
                    start_bytes = (asset_path / f"{asset}.zip").stat().st_size
                    time.sleep(5)
                elif not test_zip_file(asset, asset_path):
                    print(f"\nDownload for asset {asset} was bad!")
                    print("Waiting 5 seconds and retrying.")
                    time.sleep(5)
                else:
                    # Success!
                    break
            except Exception as ex:
                print(f"\nError while downloading asset {asset}! Exception was {ex}")
                print("Waiting 5 seconds and retrying.")
                time.sleep(5)


def request_quixel_asset(token, asset, asset_components, asset_path):
    while True:
        headers = {"Authorization": token}

        data = {"asset": asset,
                "config": {"highpoly": True,
                           "lowerlod_meshes": True,
                           "lowerlod_normals": True,
                           "ztool": True,
                           "brushes": True,
                           "meshMimeType": "application/x-fbx",
                           "albedo_lods": True},
                "components": asset_components}

        response = requests.post("https://quixel.com/v1/downloads", headers=headers, json=data)

        if response.status_code != 200:
            try:
                json_response = response.json()
                print(f"\nEncountered error {response.status_code}! Here is the response from the Quixel server: {json_response}")

                if "code" in json_response:
                    if json_response["code"] == "ASSET_DOES_NOT_EXIST":
                        print(f"\nRequested asset {asset} does not exist! Skipping. (you will continue to recieve this message on each run as long as the asset's metadata is still present, use remove_asset_from_metadata.py to remove it)")
                        return token, False
                if "message" in json_response:
                    if json_response["message"] == "Expired token":
                        token = extract_token(input("Your Quixel token has expired! Please input a refreshed token: "))
            except json.JSONDecodeError:
                print(f"\nError on decode with code {response.status_code}! Here is the response: {response}")
            
            print("Waiting 5 seconds and retrying.")
            time.sleep(5)
        else:
            try:
                json_response = response.json()
                download_id = json_response["id"]
                download_quixel_asset(asset, asset_path, download_id)

                return token, True
            except json.JSONDecodeError:
                print(f"Error on decode! Here is the response: {response}")
                print("Waiting 5 seconds and retrying.")
                time.sleep(5)


def download_all_assets(asset_metadata, asset_path, checksums):
    token = extract_token(input("Enter your Quixel token (refer to the readme for instructions): "))

    temp_assets_to_download = list(set(checksums.keys()) ^ set(asset_metadata["asset_metadata"].keys()))
    asset_categories = list(set([asset["full_metadata"]["semanticTags"]["asset_type"] for asset in asset_metadata["asset_metadata"].values() if asset["full_metadata"]["id"] in temp_assets_to_download]))

    print(f"\n{asset_metadata["total"]} total assets in asset metadata.")
    print(f"{len(temp_assets_to_download)} total assets not yet downloaded.")
    selected_asset_type = input(f"\nWhich one of these asset categories would you like to download? {", ".join(asset_categories)}: ")

    assets_to_download = [asset["full_metadata"]["id"] for asset in asset_metadata["asset_metadata"].values() if asset["full_metadata"]["semanticTags"]["asset_type"] == selected_asset_type and asset["full_metadata"]["id"] in temp_assets_to_download]

    print(f"\n{len(assets_to_download)} assets to download.")
    print("Do NOT quit the program between downloads, as this is likely to destroy your checksum file while the .zip checksum is being saved. It is safe to quit while a file is being downloaded. When you restart the program, it will resume where it left off.")

    for asset in tqdm(assets_to_download):
        if "components" in asset_metadata["asset_metadata"][asset]["full_metadata"]: # Find all components for this asset, necessary to explicitly request .exr
            type_list = list(set([component["type"] for component in asset_metadata["asset_metadata"][asset]["full_metadata"]["components"]]))
        else:
            type_list = list(set([component["type"] for component in asset_metadata["asset_metadata"][asset]["full_metadata"]["maps"]]))
        type_list.sort()
        asset_components = [{"type": image_map, "mimeType": "image/x-exr"} for image_map in type_list]
        
        token, asset_result = request_quixel_asset(token, asset, asset_components, asset_path)
        if asset_result:
            checksum = calculate_checksum(asset, asset_path)
            checksums[asset] = checksum
            save_checksums(checksums, asset_path)

    #save_asset_metadata(asset_metadata, asset_path)

    print(f"\nFinished downloading {len(assets_to_download)} assets!")


asset_path = Path(input("Enter the FULL path of the folder you want to download assets to: "))
asset_metadata = None

try:
    with open(asset_path / "asset_metadata.json", "r", encoding="utf-8") as f:
        asset_metadata = json.load(f)
except FileNotFoundError:
    print(f"\n\nCouldn't find asset_metadata.json in the directory you selected, {asset_path}")
    print("\nFor a proper archive, this program utilizes an asset_metadata.json file in the same directory as the assets to store SHA256 hashes for each .zip file when downloading is finished.")
    print("Additionally, this file lets this program request .exr for the asset textures.")
    print(f"\nSo, to run this program, simply copy your COMPLETE (basic metadata will not work!) asset_metadata.json file (made using get_all_complete_asset_metadata.py) to {asset_path}\n")
    input("Press Enter to exit...")

if asset_metadata:
    try:
        with open(asset_path / "checksums.json", "r", encoding="utf-8") as f:
            checksums = json.load(f)
    except FileNotFoundError:
        checksums = {}

    download_all_assets(asset_metadata, asset_path, checksums)