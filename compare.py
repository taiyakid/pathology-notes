import sys
import pandas as pd
from load_notes import load_notes

FIELDS = [
    ("growth_pattern", "組織構築"),
    ("cytology", "細胞像"),
    ("background", "背景"),
    ("ihc_positive", "IHC 陽性"),
    ("ihc_negative", "IHC 陰性"),
    ("ihc_variable", "IHC 一定しない"),
    ("ihc_notes", "IHC 補足"),
    ("genetics", "遺伝子異常"),
    ("differential", "鑑別"),
    ("pitfalls", "注意点"),
]

def find_disease(disease, keyword):
    hits = [d for d in disease if keyword in d["disease"]]
    if len(hits) != 1:
        sys.exit(f"「{keyword}」に一致する疾患が{len(hits)}件でした。名前の一部を見直してください。")
    return hits[0]

def to_text(key, value):
    if not value:
        return "-"
    if key == "pitfalls":
        return "¥n".join(f"・{v}" for v in value)
    if isinstance(value, list):
        return "、".join(value)
    return value

def print_marker_diff(a, b):
    pa = set(a.get("ihc_positive", []))
    pb = set(b.get("ihc_positive", []))
    print(f"両方陽性: {'、'.join(sorted(pa & pb)) or '-'}")
    print(f"{a['disease']}のみ陽性: {'、'.join(sorted(pa - pb)) or '-'}")
    print(f"{b['disease']}のみ陽性: {'、'.join(sorted(pb - pa)) or '-'}")

def build_table(selected):
    rows = {label: [to_text(key, d.get(key)) for d in selected] for key, label in FIELDS}
    return pd.DataFrame(rows, index=[d["disease"] for d in selected]).T

def save_html(df, path="comparison.html"):
    style = (
        "<style>"
        "body{font-family:sans-serif;margin:2em}"
        "table{border-collapse:collapse}"
        "th,td{border:1px solid #999;padding:6px 10px;vertical-align:top;white-space:pre-wrap}"
        "th{background:#f0f0f0}"
        "</style>"
    )
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"<meta charset='utf-8'>{style}{df.to_html()}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit("使い方: python3 compare.py 疾患名の一部 疾患名の一部 [...]")
    diseases = load_notes()
    selected = [find_disease(diseases, k) for k in sys.argv[1:]]
    if len(selected) == 2:
        print_marker_diff(*selected)
    save_html(build_table(selected))
    print("comparison.html を作成しました")