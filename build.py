from fontTools.ttLib import TTFont
import fontTools.subset as subset
import copy

HIRAGANA_TO_KATAKANA = {"ぁ":"ァ","あ":"ア","ぃ":"ィ","い":"イ","ぅ":"ゥ","う":"ウ","ぇ":"ェ","え":"エ","ぉ":"ォ","お":"オ","か":"カ","が":"ガ","き":"キ","ぎ":"ギ","く":"ク","ぐ":"グ","け":"ケ","げ":"ゲ","こ":"コ","ご":"ゴ","さ":"サ","ざ":"ザ","し":"シ","じ":"ジ","す":"ス","ず":"ズ","せ":"セ","ぜ":"ゼ","そ":"ソ","ぞ":"ゾ","た":"タ","だ":"ダ","ち":"チ","ぢ":"ヂ","っ":"ッ","つ":"ツ","づ":"ヅ","て":"テ","で":"デ","と":"ト","ど":"ド","な":"ナ","に":"ニ","ぬ":"ヌ","ね":"ネ","の":"ノ","は":"ハ","ば":"バ","ぱ":"パ","ひ":"ヒ","び":"ビ","ぴ":"ピ","ふ":"フ","ぶ":"ブ","ぷ":"プ","へ":"ヘ","べ":"ベ","ぺ":"ペ","ほ":"ホ","ぼ":"ボ","ぽ":"ポ","ま":"マ","み":"ミ","む":"ム","め":"メ","も":"モ","ゃ":"ャ","や":"ヤ","ゅ":"ュ","ゆ":"ユ","ょ":"ョ","よ":"ヨ","ら":"ラ","り":"リ","る":"ル","れ":"レ","ろ":"ロ","ゎ":"ヮ","わ":"ワ","ゐ":"ヰ","ゑ":"ヱ","を":"ヲ","ん":"ン","ゔ":"ヴ","ゕ":"ヵ","ゖ":"ヶ"} # fmt: skip
FONT_SOURCE = "NotoSansJP-VariableFont_wght.ttf"
FONT_OUTPUT = "NotoSansJPAllKatakana.ttf"


def glyph_name(glyph: str) -> str:
    return f"uni{hex(ord(glyph))[2:].upper()}"


def main():
    font = TTFont(FONT_SOURCE)
    glyf, gvar, name, hmtx = font["glyf"], font["gvar"], font["name"], font["hmtx"]

    wanted_glyphs = set()
    for hiragana, katakana in HIRAGANA_TO_KATAKANA.items():
        ghiragana, gkatakana = glyph_name(hiragana), glyph_name(katakana)
        wanted_glyphs.add(ghiragana)
        glyf[ghiragana] = copy.deepcopy(glyf[gkatakana])
        gvar.variations[ghiragana] = copy.deepcopy(gvar.variations[gkatakana])
        hmtx.metrics[ghiragana] = hmtx.metrics[gkatakana]

    subsetter = subset.Subsetter(subset.Options())
    subsetter.populate(glyphs={*wanted_glyphs})
    subsetter.subset(font)

    for name_record in name.names:
        name_record.string = name_record.string.replace(
            "Noto Sans JP".encode("utf-16-be"),
            "Noto Sans JP All Katakana".encode("utf-16-be"),
        ).replace(
            "NotoSansJP".encode("utf-16-be"),
            "NotoSansJPAllKatakana".encode("utf-16-be"),
        )

    font.save(FONT_OUTPUT)


if __name__ == "__main__":
    main()
