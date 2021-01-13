#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import random2
from PIL import Image, ImageDraw, ImageFont
result = [0, '.', ',', 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
for i in range(10):
    result.append(random2.randint(0, 9))
random2.shuffle(result)
numList = "".join([str(x) for x in result])
image = Image.new('RGBA', (1200, 50), (255, 255, 255, 0))
font = ImageFont.truetype('msyh.ttc', 36)
draw = ImageDraw.Draw(image)
for i, v in enumerate(result):
    index = (i + 1) * 30
    draw.text((index, 2), str(v), font=font, fill=(255, 102, 0, 255))
image.save('pic.png', 'PNG')
file = open("pic.css", "w+")
for i, v in enumerate(result):
    position = 30 * (i + 1)
    css = ".p_" + str(i) + "{background:url('pic.png') no-repeat -" + str(
        position) + "px #fff; width: 20px;}" + "\n"
    file.write(css)
file.close()
