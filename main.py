import asyncio
import os, shutil, sys
import argparse

import starrailcard
from starrailcard.src.api import api
from starrailcard.src.tools.pill.image_control import get_download_img
from starrailcard.src.tools.translator import SUPPORTED_LANGUAGES

parser = argparse.ArgumentParser(prog='Star Rail Card Web',
            description='A static web page generator for StarRailCard')
parser.add_argument('--uid', '-u', metavar='U', type=str, help="account uid", required=True)
parser.add_argument('--style', '-s', metavar='S', type=int, default=2,
                    help="style type (default: 2)")
parser.add_argument('--outputdir', '-o', metavar='O', type=str, default='RailCard',
                    help="image directory for saving (default: RailCard)")
parser.add_argument('--imgdir', '-fo', metavar='FO', type=str, default=None,
                    help="final imgdir variable in railcard_config.js (default: <outputdir>)")
parser.add_argument('--lang', '-l', metavar='L', choices=SUPPORTED_LANGUAGES.keys(), default='en',
                    help="display language (default: en)")
parser.add_argument('--font', '-f', metavar='F', type=str, default=None,
                    help="the name or the path for the font to be used (default: None)")
parser.add_argument('--preserve', '-p', metavar='P', type=bool, default=False,
                    help="whether to preserve previous character runs, " + 
                    "which is useful if you want to display more characters (default: False)")
args = parser.parse_args()

uid       = args.uid
style     = args.style
outputdir = args.outputdir
imgdir    = outputdir if args.imgdir is None else args.imgdir
lang      = args.lang
font      = args.font
preserve  = args.preserve

if os.path.exists(outputdir):
    if not preserve:
        shutil.rmtree(outputdir)
os.makedirs(outputdir, exist_ok=True)

async def main():
    async with starrailcard.Card(lang=lang, user_font=font) as card:

        profile_result = await card.create_profile(uid)
        print(profile_result)
        profile_result.card.convert('RGB').save(os.path.join(outputdir, 'profile.jpg'))

        # avatar
        user_profile = await api.ApiMiHoMo(uid, lang=lang).get()
        for character in user_profile.characters:
            character_avatar_filename = "avatar-{}-{}.png".format(character.name.replace(' ','_'), character.rarity)
            character_avatar = await get_download_img(character.icon)
            character_avatar.save(os.path.join(outputdir, character_avatar_filename))

        # card
        r = await card.create(uid=uid, style=style)
        print(r)
        character_list_str = []
        for character_card in r.card:
            character_fullname = "{}-{}".format(character_card.name.replace(' ','_'), character_card.rarity)
            character_card_filename = "card-{}.jpg".format(character_fullname)
            character_card.card.convert('RGB').save(os.path.join(outputdir, character_card_filename))
            character_list_str.append('"{}"'.format(character_fullname))

        # in case there are more characters in the folder
        for filename in os.listdir(outputdir):
            if 'avatar-' in filename:
                f_character_name = filename.rsplit('.')[0].split('-')[1]
                f_character_rarity = filename.rsplit('.')[0].split('-')[2]
                f_character_fullname = '"' + "{}-{}".format(f_character_name, f_character_rarity) + '"'
                if f_character_fullname not in character_list_str:
                    character_list_str.append(f_character_fullname)
        
        # config
        with open("railcard_config.js", "w") as config_js:
            config_js.write("characters = [{}];\nimgdir = \"{}\"\n".format(
                ', '.join(character_list_str), imgdir))
            
        # finish
        print("\nGeneration finished in dir: {}".format(outputdir))
        print("Config is generated in: railcard_config.js, image diretory is: {}".format(imgdir))
        print("Web page could be viewed in: railcard.html")

asyncio.run(main())
