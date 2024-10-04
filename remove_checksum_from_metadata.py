import json
from pathlib import Path


# If a downloaded asset somehow got past all the checks I put in place to ensure it was complete and turned out to be incomplete, this last-ditch script will remove the calculated checksum of an asset from an asset_metadata.json file so that it can be redownloaded.
# This is just a temporary script while I figure this issue out. Ideally this script should not be necessary whatsoever.


def save_asset_metadata(asset_metadata, asset_path):
    with open(asset_path / "asset_metadata.json", "w", encoding="utf-8") as f:
        json.dump(asset_metadata, f, ensure_ascii=False, indent=4)


def remove_checksum(asset_metadata, asset_path):
    asset = input('\nEnter the ID of the asset you want to delete the checksum for: ')

    del asset_metadata["asset_metadata"][asset]["sha256"]

    save_asset_metadata(asset_metadata, asset_path)

    print('\nChecksum deleted and metadata saved!')


asset_path = Path(input("Enter the FULL path of the folder your assets are in: "))
asset_metadata = None

try:
    with open(asset_path / "asset_metadata.json", "r", encoding="utf-8") as f:
        asset_metadata = json.load(f)
except FileNotFoundError:
    print(f"\n\nCouldn't find asset_metadata.json in the directory you selected, {asset_path}")
    input("Press Enter to exit...")

if asset_metadata:
    remove_checksum(asset_metadata, asset_path)