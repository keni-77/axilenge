from fontTools.fontBuilder import FontBuilder
from fontTools.ttLib import newTable
from fontTools.pens.ttGlyphPen import TTGlyphPen

UPM = 1000
fb = FontBuilder(UPM, isTTF=True)

# -----------------------------
# グリフ一覧
# -----------------------------
glyph_order = [".notdef"]

# 子音16個（4bit）
for i in range(16):
    glyph_order.append(f"cons_{i:04b}")

# 母音6個
vowels = ["u", "o", "a", "e", "i", "schwa"]
for v in vowels:
    glyph_order.append(f"vowel_{v}")

# 有声音マーク
glyph_order.append("voicing")

fb.setupGlyphOrder(glyph_order)

# -----------------------------
# cmap（PUA割り当て）
# -----------------------------
cmap = {}
base = 0xE100
for i in range(16):
    cmap[base + i] = f"cons_{i:04b}"

base_v = 0xE200
for idx, v in enumerate(vowels):
    cmap[base_v + idx] = f"vowel_{v}"

cmap[0xE300] = "voicing"

fb.setupCharacterMap(cmap)

# -----------------------------
# グリフ描画関数
# -----------------------------
def draw_consonant(bits):
    tl = (bits & 0b1000) != 0
    tr = (bits & 0b0100) != 0
    bl = (bits & 0b0010) != 0
    br = (bits & 0b0001) != 0

    pen = TTGlyphPen(None)

    # 外枠
    pen.moveTo((100, 100))
    pen.lineTo((900, 100))
    pen.lineTo((900, 900))
    pen.lineTo((100, 900))
    pen.closePath()

    # 4隅の線
    if tl:
        pen.moveTo((100, 900))
        pen.lineTo((300, 900))
    if tr:
        pen.moveTo((900, 900))
        pen.lineTo((700, 900))
    if bl:
        pen.moveTo((100, 100))
        pen.lineTo((300, 100))
    if br:
        pen.moveTo((900, 100))
        pen.lineTo((700, 100))

    return pen.glyph()

def draw_arrow(direction):
    pen = TTGlyphPen(None)
    if direction == "u":      # ←
        pen.moveTo((500, 500)); pen.lineTo((200, 500))
    elif direction == "o":    # ↙
        pen.moveTo((500, 500)); pen.lineTo((300, 300))
    elif direction == "a":    # ↓
        pen.moveTo((500, 500)); pen.lineTo((500, 200))
    elif direction == "e":    # ↘
        pen.moveTo((500, 500)); pen.lineTo((700, 300))
    elif direction == "i":    # →
        pen.moveTo((500, 500)); pen.lineTo((800, 500))
    elif direction == "schwa": # ↑
        pen.moveTo((500, 500)); pen.lineTo((500, 800))
    return pen.glyph()

def draw_voicing():
    pen = TTGlyphPen(None)
    pen.moveTo((750, 850))
    pen.lineTo((780, 850))
    return pen.glyph()

# -----------------------------
# グリフ生成
# -----------------------------
glyphs = {}
advance = {}

# notdef
pen = TTGlyphPen(None)
glyphs[".notdef"] = pen.glyph()
advance[".notdef"] = (UPM, 0)

# 子音16
for i in range(16):
    name = f"cons_{i:04b}"
    glyphs[name] = draw_consonant(i)
    advance[name] = (UPM, 0)

# 母音6
for v in vowels:
    name = f"vowel_{v}"
    glyphs[name] = draw_arrow(v)
    advance[name] = (UPM, 0)

# 有声音マーク
glyphs["voicing"] = draw_voicing()
advance["voicing"] = (UPM, 0)

fb.setupGlyf(glyphs)
fb.setupHorizontalMetrics(advance)

# -----------------------------
# 基本テーブル
# -----------------------------
fb.setupHorizontalHeader(ascent=800, descent=-200)
fb.setupNameTable({
    "familyName": "MyConscript",
    "styleName": "Regular",
    "fullName": "MyConscript Regular",
    "uniqueFontIdentifier": "MyConscriptRegular",
    "psName": "MyConscript-Regular",
})
fb.setupOS2()
fb.setupPost()

maxp = newTable("maxp")
maxp.tableVersion = 0x00010000
maxp.numGlyphs = len(glyph_order)
fb.font["maxp"] = maxp

# -----------------------------
# OTF生成
# -----------------------------
fb.save("myfont.otf")
print("generated myfont.otf")
