#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
Copyright (c) 2011 Tyler Kenendy <tk@tkte.ch>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

try:
    import json
except ImportError:
    import simplejson as json

import traceback

import six
import six.moves.urllib.request

from .topping import Topping

from jawa.constants import *

VERSION_MANIFEST = "https://launchermeta.mojang.com/mc/game/version_manifest.json"
LEGACY_VERSION_META = "https://s3.amazonaws.com/Minecraft.Download/versions/%(version)s/%(version)s.json" # DEPRECATED
RESOURCES_SITE = "http://resources.download.minecraft.net/%(short_hash)s/%(hash)s"
HARDCODED = {
    "18w19a": "https://launchermeta.mojang.com/mc/game/8cab0b2d8df90d8f21fd9c342b57fc1ac84ad52a/18w19a.json",
    "18w19b": "https://launchermeta.mojang.com/mc/game/47fc76c26b3350cacf86d0e6d426a06d34917e1c/18w19b.json",
    "18w20a": "https://launchermeta.mojang.com/mc/game/6a078865551f0d7732769c83c87d7cef1b2929a1/18w20a.json",
    "18w20b": "https://launchermeta.mojang.com/mc/game/a37d0ee906d1acabf894f3d2d3b93207909fc3af/18w20b.json",
    "18w20c": "https://launchermeta.mojang.com/mc/game/812951283c7120566e92f34dad4ee09e5a854d51/18w20c.json",
    "18w21a": "https://launchermeta.mojang.com/mc/game/8086f166a4ff022bf3a41523938e7dc3692c017f/18w21a.json",
    "18w21b": "https://launchermeta.mojang.com/mc/game/9ed07f1fcd93eb32979d5c367a63820628616412/18w21b.json",
    "18w22a": "https://launchermeta.mojang.com/mc/game/debf733624cfe568c56e4cdb42b39dc959df713c/18w22a.json",
    "18w22b": "https://launchermeta.mojang.com/mc/game/a93133e085caa8211034e8c10ba4840c49c2857f/18w22b.json",
    "18w22c": "https://launchermeta.mojang.com/mc/game/2bb76d3183471e759a250225116dff75e52e9aa8/18w22c.json",
    "1.13-pre1": "https://launchermeta.mojang.com/mc/game/8dbe24cb291acdf402a110ec922a15ec59d02a22/1.13-pre1.json",
    "1.13-pre2": "https://launchermeta.mojang.com/mc/game/6b31fc4f3cf1672bd4cf49d2f1fc39facc2af4f3/1.13-pre2.json",
    "1.13-pre3": "https://launchermeta.mojang.com/mc/game/f703320e27cb311c757cf320deb1ae96d8cf78b2/1.13-pre3.json",
    "1.13-pre4": "https://launchermeta.mojang.com/mc/game/5dd6bac3d40c95db2fe8718ab0bb507f74ad4c00/1.13-pre4.json",
    "1.13-pre5": "https://launchermeta.mojang.com/mc/game/1bc3bb4054ddac170c970c936975cc4a7e4d8855/1.13-pre5.json",
    "1.13-pre6": "https://launchermeta.mojang.com/mc/game/0815eae6f719740cc0ea69be6e2b715ae15191fb/1.13-pre6.json",
    "1.13-pre7": "https://launchermeta.mojang.com/mc/game/4aa225abb7ac2763f683aa7490226660c3462341/1.13-pre7.json",
    "1.13-pre8": "https://launchermeta.mojang.com/mc/game/934629cee90d584c649c8d288d3737ae558f3405/1.13-pre8.json",
    "1.13-pre9": "https://launchermeta.mojang.com/mc/game/cb10cf2c867006d90e91044edde94eeea95f710f/1.13-pre9.json",
    "1.13-pre10": "https://launchermeta.mojang.com/mc/game/d47ad89224d8bf79d6cd71619e9699ad4083f47c/1.13-pre10.json",
    "1.13": "https://launchermeta.mojang.com/mc/game/3132596cced9f9d6f1ca97aeec75651e6a9df0bc/1.13.json",
    "18w30a": "https://launchermeta.mojang.com/mc/game/7fc78b1de5a9d288a7279524aa071bef2c5160dd/18w30a.json",
    "18w30b": "https://launchermeta.mojang.com/mc/game/9e0841c5a5db7efdef2f8ebe6147440dfad38a70/18w30b.json",
    "18w31a": "https://launchermeta.mojang.com/mc/game/824b860a1f3b8a7e6d4b433a73e787be57a66f16/18w31a.json",
    "18w32a": "https://launchermeta.mojang.com/mc/game/7eb858d300e55e2240ab92abbb0179656ac8f710/18w32a.json"
}

def load_json(url):
    stream = six.moves.urllib.request.urlopen(url)
    try:
        return json.load(stream)
    finally:
        stream.close()

