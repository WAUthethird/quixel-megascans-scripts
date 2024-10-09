import requests
import json
import copy
import time
import random
from tqdm import tqdm


# This script should be run after get_all_basic_asset_metadata.py. It requires an instantiated asset_metadata.json file with all asset IDs - however, it does not require complete asset metadata.
# If you want to download assets, make sure you run this script BEFORE running download_all_assets.py! Quixel refuses download requests for any unowned assets.


def extract_token(token):
    if token.startswith("token:\""): # Copying from Firefox dev tools, remove extra json data
        token = token.removeprefix("token:\"")
        token = token.removesuffix("\"")
    elif token.startswith("{\"token\":\""): # Copying from Chrome dev tools, remove extra json data
        token = token.split("\":\"")[1].split("\",\"")[0]

    return token


def check_already_claimed(token):
    while True:
        headers = {"Authorization": token}

        response = requests.get("https://quixel.com/v1/assets/acquired", headers=headers)

        if response.status_code != 200:
            try:
                json_response = response.json()
                print(f"\nEncountered error {response.status_code}! Here is the response from the Quixel server: {json_response}")
            except json.JSONDecodeError:
                print(f"\nEncountered error! (Recieved status code {response.status_code} from Quixel server)")
            print("Waiting 5 seconds and retrying.")
            time.sleep(5)
        else:
            try:
                json_response = response.json()

                return [asset["assetID"] for asset in json_response]
            except json.JSONDecodeError:
                print(f"Error on decode! Here is the response: {response}")
                print("Waiting 5 seconds and retrying.")
                time.sleep(5)


def claim_quixel_asset(token, asset):
    while True:
        headers = {"Authorization": token}

        response = requests.post("https://quixel.com/v1/acl", headers=headers, json={"assetID": asset})

        if response.status_code != 200:
            try:
                json_response = response.json()
                print(f"\nEncountered error {response.status_code} with asset {asset}! Here is the response from the Quixel server: {json_response}")
            except json.JSONDecodeError:
                print(f"\nEncountered error! (Recieved status code {response.status_code} from Quixel server)")
            print("Waiting 5 seconds and retrying.")
            time.sleep(5)
        else:
            try:
                json_response = response.json()

                if "code" in json_response:
                    if json_response["code"] == "USER_ALREADY_OWNS_ASSET": # This is just here as a sanity check since we're already skipping claimed assets
                        print(f"Requested asset {asset} is already claimed! Skipping.")
                        break
                    elif json_response["code"] == "ASSET_DOES_NOT_EXIST": # I think this is the right code, but I already have all assets and am unable to check. Hopefully this catches everything.
                        print(f"Requested asset {asset} does not exist! Skipping. (you will continue to recieve this message on each run as long as the asset's metadata is still present, use remove_asset_from_metadata.py to remove it)")
                        break
                    elif json_response["isError"]: # This might happen if the token invalidates midway, but it's not super difficult to just restart the script to resume.
                        print(f"The server accepted the request, but returned an error. Here is the response: {json_response}")
                        print("Waiting 5 seconds and retrying.")
                        time.sleep(5)
                else:
                    # Success!
                    break
            except json.JSONDecodeError:
                print(f"Error on decode! Here is the response: {response}")
                print("Waiting 5 seconds and retrying.")
                time.sleep(5)


def claim_all_assets(asset_metadata):
    token = extract_token(input("Enter your Quixel token (refer to the readme for instructions): "))

    print(f"\n{asset_metadata["total"]} total assets in asset metadata.")
    print("Checking currently claimed assets via Quixel servers...")
    claimed = check_already_claimed(token)

    print(f"\nDetected {len(claimed)} currently claimed assets.")

    TEMP_unclaimed_asset_list = copy.deepcopy(list(asset_metadata["asset_metadata"].keys())) # It's my experience that Python is prone to doing strange things with object references, so this is just another sanity check
    unclaimed_asset_list = list(set(claimed) ^ set(TEMP_unclaimed_asset_list)) # Perform the opposite of a list intersection

    print(f"\n{len(unclaimed_asset_list)} assets to claim.")
    print("There is an artificial, random delay of between 0.1 and 1 second between each request to reduce load on the Quixel servers, so expect to wait several hours.")
    print("If the script breaks for some reason, no worries - restart it and it will resume right where it left off!\n")

    for asset_id in tqdm(unclaimed_asset_list):
        claim_quixel_asset(token, asset_id)
        time.sleep(round(random.uniform(0.1, 1), 2))

    print(f"\nFinished claiming {len(unclaimed_asset_list)} assets!")
    print("Checking currently claimed assets via Quixel servers...")

    claimed = check_already_claimed(token)

    if len(claimed) == asset_metadata["total"]:
        print(f"\nAll {asset_metadata["total"]} assets claimed successfully!")
    else: # This really shouldn't be possible, but again, sanity check
        print(f"\nCould not verify that all {asset_metadata["total"]} assets have been claimed! Try running this script one more time.")


print("Loading asset_metadata.json! Depending on if you ran get_all_complete_asset_metadata.py before this, this could take a bit.\n")


asset_metadata = None

try:
    with open("asset_metadata.json", "r", encoding="utf-8") as f:
        asset_metadata = json.load(f)
except FileNotFoundError:
    print("Couldn't find asset_metadata.json! Have you run get_all_basic_asset_metadata.py yet?\n")
    input("Press Enter to exit...")

if asset_metadata:
    claim_all_assets(asset_metadata)