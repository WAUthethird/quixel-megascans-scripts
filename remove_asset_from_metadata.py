import json
from pathlib import Path


# Self explanatory. If you're having issues claiming or downloading an asset because it doesn't exist anymore, this script can help get rid of that error.


def save_asset_metadata(asset_metadata, asset_path):
    with open(asset_path / "asset_metadata.json", "w", encoding="utf-8") as f:
        json.dump(asset_metadata, f, ensure_ascii=False, indent=4)


def remove_asset_metadata(asset_metadata, asset_path):
    asset = input('\nEnter the ID of the asset you want to delete metadata for: ')

    del asset_metadata["asset_metadata"][asset]

    save_asset_metadata(asset_metadata, asset_path)

    print('\nAsset deleted and metadata saved!')


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