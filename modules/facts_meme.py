from PIL import Image, ImageDraw, ImageFont
from functools import reduce


BOX_DIM = (1125, 760)
ANGLE = -17
LOC = (40, 2050)
LINE_OFFSET = 75
LINE_CAPACITY = 28


def fact_parser(fact):
    if len(fact) <= LINE_CAPACITY:
        return [fact]

    lines = []
    while len(fact) > 0:
        line = fact[:LINE_CAPACITY]
        fact = fact[LINE_CAPACITY:]
        if len(line) == 28 and not line[-1].isspace():
            end_char = line[-1]
            line = line[:-1] + '-'
            fact = end_char + fact
        lines.append(line)
    
    return lines


def gen_facts_meme(fact):
    parsed_fact = fact.split('\n')                                  # in case user utilizes separate lines
    parsed_fact = map(lambda l: l.replace('\r', ''), parsed_fact)   # removes weird symbol from text input box
    parsed_fact = map(lambda l: fact_parser(l), parsed_fact)        # parses each individual line
    parsed_fact = reduce(lambda a, b: a + b, parsed_fact)           # Concatenates all lists together
    
    facts_template = Image.open('./static/facts_template.jpg')
    
    box = Image.new('RGBA', BOX_DIM, (255, 255, 255, 0))
    d = ImageDraw.Draw(box)
    font = ImageFont.truetype("arial.ttf", LINE_OFFSET)
    
    for idx in range(len(parsed_fact)):
        line = parsed_fact[idx]
        d.text((9, LINE_OFFSET*idx), line, fill=(0, 0, 0, 255), font=font)

    box = box.rotate(ANGLE, expand=True)

    facts_template.paste(box, LOC, box)
    facts_template.save('./output.jpg', 'JPEG')
    return "./output.jpg", None
