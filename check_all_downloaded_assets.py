import zipfile
from pathlib import Path
from tqdm import tqdm


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

print(f"\n{len(zip_names)} zips in directory selected. Checking.")

bad_assets = []

for asset in tqdm(zip_names):
    if not test_zip_file(asset, asset_path):
        print(f"{asset} is bad! Remove it from your checksum file.")
        bad_assets.append(asset)

if len(bad_assets) > 0:
    with open(asset_path / "bad_assets.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(bad_assets))
    print(f"\nList of bad assets saved to {asset_path / "bad_assets.txt"}")
else:
    print(f"\nNo bad assets detected!")