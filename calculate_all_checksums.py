import json
import hashlib
import zipfile
from pathlib import Path
from tqdm import tqdm


# A simple script to mass-calculate the checksum of every asset currently downloaded and save it to checksums.json.


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
    

asset_path = Path(input("Enter the FULL path of the folder with your assets: "))

zip_names = sorted([zip.name.split(".zip")[0] for zip in asset_path.glob('*.zip')])

print(f"\n{len(zip_names)} zips in directory selected. Saving checksums to checksums.json.")

checksums = {}

with open(asset_path / "checksums.json", "w", encoding="utf-8") as c:
    for asset in tqdm(zip_names):
        if test_zip_file(asset, asset_path):
            checksums[asset] = calculate_checksum(asset, asset_path)
        else:
            print(f"Zip for {asset} was bad! Skipping checksum calculation.")
    
    print("\nChecksum calculation done! Saving...")

    json.dump(checksums, c, ensure_ascii=False, indent=4)