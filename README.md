# Quixel Megascans Scripts
A collection of Python scripts to facilitate claiming and downloading the *entire* [Quixel Megascans](https://quixel.com/) collection before it becomes [fully paid in 2025](https://www.unrealengine.com/en-US/blog/fab-content-marketplace-launches-in-october-publishing-portal-opens-today).

# Update: December 1st, 2024
[Fab](https://www.fab.com), Epic's single replacement for a number of their asset marketplaces and libraries (including Quixel) is available. All Quixel assets may be claimed in a single click [here](https://www.fab.com/megascans-free). Make sure to do it before the end of the year! You can also claim all legacy Quixel assets on Quixel.com before the end of the year, which I also recommend doing as I do not have a download script for Fab available at this time. This is because Fab has an absolutely atrocious method of downloading Quixel assets compared to Quixel.com, and I simply do not want to deal with it until an official API has been released, at the very least.

## Requirements
- **Python 3.12 or higher** (3.11 and prior do not work!)
- **requests** (pip)
- **tqdm** (pip)

## Getting your Quixel Token
### Firefox
The most reliable and easy way to get your Quixel token in Firefox I've found:
1. Go to [https://quixel.com/](https://quixel.com/) and log in.
2. Press **Ctrl+Shift+I** to open the Web Developer Tools.
3. Click on the Storage tab.
4. Open the Cookies dropdown in the left sidebar, and select the https://quixel.com option.
5. Click on the `auth` cookie in the main window.
6. Right-click and copy the `token` (not `refreshToken`) in the Parsed Value section in the right sidebar.
7. You're done! Any script that uses a token will parse the string you copied correctly, so don't worry if there is extra formatting. If you put the token in without any formatting, that should work as well.

### Chrome
Similar to the Firefox instructions:
1. Go to [https://quixel.com/](https://quixel.com/) and log in.
2. Press **Ctrl+Shift+I** to open the Developer Tools.
3. Click on the Application tab. If you don't see it, click the "More tabs" button next to the list of tabs and select it from there.
4. Open the Cookies dropdown in the left sidebar, and select the https://quixel.com option.
5. Click on the `auth` cookie in the main window.
6. Click "Show URL-decoded" on the bottom pane and copy the entire Cookie Value, refresh token and all.
7. You're done! Any script that uses a token will parse the string you copied correctly, so don't worry if there is extra formatting. If you put the token in without any formatting, that should work as well.

## Instructions
### Metadata Creation
Each script (except [get_all_basic_asset_metadata.py](get_all_basic_asset_metadata.py)) requires a file called `asset_metadata.json` to be present alongside them.

This file is initially created using [get_all_basic_asset_metadata.py](get_all_basic_asset_metadata.py) with the basic, barebones metadata (name and asset ID) for each asset from Quixel.

Then, using [get_all_complete_asset_metadata.py](get_all_complete_asset_metadata.py), the *full* metadata for each asset is requested and saved to `asset_metadata.json` - when this process finishes, the file is about 1.5GB in size.

### Provided Metadata
For convenience, I've compressed the [*basic*](basic_asset_metadata.tar.zst) and [*complete*](complete_asset_metadata.tar.zst) stages of `asset_metadata.json` into separate .tar.zst files. Zstandard compression is pretty awesome, so I'm able to just provide these in the repository with zero compromises.

If you're on Windows, something like [7-Zip-zstd](https://github.com/mcmilk/7-Zip-zstd) should be able to decompress these.

### Claiming Assets
## This section is now irrelevant. You can claim all legacy assets and all Fab assets with one click (do it before January 1st!) on Quixel.com and Fab.com. The old instructions follow.
I'd wager most people who are here are most interested in mass-claiming all assets to their Quixel account. To do this, run [claim_all_assets.py](claim_all_assets.py) with either a [*basic*](basic_asset_metadata.tar.zst) or [*complete*](complete_asset_metadata.tar.zst) `asset_metadata.json` file present. There is no difference in functionality.

### Downloading Assets
If you want to download all Quixel assets, run [download_all_assets.py](download_all_assets.py) with a [*complete*](complete_asset_metadata.tar.zst) `asset_metadata.json` file in the directory you want to download assets to. It ***will not work*** with *basic* metadata.

## Future Features
- Full resume functionality for [get_all_basic_asset_metadata.py](get_all_basic_asset_metadata.py) and [get_all_complete_asset_metadata.py](get_all_complete_asset_metadata.py). This would also enable new assets to be added to the metadata if and when they appear.
- Switch from `tqdm` to `rich` to support things like a fancy spinner during checksum calculation and rich text.
- Better error handling across the board

## Why is there no initial commit history?
I initially developed these scripts in a private branch while I did silly things like committing my Quixel tokens to the branch. I also wanted to get these scripts in a decent enough state before releasing them, which did take a bit.

## Notice
Please note that these scripts have been developed with an emphasis on archival purposes, so scripts like [download_all_assets.py](download_all_assets.py) may not do what you want/expect at first. That script is straight and to the point - it downloads all assets to a single directory, and doesn't bother with things like asset categories. There is also (intentionally) *no* limit on retries.

## Removed Assets
A few assets have been removed from Quixel since I initially created these scripts. If you still have these assets in your `asset_metadata.json` file, you can use the [remove_asset_from_metadata.py](remove_asset_from_metadata.py) script to remove them. The latest versions of the [*basic*](basic_asset_metadata.tar.zst) and [*complete*](complete_asset_metadata.tar.zst) stages of `asset_metadata.json` do not have these assets. My thanks to @DR-Mello for getting me the IDs for the last 4 removed assets.

- `xgkmfcya`
- `wfgpebvaw`
- `we2rbizaw`
- `vktudjsaw`
- `vktffapaw`
