# Megascans Asset Payload JSON Schema Spec


```
v1.1.8
Last updated: 24 June 2016
Authored by: Kamil Waheed <kamil@quixel.se>
(c) 2016 Quixel AB
Proprietary license
```

## Abstract
This document describes:

  - Some information regarding the packaging of Megascans asset payload JSON files.
  - The JSON schema to be used for storing Megascans asset payload representations.

## Packaging information:
  - Each Megascans asset has an accompanying payload JSON file.
  - The payload JSON files hold __the entire dataset (metadata)__ associated with their corresponding assets.
  - The location of the JSON files with respect to the rest of the asset files MUST be the same.
  - The asset uploader script must respect all the asset payload JSON files: parse, validate and post/put to the API endpoints.


## Annotated JSON Sample:

##### ID

```javascript
"id": "54b385169bc330"
```

The universally unique ID for the asset. 

##### Categories

```javascript
"categories": [
  "surface_scans",
  "soil",
  "dirt"
]
```

The entire ancestry chain that the asset belongs to; the last one being the direct parent. In the example above:
  - _surface_scans_: The top-level category
  - _soil_: The main level category
  - _dirt_: The sub-level category

The chain can theoretically be infinitely long.

Each category must be a `String`.


##### Name
```javascript
"name": "Branch debris tree (small & mixed)"
```

Name of the asset.



##### Search Tags

```javascript
"tags": [
  "dirty",
  "dry",
  "brown",
  "coarse",
  "footsteps",
  "stones"
]
```

The list of search tags for the asset. All search tags must be in lowercase. Acceptable characters are:

- alphanumeric characters
- hyphen (to separate words)

If a tag is comprised of more than one word, it MUST be separated with a hyphen (-).

For presentation purposes, all tags can be capitalized. For tags comprised of more than one word, hyphens (-) can be replaced by a non-breaking space and each word can be capitalized.

e.g.
`dirty` becomes `Dirty`
`two-sided` becomes `Two Sided`

The order is insignificant.

Each tag must be a `String`.



##### Environment Tags

```javascript
"environment": {
  "region": "pakistan",
  "biome": "semiarid-desert"
}
```

Environment information of the asset.

  - `region:String`: Geographic scan region of the asset, e.g., `australia`, `pakistan`, `sweden`, `u.s.`, etc.
  - `biome:String`: Flora and fauna community scan habitat of the asset, e.g., `mediterranean-forest`, `semiarid-desert`, `savanna-grassland`, etc.

Acceptable characters are:

  - alphanumeric characters
  - hyphen (to separate words)

If an environment tag is comprised of more than one word, it MUST be separated with a hyphen (-).

For presentation purposes, all environment tags can be capitalized. For environment tags comprised of more than one word, hyphens (-) can be replaced by a non-breaking space and each word can be capitalized.

Each environment tag must be a `String`.



##### Average Color
```javascript
"averageColor": "#123456"
```
The average color of the asset. Must be a valid hex color code as a `String`.

The frontend implementation may use this value to filter/sort the assets.

This value may also be used by the frontend client as a placeholder color while it is loading a preview image to show for the asset.



##### Preview Files
```javascript
"previews": {
  "images": [
    {
      "resolution": "320x320",
      "uri": "preview.jpg"
    },
    {
      "resolution": "800x800",
      "uri": "preview.jpg"
    }
  ],
  "relativeSize": "1x1",
  "scaleReferences": [ "scale.jpg" ]
}
```
URIs to the asset previews.

  - `images`: A list of preview images.
    - `resolution: String`: A `width`x`height` formatted resolution string where both `width` and `height` are integers.
    - `uri: String`: URI to the preview image.
  - `relativeSize:String`: An `xScale`x`yScale` formatted size scale for preview images useful for depicting the relative physical size of an asset when shown next to other assets (for example in a grid).
  - `scaleReferences:String`: A list of scale-reference images.


##### Properties

```javascript
"properties": [
  {
    "key": "orientation",
    "value": "wall"
  },
  {
    "key": "target",
    "value": "offline"
  },
  {
    "key": "layout",
    "value": "variations"
  },
  {
    "key": "size",
    "value": "tiny"
  },
  {
    "key": "color",
    "value": "brown"
  },
  {
    "key": "age",
    "value": "baby"
  }
]
```

A list of properties for the asset. Properties can be used for filtering assets.


##### Metadata
```javascript
"meta": [
  {
    "name": "Scan Area",
    "key": "scanArea",
    "value": "2x2 m"
  },
  {
    "name": "Tileable",
    "key": "tileable",
    "value": true
  },
  {
    "name": "Texel Density",
    "key": "texelDensity",
    "value": "4096 px/m"
  },
  {
    "name": "Illuminant",
    "key": "illuminant",
    "value": "D65"
  },
  {
    "name": "Calibration",
    "key": "calibration",
    "value": "Macbeth"
  },
  {
    "name": "Height",
    "key": "height",
    "value": "2cm"
  },
  {
    "name": "Scanner",
    "key": "scanner",
    "value": "QMS-PM Mkl"
  }
]
```

