from pathlib import Path
import yaml

MARKER = "CD10"

def load_notes(folder="notes"):
    diseases = []
    for path in Path(folder).glob("*.md"):
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---"):
            print(f"フロントマターなし: {path}")
            continue
        _, front, body = text.split("---", 2)
        data = yaml.safe_load(front)
        data["memo"] = body.strip()
        diseases.append(data)
    return diseases

if __name__ == "__main__":
    for d in load_notes():
        if MARKER in d.get("ihc_positive", []):
            print(d["disease"])