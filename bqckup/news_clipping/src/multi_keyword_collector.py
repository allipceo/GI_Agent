import feedparser
import json
from datetime import datetime
from pathlib import Path
import re

class MultiKeywordCollector:
    def __init__(self):
        # RSS 피드 URL 목록
        self.rss_feeds = {
            "연합뉴스_경제": "https://www.yonhapnewstv.co.kr/category/news/economy/feed/",
            "한국경제_산업": "https://rss.hankyung.com/feed/economy.xml",
            "이투뉴스_에너지": "http://www.e2news.com/rss/allArticle.xml"
        }
        
        # 카테고리별 키워드 필터
        self.categories = {
            "에너지": ["신재생에너지", "태양광", "풍력", "ESS"],
            "방산": ["방위산업", "K-방산", "한화시스템", "방산수출"],
            "보험": ["보험중개", "보험상품", "재보험"]
        }
        
        # 결과 저장 경로
        self.output_dir = Path(__file__).parent.parent / 'output'
        self.output_dir.mkdir(exist_ok=True)

    def fetch_rss_feed(self, feed_url):
        """RSS 피드에서 뉴스 기사를 가져옵니다."""
        try:
            feed = feedparser.parse(feed_url)
            return feed.entries
        except Exception as e:
            print(f"❌ RSS 피드 수집 오류 ({feed_url}): {str(e)}")
            return []

    def matches_category(self, text):
        """텍스트가 어떤 카테고리의 키워드와 일치하는지 확인합니다."""
        for category, keywords in self.categories.items():
            for keyword in keywords:
                if keyword in text:
                    return True, category
        return False, None

    def clean_html(self, text):
        """HTML 태그를 제거합니다."""
        clean = re.compile('<.*?>')
        return re.sub(clean, '', text)

    def format_date(self, date_str):
        """날짜 형식을 간단하게 변환합니다."""
        try:
            date_obj = datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S %z")
            return date_obj.strftime("%Y-%m-%d")
        except:
            return date_str

    def collect_news(self):
        """모든 RSS 피드에서 뉴스를 수집하고 카테고리별로 분류합니다."""
        categorized_news = {category: [] for category in self.categories.keys()}
        
        print("🔍 뉴스 수집 시작...")
        
        for source, feed_url in self.rss_feeds.items():
            print(f"\n📰 {source} 피드 수집 중...")
            entries = self.fetch_rss_feed(feed_url)
            
            for entry in entries:
                title = self.clean_html(entry.title)
                matches, category = self.matches_category(title)
                
                if matches:
                    news_item = {
                        "title": title,
                        "date": self.format_date(entry.get('published', '')),
                        "link": entry.link,
                        "source": source
                    }
                    categorized_news[category].append(news_item)
        
        # 결과를 파일로 저장
        output_file = self.output_dir / "multi_news_results.txt"
        total_count = 0
        
        with open(output_file, 'w', encoding='utf-8') as f:
            for category, news_list in categorized_news.items():
                count = len(news_list)
                total_count += count
                
                f.write(f"\n=== {category} 분야 ({count}건) ===\n")
                print(f"\n=== {category} 분야 ({count}건) ===")
                
                for news in news_list:
                    line = f"- {news['title']} ({news['date']})\n"
                    f.write(line)
                    print(line.strip())
            
            f.write(f"\n총 수집: {total_count}건\n")
            print(f"\n✨ 총 수집: {total_count}건")
            print(f"📁 저장 위치: {output_file}")

if __name__ == "__main__":
    collector = MultiKeywordCollector()
    collector.collect_news() 