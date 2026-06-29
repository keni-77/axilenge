# build_font.py
# 実行: python build_font.py
# 必要: pip install fonttools

from fontTools.fontBuilder import FontBuilder
from fontTools.ttLib import newTable
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.feaLib.builder import addOpenTypeFeaturesFromString

UPM = 1000
PUA_BASE = 0xE500

# --- 子音・母音の定義 ---
consOrder = [
    "t","d","k","g","h","w","s","z","p","b","n","j","l","f","m",
    "x","tx","ng","th"
]
vowels = ["u","o","a","e","i","q"]
voiced_set = {"d","g","z","b"}

# consonant -> bits (top=0b1000, right=0b0100, bottom=0b0010, left=0b0001)
consonant_to_bits = {
    "t":  0b1001,  # 上 左
    "d":  0b1001,  # t と同じ + '
    "k":  0b1011,  # 上 左 下
    "g":  0b1011,  # k と同じ + '
    "h":  0b0101,  # 左 右
    "w":  0b0111,  # 左 下 右
    "s":  0b1111,  # 上 下 左 右
    "z":  0b1111,  # s と同じ + '
    "p":  0b0011,  # 左 下
    "b":  0b0011,  # p と同じ + '
    "n":  0b1101,  # 左 上 右
    "j":  0b0110,  # 右 下
    "l":  0b0001,  # 左
    "f":  0b1010,  # 上 下
    "m":  0b1000,  # 上
    "x":  0b0010,  # 下
    "tx": 0b0100,  # 右
    "ng": 0b1110,  # 上 右 下
    "th": 0b1100,  # 上 右
}

# --- 描画定数 ---
STROKE = 50
MARGIN = 80
TRI_SIZE = 130
VOICE_R = 40

BOX_LEFT   = MARGIN
BOX_RIGHT  = UPM - MARGIN
BOX_BOTTOM = MARGIN
BOX_TOP    = UPM - MARGIN
CX = (BOX_LEFT + BOX_RIGHT) // 2
CY = (BOX_BOTTOM + BOX_TOP) // 2

# --- 描画ユーティリティ ---
def rect(pen, x1, y1, x2, y2):
    pen.moveTo((x1, y1))
    pen.lineTo((x2, y1))
    pen.lineTo((x2, y2))
    pen.lineTo((x1, y2))
    pen.closePath()

def tri(pen, p1, p2, p3):
    pen.moveTo(p1)
    pen.lineTo(p2)
    pen.lineTo(p3)
    pen.closePath()

def draw_consonant_edges(pen, bits):
    if bits & 0b1000:  # 上辺
        rect(pen, BOX_LEFT, BOX_TOP - STROKE, BOX_RIGHT, BOX_TOP)
    if bits & 0b0100:  # 右辺
        rect(pen, BOX_RIGHT - STROKE, BOX_BOTTOM, BOX_RIGHT, BOX_TOP)
    if bits & 0b0010:  # 下辺
        rect(pen, BOX_LEFT, BOX_BOTTOM, BOX_RIGHT, BOX_BOTTOM + STROKE)
    if bits & 0b0001:  # 左辺
        rect(pen, BOX_LEFT, BOX_BOTTOM, BOX_LEFT + STROKE, BOX_TOP)

