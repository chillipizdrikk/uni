"""
Швидке дослідження структури.
Виводить:
 - попередній перегляд сирого тексту,
 - типи та кількість елементів,
 - приклад першого елемента (pretty print).

python explore_json_posts.py posts.json (щоб вивести в термінал)
або
python explore_json_posts.py posts.json > explore_output_posts.txt (щоб зберегти в файл)
"""
import sys, json

def preview_raw(fn, chars=800):
    print("---- RAW PREVIEW (first {} chars) ----".format(chars))
    with open(fn, 'r', encoding='utf-8') as f:
        s = f.read()
    print(s[:chars])
    if len(s) > chars:
        print("... (truncated)")

def show_structure(fn):
    with open(fn, 'r', encoding='utf-8') as f:
        data = json.load(f)
    print("\nTop-level type:", type(data).__name__)
    if isinstance(data, list):
        print("Number of items:", len(data))
        if data:
            print("\nKeys of first item:", list(data[0].keys()))
            print("\nFirst item (pretty):")
            print(json.dumps(data[0], indent=2, ensure_ascii=False))
    elif isinstance(data, dict):
        print("Keys:", list(data.keys())[:50])
        print("Pretty:")
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        print("Unexpected top-level type.")
    return data

def main():
    if len(sys.argv) < 2:
        print("Usage: python explore_json_posts.py posts.json")
        return
    fn = sys.argv[1]
    preview_raw(fn)
    data = show_structure(fn)
    # simple summary of fields if list of dicts
    if isinstance(data, list) and data and isinstance(data[0], dict):
        counts = {k:0 for k in data[0].keys()}
        for item in data:
            for k in counts.keys():
                if k in item and item[k] is not None:
                    counts[k] += 1
        print("\nField presence counts (top-level keys):")
        for k,v in counts.items():
            print(f"  {k}: {v}/{len(data)}")
    print("\nDone.")

if __name__ == '__main__':
    main()