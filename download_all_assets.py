import requests
import json
import hashlib
import time
from pathlib import Path
from tqdm import tqdm
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from concurrent.futures import ThreadPoolExecutor, as_completed

# Set up a requests session with retry
def get_requests_session(retries=5, backoff_factor=0.5, status_forcelist=(500, 502, 504)):
    session = requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    session.headers.update({'Accept-Encoding': 'gzip, deflate'})  # Enable compression for faster downloads
    return session

# Get the user's choices for asset types
def get_user_options(asset_metadata):
    # Extract unique asset categories from metadata
    asset_categories = list(set(asset_type for asset_type in asset_metadata['facets']['type']))

    # Ask the user for their preferred asset categories
    print("\nAvailable Asset Categories:")
    for i, category in enumerate(asset_categories, 1):
        print(f"{i}. {category}")
    
    asset_type_choice = input(f"Select asset categories (comma-delimited, e.g., 1,2): ")
    selected_asset_types = [asset_categories[int(choice.strip()) - 1] for choice in asset_type_choice.split(",") if choice.strip().isdigit()]

    return selected_asset_types

def save_asset_metadata(asset_metadata, asset_path):
    with open(asset_path / "asset_metadata.json", "w", encoding="utf-8") as f:
        json.dump(asset_metadata, f, ensure_ascii=False, indent=4)

def save_checksums(checksums, asset_path):
    with open(asset_path / "checksums.json", "w", encoding="utf-8") as f:
        json.dump(checksums, f, ensure_ascii=False, indent=4)

def extract_token(token):
    if token.startswith('token:"'):  # Copying from Firefox dev tools, remove extra JSON data
        token = token.removeprefix('token:"')
        token = token.removesuffix('"')
    elif token.startswith('{"token":"'):  # Copying from Chrome dev tools, remove extra JSON data
        token = token.split('":"')[1].split('","')[0]
    return token

# Function to download the asset from Quixel
def download_quixel_asset(session, asset, asset_path, download_id):
    while True:
        try:
            url = f"https://assetdownloads.quixel.com/download/{download_id}?preserveStructure=true&url=https://quixel.com/v1/downloads"
            response = session.get(url, stream=True)

            if response.status_code != 200:
                print(f"\nFailed to download asset {asset}, status code: {response.status_code}")
                print(f"Retrying in 5 seconds...")
                time.sleep(5)
                continue  # Retry the download
            
            # Get the file size from the headers
            total_size = int(response.headers.get('content-length', 0))
            asset_zip_path = asset_path / f"{asset}.zip"
            
            # Write to the file in chunks
            with open(asset_zip_path, "wb") as f:
                print(f"\nDownloading {asset}...")
                progress_bar = tqdm(desc=f"Downloading {asset}", total=total_size, unit='B', unit_scale=True)

                for chunk in response.iter_content(1024 * 1024):  # Write in 1 MB chunks
                    if chunk:
                        f.write(chunk)
                        progress_bar.update(len(chunk))

                progress_bar.close()

            print(f"Download completed for asset {asset}.")
            break  # Break the loop when the download succeeds

        except Exception as e:
            print(f"Error while downloading asset {asset}: {e}")
            print("Retrying in 5 seconds...")
            time.sleep(5)

# Function to request asset from Quixel
def request_quixel_asset(session, token, asset, asset_components, asset_path, asset_type):
    while True:
        headers = {"Authorization": token}

        # Request the asset
        data = {
            "asset": asset,
            "config": {
                "highpoly": True,  # Request high-poly mesh if available
                "assetTypes": [asset_type],  # User-selected asset types
            }
        }

        response = session.post("https://quixel.com/v1/downloads", headers=headers, json=data)

        if response.status_code != 200:
            try:
                json_response = response.json()
                print(f"\nEncountered error {response.status_code}! Here is the response from the Quixel server: {json_response}")

                if "code" in json_response:
                    if json_response["code"] == "ASSET_DOES_NOT_EXIST":
                        print(f"\nRequested asset {asset} does not exist! Skipping.")
                        return token, False
                if "message" in json_response:
                    if json_response["message"] == "Expired token":
                        token = extract_token(input("Your Quixel token has expired! Please input a refreshed token: "))
            except json.JSONDecodeError:
                print(f"\nError on decode with code {response.status_code}! Here is the response: {response}")

        else:
            try:
                json_response = response.json()
                download_id = json_response["id"]
                download_quixel_asset(session, asset, asset_path, download_id)

                return token, True
            except json.JSONDecodeError:
                print(f"Error on decode! Here is the response: {response}")