A list of metadata that the frontend client can display to the user where each item is an object with:
  
  - `name: String`: The human-readable name of the metadata property.
  - `key: String`: The metadata property identifier.
  - `value: String|Number|Boolean`: The value of the metadata property.


##### References
```javascript
"references": [
  "http://images.google.com/young-eucalyptus-2004-01-01.jpg"
]
```

A list of reference images for the asset. Useful for visually communicating the context of an asset, like a picture of a plant that a leaf asset belongs to.


##### Brush Files
```javascript
"brushes": [
  {
    "uri": "/quixel-megascans-assets/asset-pbbaz/pbbaz_Brush_2.tif"
  }
]
```

A list of brush files for the asset.

  - `uri: String`: URI to the brush file.

##### Mesh Files
```javascript
"meshes": [
  {
    "type": "zbrush",
    "uris": [
      {
        "mimeType": "application/x-ztl",
        "uri": "Debris_Tree_Small_Mixed_Branch_pdEuS.ztl"
      }
    ]
  },
  {
    "type": "original",
    "uris": [
      {
        "mimeType": "application/x-obj",
        "uri": "Debris_Tree_Small_Mixed_Branch_pdEuS-orig.obj"
      },
      {
        "mimeType": "application/x-fbx",
        "uri": "Debris_Tree_Small_Mixed_Branch_pdEuS-orig.fbx"
      }
    ]
  },
  {
    "type": "lod",
    "tris": 17350,
    "uris": [
      {
        "mimeType": "application/x-obj",
        "uri": "Debris_Tree_Small_Mixed_Branch_pdEuS-lod0.obj"
      },
      {
        "mimeType": "application/x-fbx",
        "uri": "Debris_Tree_Small_Mixed_Branch_pdEuS-lod0.fbx"
      }
    ]
  }
]
```

