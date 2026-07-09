"""
Реалізація трьох задач для posts.json .
Функції:
 - top_users(posts, top_n=5)
 - length_stats(posts, top_n_bodies=10)
 - keyword_analysis(posts, keywords, top_n_words=20)

python tasks_solutions_posts.py posts.json (щоб вивести в термінал)
або
python tasks_solutions_posts.py posts.json > results_posts.txt (щоб зберегти в файл)
"""
import sys, json, re
from collections import defaultdict, Counter
from typing import List, Dict, Any

# simple set of English stop-words for filtering
STOPWORDS = set([
    "a","the","and","in","of","to","is","it","for","on","that","this","with",
    "as","are","was","but","be","by","an","or","at","from","i","you","he","she",
    "they","we","his","her","its","have","has","had","not","their","them"
])

# token regex: letters and digits and apostrophe (supports latin and cyrillic letters)
TOKEN_RE = re.compile(r"\b[а-яА-ЯёЁa-zA-Z0-9']+\b", re.UNICODE)

def load_posts(fn: str) -> List[Dict[str, Any]]:
    """Load a JSON file and return the list of posts."""
    with open(fn, 'r', encoding='utf-8') as f:
        return json.load(f)

def top_users(posts: List[Dict[str, Any]], top_n=5):
    """Task 1: Count posts per userId and return top-N users.
    
    Returns a list of tuples: (userId, post_count, sorted_list_of_post_ids).
    """
    counts = defaultdict(list)  # userId -> list of post ids
    for p in posts:
        uid = p.get('userId')
        pid = p.get('id')
        counts[uid].append(pid)
    counts_summary = [(uid, len(ids), sorted(ids)) for uid, ids in counts.items()]
    counts_summary.sort(key=lambda x: x[1], reverse=True)
    return counts_summary[:top_n]

def length_stats(posts: List[Dict[str, Any]], top_n_bodies=10):
    """Task 2:
    - For each userId: compute average length of title and average length of body.
    - Return top N posts by body length.
    
    Returns (user_stats, top_bodies) where:
      user_stats: dict userId -> {avg_title_len, avg_body_len, posts_count}
      top_bodies: list of dicts with keys: id, userId, body_len, title
    """
    by_user = defaultdict(lambda: {'title_total':0, 'body_total':0, 'count':0})
    body_lengths = []
    for p in posts:
        uid = p.get('userId')
        title = p.get('title') or ""
        body = p.get('body') or ""
        by_user[uid]['title_total'] += len(title)
        by_user[uid]['body_total'] += len(body)
        by_user[uid]['count'] += 1
        body_lengths.append((len(body), p.get('id'), uid, title))
    # compute averages per user
    user_stats = {}
    for uid, v in sorted(by_user.items()):
        cnt = v['count'] or 1
        user_stats[uid] = {
            'avg_title_len': round(v['title_total'] / cnt, 2),
            'avg_body_len': round(v['body_total'] / cnt, 2),
            'posts_count': cnt
        }
    # sort posts by body length descending and prepare top list
    body_lengths.sort(reverse=True)
    top_bodies = [{'id': pid, 'userId': uid, 'body_len': bl, 'title': title}
                  for bl, pid, uid, title in body_lengths[:top_n_bodies]]
    return user_stats, top_bodies

def tokenize(text: str):
    """Simple tokenizer — returns list of lowercase tokens without punctuation."""
    return [t.lower() for t in TOKEN_RE.findall(text)]

def keyword_analysis(posts: List[Dict[str, Any]], keywords: List[str], top_n_words=20):
    """Task 3:
    - Build a frequency dictionary over title+body text,
    - Return top-N words (excluding stop-words),
    - For each keyword, return a list of post ids where the word appears.

    Token matching is case-insensitive and uses simple tokenization.
    """
    freq = Counter()
    keyword_map = {k.lower(): [] for k in keywords}
    for p in posts:
        pid = p.get('id')
        text = ((p.get('title') or "") + " " + (p.get('body') or ""))
        tokens = tokenize(text)
        freq.update(tokens)
        token_set = set(tokens)
        for k in keyword_map.keys():
            if k in token_set:
                keyword_map[k].append(pid)
    # remove stopwords from frequency counter and build top list
    for w in list(freq.keys()):
        if w in STOPWORDS:
            del freq[w]
    top_words = freq.most_common(top_n_words)
    return top_words, keyword_map

def main():
    if len(sys.argv) < 2:
        print("Usage: python tasks_solutions_posts.py posts.json")
        return
    fn = sys.argv[1]
    posts = load_posts(fn)
    print("=== Task 1: Top users by number of posts ===")
    for uid, cnt, ids in top_users(posts, top_n=5):
        print(f"userId={uid} | posts={cnt} | ids={ids}")
    print("\n=== Task 2: Statistics of title and body lengths ===")
    user_stats, top_bodies = length_stats(posts, top_n_bodies=10)
    print("User statistics (userId: avg_title_len, avg_body_len, posts_count):")
    for uid, stats in sorted(user_stats.items()):
        print(f"  {uid}: {stats['avg_title_len']}, {stats['avg_body_len']}, {stats['posts_count']}")
    print("\nTop posts by body length:")
    for item in top_bodies:
        print(f"  id={item['id']} userId={item['userId']} body_len={item['body_len']} title={item['title'][:60]!r}")
    print("\n=== Task 3: Frequency analysis and keyword search ===")
    keywords = ["qui", "et", "sunt"]  # example keywords
    top_words, keyword_map = keyword_analysis(posts, keywords, top_n_words=20)
    print("Top words:")
    for w,c in top_words:
        print(f"  {w}: {c}")
    print("\nPosts containing keywords:")
    for k, ids in keyword_map.items():
        print(f"  '{k}': {sorted(ids)}")

if __name__ == '__main__':
    main()