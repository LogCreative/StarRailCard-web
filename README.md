## StarRailCard-web

A static web page generator for StarRailCard based on [StarRailCard](https://github.com/DEViantUA/StarRailCard).

<img width="669" alt="preview" src="https://github.com/LogCreative/StarRailCard/assets/61653082/731cd519-0d3c-4a6d-a63e-f04c91263ade">

## Usage

Install the dependencies:
```bash
pip install -r requirements.txt
```

And run the script, pass the uid as the argument:
```bash
python main.py -u 109814396
```
If you want to change the language, for example, to Chinese (Simplified) with the correct font being used, then use:
```bash
python main.py -u 109814396 -l cn -f "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
```
where `/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc` font should be installed on your computer manually.

You could get more help by
```bash
python main.py -h
```

After the generation, you could open `railcard.html` directly to preview the result. You could directly deploy those files to your website. Click the avatar to display the detail of different characters. And `profile.jpg` is also generated for your own use. You could add your customized style to make it look better.
