import feedparser
import json
from datetime import datetime
from pathlib import Path
import re

class RSSNewsCollector:
    def __init__(self):
        # RSS 피드 URL 목록
        self.rss_feeds = {
            "연합뉴스_경제": "https://www.yonhapnewstv.co.kr/category/news/economy/feed/",
            "한국경제_산업": "https://rss.hankyung.com/feed/economy.xml",
            "이투뉴스_에너지": "http://www.e2news.com/rss/allArticle.xml"
        }
        
        # 키워드 필터
        self.keywords = {
            "energy": ["신재생에너지", "태양광", "풍력", "ESS", "에너지정책", "RE100"],
            "defense": ["방위산업", "K-방산", "한화시스템", "LIG넥스원", "KAI", "방산수출"],
            "insurance": ["보험중개사", "보험상품", "재보험", "IFRS17", "인슈어테크"]
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

    def matches_keywords(self, text):
        """텍스트가 키워드 필터와 일치하는지 확인합니다."""
        for category, keywords in self.keywords.items():
            for keyword in keywords:
                if keyword in text:
                    return True, category
        return False, None

    def clean_html(self, text):
        """HTML 태그를 제거합니다."""
        clean = re.compile('<.*?>')
        return re.sub(clean, '', text)

    def collect_news(self):
        """모든 RSS 피드에서 뉴스를 수집하고 필터링합니다."""
        collected_news = []
        
        print("🔍 뉴스 수집 시작...")
        
        for source, feed_url in self.rss_feeds.items():
            print(f"\n📰 {source} 피드 수집 중...")
            entries = self.fetch_rss_feed(feed_url)
            
            for entry in entries:
                title = self.clean_html(entry.title)
                matches, category = self.matches_keywords(title)
                
                if matches:
                    news_item = {
                        "title": title,
                        "link": entry.link,
                        "published": entry.get('published', ''),
                        "summary": self.clean_html(entry.get('summary', '')),
                        "source": source,
                        "category": category
                    }
                    collected_news.append(news_item)
        
        # 결과 저장
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = self.output_dir / f"news_collection_{timestamp}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(collected_news, f, ensure_ascii=False, indent=2)
        
        print(f"\n✨ 수집 완료! 총 {len(collected_news)}건의 뉴스 수집")
        print(f"📁 저장 위치: {output_file}")
        
        return collected_news

if __name__ == "__main__":
    collector = RSSNewsCollector()
    collector.collect_news() 