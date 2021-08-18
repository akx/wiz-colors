import colorsys
import json
import re
import xml.etree.ElementTree as et
from functools import lru_cache


def get_color_string_ids():
    color_string_ids = {}
    with open("input/public.xml", encoding="UTF-8") as f:
        for el in et.parse(f).getroot().findall("public"):
            if el.get("type") != "string":
                continue
            name = el.get("name")
            if not name.startswith("Color_"):
                continue
            color_string_ids[int(el.get("id")[2:], 16)] = name
    return color_string_ids


def get_color_names():
    color_string_names = {}
    with open("input/strings.xml", encoding="UTF-8") as f:
        for el in et.parse(f).getroot().findall("string"):
            name = el.get("name")
            if not name.startswith("Color_"):
                continue
            color_string_names[name] = el.text
    return color_string_names


def extract_static_constructor():
    in_static_block = False
    with open("input/NamedColorHelper.smali", encoding="UTF-8") as f:
        for i, line in enumerate(f, 1):
            line, *_ = line.partition("#")
            line = line.strip()
            if not line:
                continue
            if line == "new-array v1, v1, [Lcom/tao/wiz/data/entities/NamedColor;":
                in_static_block = True
                continue
            if in_static_block:
                if line == ".end method":
                    return
                yield (i, line)


CONST_RE = r"^const(.*?) (?P<target>.+), (?P<value>.+)"
INVOKE_DIRECT_RE = r"^invoke-direct {(?P<r1>.+?), (?P<r2>.+?), (?P<r3>.+?)}, Lcom/tao/wiz/data/entities/NamedColor"


def parse_smali():
    registers = {}
    for i, line in extract_static_constructor():
        if m := re.match(CONST_RE, line):
            registers[m.group("target")] = m.group("value")
        elif m := re.match(INVOKE_DIRECT_RE, line):
            # hack: assumes registers start out as 0
            v1 = registers.get(m.group("r2"), "0x0")
            v2 = registers.get(m.group("r3"), "0x0")
            yield (v1, v2)


@lru_cache(maxsize=None)
def hex2rgb(h):
    return [int(c, 16) for c in (h[1:3], h[3:5], h[5:7])]


def is_dark(hex):
    r, g, b = [c / 255 for c in hex2rgb(hex)]
    return (0.30 * r + 0.59 * g + 0.11 * b) < 0.5


def get_sort_order(hex):
    r, g, b = [c / 255 for c in hex2rgb(hex)]
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    # y, i, q = colorsys.rgb_to_yiq(r, g, b)
    if s < 0.4:  # desaturated colors: sort by value
        return (0, l)
    hx, hq = divmod(h * 6, 1)
    return (1, hx, l * (1 if hx % 2 else -1))


HTML_PRELUDE = """
<html>
<style>
body{display:flex;flex-wrap:wrap;font-family:sans-serif}
div{flex:1;max-width: 10vw;min-width: 5em;margin:6px;padding:3px;text-align:center;border-radius:2px}
.d{color:#fff}
</style>
<body>
"""


def write_outputs(name_to_color_map):
    with open("colors.tsv", "w", encoding="UTF-8", newline="\n") as outf:
        for tup in sorted(name_to_color_map.items()):
            print(*tup, sep="\t", file=outf)
    with open("colors.json", "w", encoding="UTF-8", newline="\n") as outf:
        json.dump(name_to_color_map, outf, sort_keys=True, indent=2)
    with open("colors.html", "w", encoding="UTF-8", newline="\n") as outf:
        print(
            HTML_PRELUDE.strip(),
            file=outf,
        )
        for name, color in sorted(name_to_color_map.items(), key=lambda pair: get_sort_order(pair[1])):
            cls = "d" if is_dark(color) else "l"
            print(
                f'<div style="background: {color}" class="{cls}">{name}</div>',
                file=outf,
            )
        print("</body></html>", file=outf)


def main():
    name_to_color_map = get_name_to_hex_map()
    write_outputs(name_to_color_map)


def get_name_to_hex_map():
    string_id_to_string_name_map = get_color_string_ids()
    string_name_to_human_name_map = get_color_names()
    string_id_to_human_name_map = {
        string_id: string_name_to_human_name_map.get(string_name, string_id)
        for (string_id, string_name) in string_id_to_string_name_map.items()
    }
    string_id_to_color = {int(v2[2:], 16): int(v1[2:], 16) for (v1, v2) in parse_smali()}
    name_to_color_map = {
        string_id_to_human_name_map.get(string_id, string_id).strip('"'): f"#{color:06x}"
        for (string_id, color) in string_id_to_color.items()
    }
    return name_to_color_map


if __name__ == "__main__":
    main()
