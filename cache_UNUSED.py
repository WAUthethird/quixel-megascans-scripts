import requests
import json
from urllib.parse import urlencode

# Illustrates how to call the user-facing API -- this isn't necessary since I just use the developer API which works for regular user tokens.

def call_cache_api():
    params = {
        "page": 0,
        "maxValuesPerFacet": 1000,
        "hitsPerPage": 1000,
        "attributesToRetrieve": ",".join(["id",
                                          "previews.relativeSize",
                                          "previews.scaleReferences",
                                          "previews.images.thumb",
                                          "previews.images.thumbRetina",
                                          "previews.images.thumbRetinaJpg",
                                          "previews.images.aspectRatio",
                                          "previews.images.preview",
                                          "previews.images.thumbJpg",
                                          "created",
                                          "points",
                                          "subCategory",
                                          "category",
                                          "type",
                                          "name",
                                          "descriptive",
                                          "theme",
                                          "contains",
                                          "approvedAt",
                                          "revised"])
    }

    data = {
        "url": "https://6UJ1I5A072-2.algolianet.com/1/indexes/assets/query?x-algolia-application-id=6UJ1I5A072&x-algolia-api-key=e93907f4f65fb1d9f813957bdc344892",
        "params": urlencode(params)
    }

    response = requests.post(
        "https://proxy-algolia-prod.quixel.com/algolia/cache",
        headers={
            "x-api-key": "KEY-GOES-HERE",
            "Origin": "https://quixel.com",
        },
        json=data
    )

    return json.dumps(response.json())

# Example usage
result = call_cache_api()
print(result)