def draw_voiced_mark(pen):
    mx = BOX_RIGHT + 15
    my = BOX_TOP - 10
    rect(pen, mx, my - VOICE_R * 2, mx + VOICE_R // 2, my)

def draw_vowel_triangle(pen, v):
    s = 180
    d1 = 120
    d2 = 60
    h1 = 84
    h2 = 42
    hs = 126

    if v == "u":    # 左向き ◁
        tri(pen, (CX - d1, CY), (CX + d2, CY + s), (CX + d2, CY - s))
    elif v == "o":  # 左下向き ◿
        tri(pen, (CX - h1, CY - h1), (CX + h2 + hs, CY + h2 - hs), (CX + h2 - hs, CY + h2 + hs))
    elif v == "a":  # 下向き ▽
        tri(pen, (CX, CY - d1), (CX - s, CY + d2), (CX + s, CY + d2))
    elif v == "e":  # 右下向き ◺
        tri(pen, (CX + h1, CY - h1), (CX - h2 + hs, CY + h2 + hs), (CX - h2 - hs, CY + h2 - hs))
    elif v == "i":  # 右向き ▷
        tri(pen, (CX + d1, CY), (CX - d2, CY + s), (CX - d2, CY - s))
    elif v == "q":  # 上向き △
        tri(pen, (CX, CY + d1), (CX - s, CY - d2), (CX + s, CY - d2))

# --- グリフ生成 ---
def make_empty():
    pen = TTGlyphPen(None)
    return pen.glyph()

def make_box():
    pen = TTGlyphPen(None)
    rect(pen, 200, 200, 800, 800)
    return pen.glyph()

def make_vowel_only(v):
    pen = TTGlyphPen(None)
    draw_vowel_triangle(pen, v)
    return pen.glyph()

def make_cons_only(cons):
    pen = TTGlyphPen(None)
    draw_consonant_edges(pen, consonant_to_bits[cons])
    if cons in voiced_set:
        draw_voiced_mark(pen)
    return pen.glyph()

def make_syllable(cons, v):
    pen = TTGlyphPen(None)
    draw_consonant_edges(pen, consonant_to_bits[cons])
    draw_vowel_triangle(pen, v)
    if cons in voiced_set:
        draw_voiced_mark(pen)
    return pen.glyph()

# --- グリフ・cmap 構築 ---
glyph_order = [".notdef"]
glyphs = {".notdef": make_empty()}
advance = {".notdef": (UPM, 0)}
cmap = {}

# スペース
glyph_order.append("space")
glyphs["space"] = make_empty()
advance["space"] = (UPM // 2, 0)
cmap[0x0020] = "space"

# 母音グリフ — cmap でラテン文字に直接マッピング
# 例: 'a' を打つと vowel_a (下向き三角形) が表示される
for vi, v in enumerate(vowels):
    name = f"vowel_{v}"
    glyph_order.append(name)
    glyphs[name] = make_vowel_only(v)
    advance[name] = (UPM, 0)
    cmap[ord(v)] = name                     # ラテン文字 → 母音グリフ
    cmap[PUA_BASE + vi] = name              # PUA マッピング

# 子音グリフ — 単一文字の子音はラテン文字にマッピング
# 例: 't' を打つと cons_t (上辺+左辺) が表示される
PUA_CONS_BASE = PUA_BASE + len(vowels)      # 0xE506
for ci, cons in enumerate(consOrder):
    name = f"cons_{cons}"
    glyph_order.append(name)
    glyphs[name] = make_cons_only(cons)
    advance[name] = (UPM, 0)
    if len(cons) == 1:
        cmap[ord(cons)] = name              # ラテン文字 → 子音グリフ
    cmap[PUA_CONS_BASE + ci] = name         # PUA マッピング

# nn グリフ (子音nの母音なし版)
PUA_NN = PUA_CONS_BASE + len(consOrder)     # 0xE519
glyph_order.append("cons_nn")
glyphs["cons_nn"] = make_cons_only("n")     # n と同じ形
advance["cons_nn"] = (UPM, 0)
cmap[PUA_NN] = "cons_nn"

# 音節グリフ (子音+母音)
PUA_SYLL_BASE = PUA_NN + 1                  # 0xE51A
idx = 0
for cons in consOrder:
    for v in vowels:
        name = f"syll_{cons}_{v}"
        glyph_order.append(name)
        glyphs[name] = make_syllable(cons, v)
        advance[name] = (UPM, 0)
        cmap[PUA_SYLL_BASE + idx] = name
        idx += 1

# 未使用ラテン文字 (c, r, v, y) — フォールバック用ボックス
for ch in "crvy":
    name = f"latin_{ch}"
    glyph_order.append(name)
    glyphs[name] = make_box()
    advance[name] = (UPM, 0)
    cmap[ord(ch)] = name

# --- GSUB リガチャ生成 ---
# 「ta」と打つ → cons_t + vowel_a → GSUB が syll_t_a に自動置換
fea_lines = [
    "languagesystem DFLT dflt;",
    "languagesystem latn dflt;",
    "",
    "feature liga {",
]

# 複数文字子音の定義 (cons_t + cons_x → tx系, etc.)
multi_char = [
    ("tx", "cons_t", "cons_x"),
    ("th", "cons_t", "cons_h"),
    ("ng", "cons_n", "cons_g"),
]

# (1) 3グリフ: 複数文字子音 + 母音 → 音節 (最長一致を優先するため先に記述)
for mc, g1, g2 in multi_char:
    for v in vowels:
        fea_lines.append(f"    sub {g1} {g2} vowel_{v} by syll_{mc}_{v};")

# (2) 2グリフ: 複数文字子音のみ (母音なし)
for mc, g1, g2 in multi_char:
    fea_lines.append(f"    sub {g1} {g2} by cons_{mc};")

# (3) 2グリフ: nn → 子音nの母音なし版
fea_lines.append("    sub cons_n cons_n by cons_nn;")

# (4) 2グリフ: 単一子音 + 母音 → 音節
for cons in consOrder:
    if cons in ("tx", "th", "ng"):
        continue  # 複数文字子音は (1)(2) で処理済み
    for v in vowels:
        fea_lines.append(f"    sub cons_{cons} vowel_{v} by syll_{cons}_{v};")

fea_lines.append("} liga;")
fea_code = "\n".join(fea_lines)

# LSB (Left Side Bearing) を正確に計算して左寄りを防止
for name, glyph in glyphs.items():
    if hasattr(glyph, "coordinates") and glyph.coordinates:
        xmin = int(min(pt[0] for pt in glyph.coordinates))
    else:
        xmin = 0
    advance[name] = (UPM, xmin)

# --- フォント構築 ---
fb = FontBuilder(UPM, isTTF=True)
fb.setupGlyphOrder(glyph_order)
fb.setupGlyf(glyphs)
fb.setupHorizontalMetrics(advance)
fb.setupHorizontalHeader(ascent=1000, descent=0)
fb.setupCharacterMap(cmap)
fb.setupOS2()
fb.font["OS/2"].sTypoAscender = 1000
fb.font["OS/2"].sTypoDescender = 0
fb.font["OS/2"].usWinAscent = 1000
fb.font["OS/2"].usWinDescent = 0
fb.setupNameTable({
    "familyName": "AxilengeScript",
    "styleName": "Regular",
    "fullName": "AxilengeScript Regular",
    "uniqueFontIdentifier": "AxilengeScript",
    "psName": "AxilengeScript-Regular",
})
fb.setupPost()

# GSUB テーブル追加 (リガチャ)
addOpenTypeFeaturesFromString(fb.font, fea_code)

# maxp
maxp = newTable("maxp")
maxp.tableVersion = 0x00010000
maxp.numGlyphs = len(glyph_order)
maxp.maxPoints = 200
maxp.maxContours = 100
maxp.maxCompositePoints = 0
maxp.maxCompositeContours = 0
maxp.maxZones = 1
maxp.maxTwilightPoints = 0
maxp.maxStorage = 0
maxp.maxFunctionDefs = 0
maxp.maxInstructionDefs = 0
maxp.maxStackElements = 0
maxp.maxSizeOfInstructions = 0
maxp.maxComponentElements = 0
maxp.maxComponentDepth = 0
fb.font["maxp"] = maxp

# --- 保存 ---
fb.save("font_pua.otf")
print("Generated font_pua.otf")
print(f"  母音のみ:  U+{PUA_BASE:04X}〜U+{PUA_BASE + len(vowels) - 1:04X} ({len(vowels)}個)")
print(f"  子音のみ:  U+{PUA_CONS_BASE:04X}〜U+{PUA_CONS_BASE + len(consOrder) - 1:04X} ({len(consOrder)}個)")
print(f"  nn:        U+{PUA_NN:04X}")
print(f"  音節:      U+{PUA_SYLL_BASE:04X}〜U+{PUA_SYLL_BASE + idx - 1:04X} ({idx}個)")
print(f"  GSUBリガチャ: {sum(1 for l in fea_lines if l.strip().startswith('sub '))}ルール")
print(f"  合計グリフ: {len(glyph_order)}")
