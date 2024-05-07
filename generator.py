from fontTools import ttLib
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen 

import pyperclip

title = "L'AVENTURIER"
artist = "INDOCHINE"
year = "1982"
lyrics = """Egare dans la vallee infernale
Le heros s'appelle Bob Morane
A la recherche de l'Ombre Jaune
Le bandit s'appelle Mister Kali Jones
Avec l'ami Bill Ballantine
Sauve de justesse des crocodiles
Stop au trafic des Caraibes
Escale dans l'operation Nadawieb
Le coeur tendre dans le lit de Miss Clark
Prisonniere du Sultan de Jarawak
En pleine terreur a Manicouagan
Isole dans la jungle birmane
Emprisonnant les flibustiers
L'ennemi est demasque
On a vole le collier de Civa
Le Maharadjah en repondra
Et soudain surgit face au vent
Le vrai heros de tous les temps
Bob Morane contre tout chacal
L'aventurier contre tout guerrier
Bob Morane contre tout chacal
L'aventurier contre tout guerrier
Derivant a bord du Liang
L'aventure au parfum d'Ylalang
Son surnom, Samourai du Soleil
En demantelant le gang de l'Archipel
L'otage des guerriers du Doc Xhatan
Il s'en sortira toujours a temps
Tel l'aventurier solitaire
Bob Morane est le roi de la Terre
Et soudain surgit face au vent
Le vrai heros de tous les temps
Bob Morane contre tout chacal
L'aventurier contre tout guerrier
Bob Morane contre tout chacal
L'aventurier contre tout guerrier"""
intro = 4

font = ttLib.TTFont("ressources/LiberationSans-Bold.ttf")
scale_factor = 17 / font["head"].unitsPerEm
cmap = font.getBestCmap(((0, 3),))

ponctuations = ["...", "!", "?"]
chars_width = {}
for c in lyrics:
    if c != "\n":
        chars_width[c.upper()] = font["hmtx"][cmap[ord(c.upper())]][0]

lyrics = list(map(lambda x: x.strip(), lyrics.split('\n')))

svg_width = 830
with open("ressources/BACKGROUND.svg", "r") as bg:
    background = bg.readlines()

answer_count = 1

export = "HINT\tHINT\tANSWER\nSVG_ID\tVERS\tMot\n"

def draw_sentence(out, words, answer_count = None, vers = None):
    width = 0
    words_width = {}
    for word in words:
        words_width[word] = 0
        for char in word.upper():
            words_width[word] += chars_width[char]
        width += words_width[word] * scale_factor
    width += (len(words) - 1) * font["hmtx"]["space"][0] * scale_factor
    x = (svg_width - width) / 2
    for word in words:
        ans_id = "" if answer_count is None else f"ans{answer_count}"
        ans_tag = "" if answer_count is None else f"{ans_id} text"
        if len(word) > 1:
            buffer = "" 
            out.write(f'<g class="{ans_tag}" transform="translate({x} {y})">\n')
            inside_padding = 0
            for char in word:
                spen = SVGPathPen(font.getGlyphSet, lambda f : str(round(f, 3)))
                pen = TransformPen(spen, (scale_factor, 0, 0, -scale_factor, inside_padding * scale_factor, 0))
                inside_padding += chars_width[char.upper()]
                id = cmap[ord(char.upper())]
                # print(id)
                font.getGlyphSet()[id].draw(pen)
                if char in "'-.?!,":
                    underline_tag = "" if answer_count is None else "underline"
                    buffer += f'<g transform="translate({x} {y})"><path class="{ans_id} {underline_tag}" d="{spen.getCommands()}"/></g>\n'
                else:    
                    out.write(f'<path d="{spen.getCommands()}"/>\n')
            out.write('</g>\n')
            out.write(f'{buffer}\n')
        elif len(word) == 1:
            out.write(f'<g transform="translate({x} {y})">\n')
            spen = SVGPathPen(font.getGlyphSet, lambda f: str(round(f, 3)))
            pen = TransformPen(spen, (scale_factor, 0, 0, -scale_factor, 0, 0))
            id = cmap[ord(word.upper())]
            font.getGlyphSet()[id].draw(pen)
            out.write(f'<path class="{ans_tag}" d="{spen.getCommands()}"/>\n')
            out.write('</g>\n')
        if answer_count is not None and word not in ["...", "!", "?"]:
            out.write(f'<rect class="underline {ans_id}" x="{x}" y="{y+5}" width="{words_width[word] * scale_factor}" height="2"/>')
            answer_count += 1
            global export 
            export += f"{ans_id}\tVers {vers}\t{word}\n"
        x += (words_width[word] + font["hmtx"]["space"][0]) * scale_factor
    return answer_count

def get_string_width(str, scale_factor=scale_factor, font=font):
    width = 0
    for char in str:
        width += chars_width[char]
    return width * scale_factor

def number_of_ans(words) -> int:
    return len(list(filter(lambda s: s != "...", words))) 


with open(f"{title}.svg", "w") as out:
    for line in background[:-2:]:
        out.write(line)

    # Titre, artistes, année
    out.write('<g transform="translate(9.7656e-6 .28643)" font-family="sans-serif" font-weight="bold">\n')
    title_x = 346.320 - 7
    artist_x = 370.200 - 7
    out.write(f'<text x="{title_x}" y="307.5" fill="#f2f2f2" font-size="20px" style="line-height:1.25" xml:space="preserve"><tspan x="{title_x}" y="307.5">{title}</tspan></text>\n')
    out.write(f'<text x="{artist_x}" y="331.90356" fill="#5c87c5" font-size="16px" font-style="italic" xml:space="preserve"><tspan x="{artist_x}" y="331.90356" font-size="16px" font-style="italic">{artist}</tspan></text>\n')
    out.write(f'<text x="393.36526" y="356.26712" fill="#5c87c5" font-size="16px" font-style="italic" xml:space="preserve"><tspan x="393.36526" y="356.26712" font-size="16px" font-style="italic">{year}</tspan></text>\n')
    out.write('</g>\n')
    out.write('</g>\n')

    intro_count = 1
    y = 360
    for i in range(intro):
        tag = f"sentence intro{intro_count}"
        out.write(f'<g class="{tag}" fill="#f2f2f2">\n')
        draw_sentence(out, lyrics[i].split(' '))
        out.write(f'</g>\n')
        intro_count += 1

    vers = 1
    for i in range(intro, len(lyrics)):
        ans_in = "sentence1 " if vers == 1 else ""
        words = lyrics[i].split(' ')
        for i in range(answer_count, answer_count + number_of_ans(words)):
            ans_in += f"ans{i} "
        out.write(f'<g class=\"sentence {ans_in}\" fill="#fe5f55">\n')
        answer_count = draw_sentence(out, words, answer_count, vers)
        out.write('</g>\n')
        vers += 1

    out.write("</svg>")       

pyperclip.copy(export)