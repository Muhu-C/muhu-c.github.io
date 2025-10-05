import pyperclip
import re

img_str = pyperclip.paste()

if img_str.startswith("[") or img_str.startswith("!") or not img_str.endswith(".png") or not img_str.endswith(".png") or not img_str.endswith(".avif") or not img_str.endswith(".webp"):
    img_str = re.findall("(https://(.*?)(.jpg|.png|.avif|.webp))", img_str)[0][0]

pyperclip.copy(img_str)