A list of mesh files for the asset. This is useful for when the asset is an object scan.

  - `type: String`: Type of mesh (possible values: *1.* `original` for high-poly meshes, *2.* `lod` for meshes at a specific LOD, and *3.* `zbrush` for ZBrush specific high-poly mesh data).
  - `tris: Number`: Number of triangles for when `type` is `lod`.
  - `uris: Array`: List of URIs.
    - `mimeType: String`: [Mime-type](http://en.wikipedia.org/wiki/Internet_media_type) for the mesh file. (*application/x-obj* for .obj files, *application/x-fbx* for .fbx files and *application/x-ztl* for .ztl files)
    - `uri: String`: URI to the mesh file.

##### Components
```javascript
"components": [
  ...
]
```

A list of components for the asset.

###### Component Properties
```javascript
"components": [
  {
    "type": "albedo",
    "name": "Albedo",
    "minIntensity": 50,
    "maxIntensity": 240,
    "averageColor": "#6F5E4E",
    "colorSpace": "sRGB",
    ...
  }
]
```

  - `type: String`: The type identifier of the component.
  - `name: String`: The human-readable name of the component.
  - `minIntensity: Number`: Coupled with `maxIntensity`, intensity range of the component. This must be a value between 0 and 255.
  - `maxIntensity: Number`: Coupled with `minIntensity`, intensity range of the component. This must be a value between 0 and 255.
  - `averageColor: String`: Average color of the component. This value may be used by the frontend client for the visual representation of the component. This must be a hex color code.
  - `colorSpace: String`: The color space of the component like `sRGB`, `Linear`, etc. Value must be human-readable.


###### Component URIs
```javascript
"components": [
  {
    ...
    "uris": [
      {
        "physicalSize": "40x40",
        "resolutions": [
          {
            "resolution": "2048x2048",
            "formats": [
              {
                "mimeType": "image/jpeg",
                "bitDepth": 8,
                "uri": "Scrap_Coal_39bfc763fb452_Albedo.jpg"
              },
              {
                "mimeType": "image/png",
                "bitDepth": 16,
                "uri": "Scrap_Coal_39bfc763fb452_Albedo.png"
              },
              {
                "mimeType": "image/x-exr",
                "bitDepth": 32,
                "uri": "Scrap_Coal_39bfc763fb452_Albedo.exr"
              }
            ]
          }
        ]
      }
    ]
    ...
  }
]
```

A list having objects with:

  - `physicalSize: String`: A `width`x`height` formatted physical size string of the asset component where both `width` and `height` are decimeter integers.
  - `resolutions`: List of digital resolutions available for the specific physical size.
    - `resolution: String`: A `width`x`height` formatted resolution string where both `width` and `height` are integers.
    - `formats`: List of file formats available for the specific physical size and resolution pair.
      - `mimeType: String`: [Mime-type](http://en.wikipedia.org/wiki/Internet_media_type) for the asset component file.
      - `bitDepth: Number`: Bit-depth of the asset component file.
      - `uri: String`: URI to the asset component file.

---

## Full JSON sample:

```javascript
{
  "id": "54b385169bc330",
  "categories": [
    "surface_scans",
    "soil",
    "dirt"
  ],
  "name": "Branch debris tree (small & mixed)",
  "tags": [
    "dirty",
    "dry",
    "brown",
    "coarse",
    "footsteps",
    "stones"
  ],

  "environment": {
    "region": "pakistan",
    "biome": "semiarid-desert"
  },

  "averageColor": "#123456",

  "previews": {
    "images": [
      {
        "resolution": "320x320",
        "uri": "preview.jpg"
      },
      {
        "resolution": "800x800",
        "uri": "preview.jpg"
      }
    ],
    "relativeSize": "1x1",
    "scaleReferences": [ "scale.jpg" ]
  },

  "properties": [
    {
      "key": "orientation",
      "value": "wall"
    },
    {
      "key": "target",
      "value": "offline"
    },
    {
      "key": "layout",
      "value": "variations"
    },
    {
      "key": "size",
      "value": "tiny"
    },
    {
      "key": "color",
      "value": "brown"
    },
    {
      "key": "age",
      "value": "baby"
    }
  ],

  "meta": [
    {
      "name": "Scan Area",
      "key": "scanArea",
      "value": "2x2 m"
    },
    {
      "name": "Tileable",
      "key": "tileable",
      "value": true
    },
    {
      "name": "Texel Density",
      "key": "texelDensity",
      "value": "4096 px/m"
    },
    {
      "name": "Illuminant",
      "key": "illuminant",
      "value": "D65"
    },
    {
      "name": "Calibration",
      "key": "calibration",
      "value": "Macbeth"
    },
    {
      "name": "Height",
      "key": "height",
      "value": "2cm"
    },
    {
      "name": "Scanner",
      "key": "scanner",
      "value": "QMS-PM Mkl"
    }
  ],

  "references": [
    "http://images.google.com/young-eucalyptus-2004-01-01.jpg"
  ],
  
  "brushes": [
    {
      "uri": "/quixel-megascans-assets/asset-pbbaz/pbbaz_Brush_2.tif"
    }
  ],

  "meshes": [
    {
      "type": "zbrush",
      "uris": [
        {
          "mimeType": "application/x-ztl",
          "uri": "Debris_Tree_Small_Mixed_Branch_pdEuS.ztl"
        }
      ]
    },
    {
      "type": "original",
      "uris": [
        {
          "mimeType": "application/x-obj",
          "uri": "Debris_Tree_Small_Mixed_Branch_pdEuS-orig.obj"
        },
        {
          "mimeType": "application/x-fbx",
          "uri": "Debris_Tree_Small_Mixed_Branch_pdEuS-orig.fbx"
        }
      ]
    },
    {
      "type": "lod",
      "tris": 17350,
      "uris": [
        {
          "mimeType": "application/x-obj",
          "uri": "Debris_Tree_Small_Mixed_Branch_pdEuS-lod0.obj"
        },
        {
          "mimeType": "application/x-fbx",
          "uri": "Debris_Tree_Small_Mixed_Branch_pdEuS-lod0.fbx"
        }
      ]
    },
    {
      "type": "lod",
      "tris": 11253,
      "uris": [
        {
          "mimeType": "application/x-obj",
          "uri": "Debris_Tree_Small_Mixed_Branch_pdEuS-lod1.obj"
        },
        {
          "mimeType": "application/x-fbx",
          "uri": "Debris_Tree_Small_Mixed_Branch_pdEuS-lod1.fbx"
        }
      ]
    },
    {
      "type": "lod",
      "tris": 5670,
      "uris": [
        {
          "mimeType": "application/x-obj",
          "uri": "Debris_Tree_Small_Mixed_Branch_pdEuS-lod2.obj"
        },
        {
          "mimeType": "application/x-fbx",
          "uri": "Debris_Tree_Small_Mixed_Branch_pdEuS-lod2.fbx"
        }
      ]
    },
    {
      "type": "lod",
      "tris": 1154,
      "uris": [
        {
          "mimeType": "application/x-obj",
          "uri": "Debris_Tree_Small_Mixed_Branch_pdEuS-lod3.obj"
        },
        {
          "mimeType": "application/x-fbx",
          "uri": "Debris_Tree_Small_Mixed_Branch_pdEuS-lod3.fbx"
        }
      ]
    },
    {
      "type": "lod",
      "tris": 680,
      "uris": [
        {
          "mimeType": "application/x-obj",
          "uri": "Debris_Tree_Small_Mixed_Branch_pdEuS-lod4.obj"
        },
        {
          "mimeType": "application/x-fbx",
          "uri": "Debris_Tree_Small_Mixed_Branch_pdEuS-lod4.fbx"
        }
      ]
    },
    {
      "type": "lod",
      "tris": 320,
      "uris": [
        {
          "mimeType": "application/x-obj",
          "uri": "Debris_Tree_Small_Mixed_Branch_pdEuS-lod4.obj"
        },
        {
          "mimeType": "application/x-fbx",
          "uri": "Debris_Tree_Small_Mixed_Branch_pdEuS-lod4.fbx"
        }
      ]
    }
  ],

  "components": [
    {
      "type": "albedo",
      "name": "Albedo",
      "minIntensity": 50,
      "maxIntensity": 240,
      "averageColor": "#6F5E4E",
      "colorSpace": "sRGB",
      "uris": [
        {
          "physicalSize": "40x40",
          "resolutions": [
            {
              "resolution": "2048x2048",
              "formats": [
                {
                  "mimeType": "image/jpeg",
                  "bitDepth": 8,
                  "uri": "Scrap_Coal_39bfc763fb452_Albedo.jpg"
                },
                {
                  "mimeType": "image/png",
                  "bitDepth": 16,
                  "uri": "Scrap_Coal_39bfc763fb452_Albedo.png"
                },
                {
                  "mimeType": "image/x-exr",
                  "bitDepth": 32,
                  "uri": "Scrap_Coal_39bfc763fb452_Albedo.exr"
                }
              ]
            },
            {
              "resolution": "4096x4096",
              "formats": [
                {
                  "mimeType": "image/jpeg",
                  "bitDepth": 8,
                  "uri": "Scrap_Coal_39bfc763fb454_Albedo.jpg"
                },
                {
                  "mimeType": "image/png",
                  "bitDepth": 16,
                  "uri": "Scrap_Coal_39bfc763fb454_Albedo.png"
                },
                {
                  "mimeType": "image/x-exr",
                  "bitDepth": 32,
                  "uri": "Scrap_Coal_39bfc763fb454_Albedo.exr"
                }
              ]
            },
            {
              "resolution": "8192x8192",
              "formats": [
                {
                  "mimeType": "image/jpeg",
                  "bitDepth": 8,
                  "uri": "Scrap_Coal_39bfc763fb458_Albedo.jpg"
                },
                {
                  "mimeType": "image/png",
                  "bitDepth": 16,
                  "uri": "Scrap_Coal_39bfc763fb458_Albedo.png"
                },
                {
                  "mimeType": "image/x-exr",
                  "bitDepth": 32,
                  "uri": "Scrap_Coal_39bfc763fb458_Albedo.exr"
                }
              ]
            }
          ]
        }
      ]
    }
  ]
}
```

---


## Changelog

  - __1.1.8__ - 24/6/2016
    - Added `brushes`
  - __1.1.7__ - 15/6/2016
    - Added `relativeSize` under `preview`
    - Renamed `scale` for scale-reference images to `scaleReferences` under the `preview`
  - __1.1.6__ - 11/5/2016
    - Added the references field.
  - __1.1.5__ - 2/3/2016
    - Added the scale-reference preview image field.
  - __1.1.4__ - 5/2/2016
    - Changed `_id` to `id`
  - __1.1.3__ - 3/2/2016
    - Updated the packaging information to reflect that the JSON files must reside in the same directory as the asset files.
  - __1.1.2__ - 3/2/2016
    - Added `minIntensity` and `maxIntensity` for asset components.
    - Added "Height" meta data to example meta data fields.
    - Changed example uri fields to only include file names.
  - __1.1.1__ - 3/2/2016
    - Added the `properties` field
  - __1.1.0__ - 1/2/2016
    - Added acceptable characters for `tags` and hints for presentation.
    - Added the `environment` field.
    - Removed the `related` field.
    - Removed the `filterProps` field.
    - Removed the `unity` and `unity-internal` fields from under `previews`
  - __1.0.5__ - 28/9/2015
    - Adding the missing `name` field.
  - __1.0.4__ - 11/8/2015
    - Removed the no-longer-necessary `accessTags` field.
    - Updated the `mesh` field according to the new structure.
    – Got rid of the JSON Schema. We never needed that anyways.
  - __1.0.3__ - 20/1/2015
    - Added _id field
    - Added related field
    - Fixed jpeg mime-type in the sample JSON
  - __1.0.2__ - 26/12/2014
    - Removed modifierProps from asset components
  - __1.0.1__ - 26/12/2014
    - Added access tags
  - __1.0.0__ - 23/12/2014
    - Initial Commit
