import feedparser
import json
import re
from difflib import SequenceMatcher
import os

KEYWORDS = ["보험중개", "신재생에너지", "방산"]
NEWS_PER_KEYWORD = 40
GOOGLE_NEWS_RSS = "https://news.google.com/rss/search?q={keyword}&hl=ko&gl=KR&ceid=KR:ko"

# 언론사명 추출: 제목 끝 괄호, 대괄호, 중괄호 등에서 추출
SOURCE_PATTERNS = [
    r"[\[(](.*?)[\])]$",  # (언론사), [언론사], {언론사} 등
    r"-\s*([^\-\|]+)$",   # - 언론사
    r"\|\s*([^\-\|]+)$"  # | 언론사
]

def extract_source(title):
    for pattern in SOURCE_PATTERNS:
        m = re.search(pattern, title)
        if m:
            return m.group(1).strip()
    return "Unknown"

def is_similar(a, b, threshold=0.85):
    return SequenceMatcher(None, a, b).ratio() > threshold

def deduplicate(news_list):
    deduped = []
    for item in news_list:
        if not any(item['title'] == n['title'] or is_similar(item['title'], n['title']) for n in deduped):
            deduped.append(item)
    return deduped

def fetch_news(keyword):
    url = GOOGLE_NEWS_RSS.format(keyword=keyword)
    feed = feedparser.parse(url)
    news_items = []
    for entry in feed.entries[:NEWS_PER_KEYWORD]:
        news_items.append({
            "title": entry.title,
            "link": entry.link,
            "published": entry.published if "published" in entry else None,
            "keyword": keyword
        })
    return news_items

def main():
    # 현재 스크립트 파일의 디렉토리 경로를 얻음
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # news_clipping 디렉토리 경로
    news_clipping_dir = os.path.dirname(script_dir)
    # 최종 저장될 JSON 파일 경로
    output_path = os.path.join(news_clipping_dir, "news_data.json")

    all_news = []
    for kw in KEYWORDS:
        news = fetch_news(kw)
        all_news.extend(news)
    # 중복 제거
    deduped_news = deduplicate(all_news)
    # JSON 구조화 및 source 추출
    json_news = []
    for item in deduped_news:
        json_news.append({
            "date": item["published"],
            "title": item["title"],
            "link": item["link"],
            "keyword": item["keyword"],
            "source": extract_source(item["title"])
        })
    # 웹에서 읽기 쉬운 JSON 저장
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(json_news, f, ensure_ascii=False, indent=2)
    print(f"\n총 {len(json_news)}건의 뉴스가 {output_path}에 저장되었습니다.")

if __name__ == "__main__":
    main() 