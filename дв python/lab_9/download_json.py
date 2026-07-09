"""
Програма завантажує JSON з вказаного URL і зберігає у файл.

python download_json.py https://jsonplaceholder.typicode.com/posts posts.json
"""
import sys
import json

def download_with_requests(url):
    import requests
    r = requests.get(url, timeout=20)
    r.raise_for_status()
    return r.text

def download_with_urllib(url):
    from urllib.request import urlopen, Request
    req = Request(url, headers={'User-Agent': 'python-urllib/3'})
    with urlopen(req, timeout=20) as resp:
        return resp.read().decode('utf-8')

def main():
    if len(sys.argv) < 3:
        print("Usage: python download_json.py <URL> <output_filename>")
        sys.exit(1)
    url = sys.argv[1]
    outfn = sys.argv[2]
    try:
        try:
            text = download_with_requests(url)
        except Exception:
            text = download_with_urllib(url)
    except Exception as e:
        print("Error downloading:", e)
        sys.exit(2)
    # optionally validate JSON
    try:
        js = json.loads(text)
    except Exception as e:
        print("Warning: downloaded content is not valid JSON:", e)
        # still save raw
        with open(outfn, 'w', encoding='utf-8') as f:
            f.write(text)
        print("Saved raw content to", outfn)
        sys.exit(0)
    with open(outfn, 'w', encoding='utf-8') as f:
        json.dump(js, f, indent=2, ensure_ascii=False)
    print("Saved JSON to", outfn)

if __name__ == "__main__":
    main()