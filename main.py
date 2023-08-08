import asyncio
import os, shutil, sys
import argparse

from starrailcard import honkaicard
from starrailcard.src.tools.pill import get_dowload_img
from starrailcard.src.tools.translation import supportLang

parser = argparse.ArgumentParser(prog='Star Rail Card Web',
            description='A static web page generator for StarRailCard')
parser.add_argument('--uid', '-u', metavar='U', type=str, help="account uid", required=True)
parser.add_argument('--outputdir', '-o', metavar='O', type=str, default='RailCard',
                    help="image directory for saving (default: RailCard)")
parser.add_argument('--imgdir', '-fo', metavar='FO', type=str, default=None,
                    help="final imgdir variable in railcard_config.js (default: <outputdir>)")
parser.add_argument('--lang', '-l', metavar='L', choices=supportLang.keys(), default='en',
                    help="display language (default: en)")
parser.add_argument('--preserve', '-p', metavar='P', type=bool, default=False,
                    help="whether to preserve previous character runs, " + 
                    "which is useful if you want to display more characters (default: False)")
args = parser.parse_args()

uid       = args.uid
outputdir = args.outputdir
imgdir    = outputdir if args.imgdir is None else args.imgdir
lang      = args.lang
preserve  = args.preserve

if os.path.exists(outputdir):
    if not preserve:
        shutil.rmtree(outputdir)
os.makedirs(outputdir, exist_ok=True)

async def main():
    async with honkaicard.MiHoMoCard(lang=lang) as hmhm:

        # avatar
        user_profile = await hmhm.API.get_full_data(uid)
        for character in user_profile.characters:
            character_avatar_filename = "avatar-{}-{}.png".format(character.name.replace(' ','_'), character.rarity)
            character_avatar = await get_dowload_img(character.icon)
            character_avatar.save(os.path.join(outputdir, character_avatar_filename))

        # card
        r = await hmhm.creat(uid=uid)
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
