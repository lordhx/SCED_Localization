# SCED Localization

This repository contains the script for automatically generating localized [SCED mod](https://github.com/argonui/SCED).

## Dependencies

- The [Strange Eons](https://cgjennings.ca/eons/) program. You will want to install it together with the [Arkham Horror](https://discord.com/channels/225349059689447425/249270867522093056) and the [CSV Factory](http://se3docs.cgjennings.ca/um-proj-csv-factory.html) plugins.

- Python with some packages. Install the required packages with `pip install -r requirements.txt`.

## How it works

This script uses Strange Eons to create custom Arkham Horror cards using the [ArkhamDB card translation](https://github.com/Kamalisk/arkhamdb-json-data) together with the scanned card images in the mod.

The script is `main.py` in the root directory. You can run `python main.py --help` to get a list of command line options it takes. Most command line options have sensible defaults. The options are explained below:

- `--lang`

    This is the language you want to translate to. This list is restrained by what translation are available on ArkhamDB.

- `--se-executable`

    This is the path to the Strange Eons command line program. The default Windows installation gives the path `C:\Program Files\StrangeEons\bin\eons.exe`.

- `--se-preferences`

    This is the path to the Strange Eons preference file, which controls settings like font family, size and offset. The default Windows installation gives the path `C:\Users\lriuui0x0\AppData\Roaming\StrangeEons3\preferences`.

- `--filter`

    This is a Python expression string used to filter what cards will be translated. You can assume a variable named `card` will be available to use whose value is the data on ArkahmDB. For example `card['pack_code'] in ['core', 'rcore']` will filter for only cards in the Core and Revised Core Set.

- `--repo-dir`

    This is a directory to keep the intermediate repositories during processing. See the `--ahdb-dir`, `--mod-dir-primary` and `--mod-dir-secondary` below.

- `--cache-dir`

    This is a directory to keep the intermediate resources during processing. Explained in more details below.

- `--decks-dir`

    This is a directory to keep the translated and packed deck images. These images will be uploaded and their URLs will be referenced directly from the mod.

- `--ahdb-dir`

    This is the directory to the ArkhamDB json data repository. If you don't provide it, the script will clone the [Kamalisk/arkhamdb-json-data](https://github.com/Kamalisk/arkhamdb-json-data) repository into the repo directory. We use repository data instead of API to be more flexible on local changes.

- `--mod-dir-primary`, `--mod-dir-secondary`

    These are the directories to the local mod repositories. If you don't provide it, the script will clone the [argonui/SCED](https://github.com/argonui/SCED) and [Chr1Z93/loadable-objects](https://github.com/Chr1Z93/loadable-objects) repository into the repo directory.

- `--url-file`

    This is the file that keeps the mapping between original deck image URLs and the corresponding translated version. Explained in more details below.

- `--dropbox-token`

    The Dropbox access token for uploading deck images. Explained in more details below.

- `--new-link`

    This flag will force the uploaded deck images to have new image links, which is useful for invalidating mod cache.

- `--step`

    The particular step to run this automation script. Explained in more details below.

The script runs in the following steps. Each step only requires persisted data generated from the previous steps, so if you kill the script half way, you should be able to continue from the last unfinished steps.

1. *Translate* the card objects in the mod repositories. The translation data will be saved in the `SE_Generator/data` directory as CSV files.

2. *Generate* the Strange Eons script to generate a list of individual translated card images, saved in the `SE_Generator/images` directory. This step will not overwrite preiviously generated images.

3. *Pack* the individual translated images into deck images and save them into the deck image directory.

4. *Upload* all the translated deck images to the image host.

5. *Update* the objects in the mod repositoires.

Upon finishing the above steps, the mod repositories in the cache directory will have unstaged changes ready for you to commit. If you use your own fork, you also need to manually update the [repository URL](https://github.com/argonui/SCED/blob/545181308bdb9266e0ac16005f1d51ecbde043fb/src/core/Global.ttslua#L45) in the mod.

### URL mapping file

The URL mapping file keeps track of the original and translated deck image URLs so that update is possible. It also assigns a uuid for each unique deck image. If this file is deleted, the script will forget all the URLs it has seen before and will not recognize previously processed deck images.

### Cache directory

The cache directory keeps the list of intermediate resources required for processing. This includes the processed ArkhamDB translation data, the original deck images, the cropped individual images, and more.

### Intermediate filenames

During processing, the script will generate a series of files with strange filenames. Those filenames encode the necessary information for the following steps to process them. This includes the deck image URL id, the slot within the deck image, whether the image has been rotated, and more.

### SE_Generator project

The `SE_Generator` directory is a self-contained Strange Eons project. This means you can open this project in the Strange Eons UI and inspect its content, as well as running its automation script. Please note it seems that the Strange Eons UI cannot run at the same time as its command line.

### Translation directory

Some cards don't have direct entries on ArkhamDB, e.g. taboo cards, so we include their translation data in the `translations` folder.

Run misc/taboo.py script to download latest taboo changes.

If you want to perform any language dependent transformation on generated text, you can add a `transform.py` file (with region code suffix) and declare the corresponding [transformation functions](https://github.com/lriuui0x0/SCED_Localization/blob/master/translations/zh/transform_CN.py). You will likely need to declare an entry for `transform_victory` at least because ArkhamDB translation data doesn't translate the word "Victory".

### Dropbox access token

To get an access token for Dropbox, you need to first [create an application](https://www.dropbox.com/developers/apps), then make sure you tick every individual scope permission in the permissions tab. Generate an access token on the settings tab.