def get_version_meta(version, verbose):
    """
    Gets a version metadata file using the (deprecated)
    s3.amazonaws.com/Minecraft.Download pages.  This is done because e.g.
    older snapshots do not exist in the version manifest but do exist here.
    """
    version_manifest = load_json(VERSION_MANIFEST)
    for version_info in version_manifest["versions"]:
        if version_info["id"] == version:
            address = version_info["url"]
            break
    else:
        if verbose:
            print("Failed to find %s in the main version manifest" % version)
        if version in HARDCODED:
            print("Using hardcoded fallback")
            address = HARDCODED[version]
        else:
            print("Using legacy site")
            address = LEGACY_VERSION_META % {'version': version}
    if verbose:
        print("Loading version manifest for %s from %s" % (version, address))
    return load_json(address)

def get_asset_index(version_meta, verbose):
    """Downloads the Minecraft asset index"""
    if "assetIndex" not in version_meta:
        raise Exception("No asset index defined in the version meta")
    asset_index = version_meta["assetIndex"]
    if verbose:
        print("Assets: id %(id)s, url %(url)s" % asset_index)
    return load_json(asset_index["url"])

def get_sounds(asset_index, resources_site=RESOURCES_SITE):
    """Downloads the sounds.json file from the assets index"""
    hash = asset_index["objects"]["minecraft/sounds.json"]["hash"]
    short_hash = hash[0:2]
    sounds_url = resources_site % {'hash': hash, 'short_hash': short_hash}

    sounds_file = six.moves.urllib.request.urlopen(sounds_url)

    try:
        return json.load(sounds_file)
    finally:
        sounds_file.close()

class SoundTopping(Topping):
    """Finds all named sound effects which are both used in the server and
       available for download."""

    PROVIDES = [
        "sounds"
    ]

    DEPENDS = [
        "identify.sounds.list",
        "identify.sounds.event",
        "version.name",
        "language"
    ]

    @staticmethod
    def act(aggregate, classloader, verbose=False):
        sounds = aggregate.setdefault('sounds', {})
        try:
            version_meta = get_version_meta(aggregate["version"]["name"], verbose)
        except Exception as e:
            if verbose:
                print("Error: Failed to download version meta for sounds: %s" % e)
                traceback.print_exc()
            return
        try:
            assets = get_asset_index(version_meta, verbose)
        except Exception as e:
            if verbose:
                print("Error: Failed to download asset index for sounds: %s" % e)
                traceback.print_exc()
            return
        try:
            sounds_json = get_sounds(assets)
        except Exception as e:
            if verbose:
                print("Error: Failed to download sound list: %s" % e)
                traceback.print_exc()
            return

        if not 'sounds.list' in aggregate["classes"]:
            # 1.8 - TODO implement this for 1.8
            return

        soundevent = aggregate["classes"]["sounds.event"]
        cf = classloader[soundevent]

        # Find the static sound registration method
        method = cf.methods.find_one(args='', returns="V", f=lambda m: m.access_flags.acc_public and m.access_flags.acc_static)

        sound_name = None
        sound_id = 0
        for ins in method.code.disassemble():
            if ins.mnemonic in ('ldc', 'ldc_w'):
                const = ins.operands[0]
                sound_name = const.string.value
            elif ins.mnemonic == 'invokestatic':
                sound = {
                    "name": sound_name,
                    "id": sound_id
                }
                sound_id += 1

                if sound_name in sounds_json:
                    json_sound = sounds_json[sound_name]
                    if "sounds" in json_sound:
                        sound["sounds"] = []
                        for value in json_sound["sounds"]:
                            data = {}
                            if isinstance(value, six.string_types):
                                data["name"] = value
                                path = value
                            elif isinstance(value, dict):
                                # Guardians use this to have a reduced volume
                                data = value
                                path = value["name"]
                            asset_key = "minecraft/sounds/%s.ogg" % path
                            if asset_key in assets["objects"]:
                                data["hash"] = assets["objects"][asset_key]["hash"]
                            sound["sounds"].append(data)
                    if "subtitle" in json_sound:
                        subtitle = json_sound["subtitle"]
                        sound["subtitle_key"] = subtitle
                        # Get rid of the starting key since the language topping
                        # splits it off like that
                        subtitle_trimmed = subtitle[len("subtitles."):]
                        if subtitle_trimmed in aggregate["language"]["subtitles"]:
                            sound["subtitle"] = aggregate["language"]["subtitles"][subtitle_trimmed]

                sounds[sound_name] = sound

        # Get fields now
        soundlist = aggregate["classes"]["sounds.list"]
        lcf = classloader[soundlist]

        method = lcf.methods.find_one(name="<clinit>")
        for ins in method.code.disassemble():
            if ins.mnemonic in ('ldc', 'ldc_w'):
                const = ins.operands[0]
                sound_name = const.string.value
            elif ins.mnemonic == "putstatic":
                if sound_name is None or sound_name == "Accessed Sounds before Bootstrap!":
                    continue
                const = ins.operands[0]
                field = const.name_and_type.name.value
                sounds[sound_name]["field"] = field