# Calculate SHA256 checksum for a file
def calculate_checksum(asset, asset_path):
    asset_zip_path = asset_path / f"{asset}.zip"
    sha256_hash = hashlib.sha256()
    with open(asset_zip_path, "rb") as f:
        # Read and update hash in chunks of 4K
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def download_asset(session, asset_id, asset_metadata, asset_path, checksums, token, asset_type):
    asset_data = asset_metadata["asset_metadata"][asset_id]
    asset_type_from_metadata = asset_data["full_metadata"]["semanticTags"]["asset_type"]

    # Only download the selected asset types
    if asset_type != asset_type_from_metadata:
        return

    # Create subfolder for the asset type if it doesn't exist
    category_path = asset_path / asset_type
    category_path.mkdir(parents=True, exist_ok=True)

    # Get asset components
    if "components" in asset_data["full_metadata"]:  # Find all components for this asset
        type_list = list(set([component["type"] for component in asset_data["full_metadata"]["components"]]))
    else:
        type_list = list(set([component["type"] for component in asset_data["full_metadata"]["maps"]]))
    type_list.sort()
    asset_components = [{"type": image_map, "mimeType": "image/x-exr"} for image_map in type_list]

    # Download asset and save checksum
    token, asset_result = request_quixel_asset(session, token, asset_id, asset_components, category_path, asset_type)
    if asset_result:
        checksum = calculate_checksum(asset_id, category_path)
        checksums[asset_id] = checksum
        save_checksums(checksums, asset_path)

def download_all_assets(asset_metadata, asset_path, checksums, num_threads):
    # Get user choices for asset categories
    selected_asset_types = get_user_options(asset_metadata)

    token = extract_token(input("Enter your Quixel token (refer to the readme for instructions): "))
    session = get_requests_session()  # Create a session with retry support

    temp_assets_to_download = list(set(checksums.keys()) ^ set(asset_metadata["asset_metadata"].keys()))

    # Filter assets based on the selected categories
    filtered_assets_to_download = [asset_id for asset_id in temp_assets_to_download
                                   if asset_metadata["asset_metadata"][asset_id]["full_metadata"]["semanticTags"]["asset_type"] in selected_asset_types]

    print(f"\n{len(filtered_assets_to_download)} assets in the selected categories.")
    print(f"{len(checksums)} total assets downloaded.")
    print(f"{len(filtered_assets_to_download)} assets not yet downloaded in the selected categories.")

    print(f"\n{len(filtered_assets_to_download)} assets to download.")
    print("Do NOT quit the program between downloads, as this is likely to destroy your checksum file while the .zip checksum is being saved. It is safe to quit while a file is being downloaded. When you restart the program, it will resume where it left off.")

    # Thread pool for concurrent downloads
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(download_asset, session, asset_id, asset_metadata, asset_path, checksums, token, asset_type)
                   for asset_id in filtered_assets_to_download for asset_type in selected_asset_types]
        
        for future in tqdm(as_completed(futures), total=len(futures), desc="Overall Progress"):
            future.result()  # This will raise any exceptions that occurred during download

    print(f"\nFinished downloading {len(filtered_assets_to_download)} assets!")

# Main setup
asset_path = Path(input("Enter the FULL path of the folder you want to download assets to: "))
asset_metadata = None

try:
    with open(asset_path / "asset_metadata.json", "r", encoding="utf-8") as f:
        asset_metadata = json.load(f)
except FileNotFoundError:
    print(f"\n\nCouldn't find asset_metadata.json in the directory you selected, {asset_path}")
    print("\nFor a proper archive, this program utilizes an asset_metadata.json file in the same directory as the assets to store SHA256 hashes for each .zip file when downloading is finished.")
    print(f"\nSo, to run this program, simply copy your COMPLETE (basic metadata will not work!) asset_metadata.json file to {asset_path}\n")
    input("Press Enter to exit...")

if asset_metadata:
    try:
        with open(asset_path / "checksums.json", "r", encoding="utf-8") as f:
            checksums = json.load(f)
    except FileNotFoundError:
        checksums = {}

    # Ask the user how many threads to run
    num_threads = int(input("Enter the number of threads to use for concurrent downloads (e.g., 5): "))
    download_all_assets(asset_metadata, asset_path, checksums, num_threads)
