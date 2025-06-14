import feedparser
from urllib.parse import quote
from datetime import datetime
import os

TEMPLATE_PATH = "news_dashboard.html"
OUTPUT_PATH = "auto_dashboard.html"

CATEGORY_KEYWORDS = {
    '에너지': [
        '에너지 관련 보험 시장 현황',
        '국가 에너지 발전 기본계획 방향',
        '신재생에너지 현황 및 전망',
        '풍력발전소 건설 현황 및 전망'
    ],
    '방산': [
        '방산업 관련 보험 시장 현황',
        '방산업 현황 및 전망',
        '방위력 개선 개발예산 관련',
        '방위사업청 관련',
        '방산업 수출 현황'
    ],
    '보험': [
        '보험중개 시장 현황',
        '보험상품 현황',
        '재보험 시장 현황'
    ]
}

def fetch_google_news(keyword, max_items=5):
    encoded_keyword = quote(keyword)
    url = f"https://news.google.com/rss/search?q={encoded_keyword}&hl=ko&gl=KR&ceid=KR:ko"
    feed = feedparser.parse(url)
    return feed.entries[:max_items]

def make_news_html(news_items):
    if not news_items:
        return '<p class="text-muted">수집된 뉴스가 없습니다.</p>'
    html = []
    for item in news_items:
        html.append(f'<div class="news-title">{item.title}</div>')
        html.append(f'<div class="news-date">{item.published}</div>')
    return '<div>' + '</div><div style="margin-bottom:10px;"></div>'.join(html) + '</div>'

def main():
    category_results = {'에너지': [], '방산': [], '보험': []}
    total_count = 0
    for category, keywords in CATEGORY_KEYWORDS.items():
        news_items = []
        for keyword in keywords:
            items = fetch_google_news(keyword, max_items=2)
            news_items.extend(items)
        category_results[category] = news_items
        total_count += len(news_items)

    # 템플릿 읽기
    with open(TEMPLATE_PATH, encoding='utf-8') as f:
        template = f.read()

    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    html = template.format(
        update_time=now,
        energy_count=len(category_results['에너지']),
        defense_count=len(category_results['방산']),
        insurance_count=len(category_results['보험']),
        energy_news=make_news_html(category_results['에너지']),
        defense_news=make_news_html(category_results['방산']),
        insurance_news=make_news_html(category_results['보험']),
        total_count=total_count
    )

    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"✨ 대시보드 생성 완료: {OUTPUT_PATH}")
    try:
        os.startfile(OUTPUT_PATH)
    except Exception:
        pass

if __name__ == "__main__":
    main() 