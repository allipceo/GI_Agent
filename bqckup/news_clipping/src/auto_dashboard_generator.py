import os
from pathlib import Path
from datetime import datetime
from multi_keyword_collector import MultiKeywordCollector

class DashboardGenerator:
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.output_dir = self.base_dir / 'output'
        self.template_path = self.output_dir / 'news_dashboard.html'
        self.output_path = self.output_dir / 'auto_dashboard.html'
        
    def collect_news(self):
        """뉴스를 수집하고 결과를 반환합니다."""
        print("🔍 뉴스 수집 중...")
        collector = MultiKeywordCollector()
        news_data = collector.collect_news()
        return news_data
        
    def read_template(self):
        """HTML 템플릿을 읽어옵니다."""
        try:
            with open(self.template_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"❌ 템플릿 읽기 실패: {str(e)}")
            return None

    def parse_news_data(self):
        """수집된 뉴스 데이터를 파싱합니다."""
        news_data = {'에너지': [], '방산': [], '보험': [], 'total': 0}
        
        try:
            with open(self.output_dir / 'multi_news_results.txt', 'r', encoding='utf-8') as f:
                current_category = None
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                        
                    if line.startswith('=== '):
                        # 카테고리 라인 파싱
                        category = line.split(' ')[1]
                        current_category = category
                    elif line.startswith('- '):
                        # 뉴스 항목 파싱
                        if current_category:
                            title_date = line[2:].rsplit(' (', 1)
                            if len(title_date) == 2:
                                title, date = title_date
                                date = date.rstrip(')')
                                news_data[current_category].append({
                                    'title': title,
                                    'date': date
                                })
                    elif line.startswith('총 수집:'):
                        # 총계 파싱
                        news_data['total'] = int(line.split(' ')[2].rstrip('건'))
                        
        except Exception as e:
            print(f"❌ 뉴스 데이터 파싱 실패: {str(e)}")
            
        return news_data

    def generate_news_items_html(self, news_list):
        """뉴스 항목들의 HTML을 생성합니다."""
        if not news_list:
            return '<p class="text-muted">수집된 뉴스가 없습니다.</p>'
            
        items_html = []
        for news in news_list:
            items_html.append(f'''
                <div class="news-item">
                    <div class="news-title">{news['title']}</div>
                    <div class="news-date">{news['date']}</div>
                </div>
            ''')
        return '\n'.join(items_html)

    def generate_dashboard(self):
        """대시보드 HTML을 생성합니다."""
        print("\n📊 대시보드 생성 중...")
        
        # 템플릿 읽기
        template = self.read_template()
        if not template:
            return False
            
        # 뉴스 데이터 파싱
        news_data = self.parse_news_data()
        
        # 카테고리별 뉴스 항목 HTML 생성
        replacements = {}
        for category in ['에너지', '방산', '보험']:
            count = len(news_data[category])
            news_html = self.generate_news_items_html(news_data[category])
            
            # 카테고리 제목 교체
            replacements[f'<h4 class="my-0">{category} 분야'] = \
                f'<h4 class="my-0">{category} 분야 ({count}건)'
            
            # 카테고리 내용 교체
            if category == '에너지':
                replacements['<div class="news-item">\n                            <div class="news-title">"영농형 태양광은'] = \
                    news_html.strip()
            elif category == '방산':
                replacements['<p class="text-muted">수집된 뉴스가 없습니다.</p>'] = news_html
            elif category == '보험':
                replacements['<p class="text-muted">수집된 뉴스가 없습니다.</p>'] = news_html
        
        # 총계 교체
        replacements['총 수집: 4건'] = f'총 수집: {news_data["total"]}건'
        
        # 생성 시간 추가
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        replacements['최신 뉴스 클리핑 결과'] = f'최신 뉴스 클리핑 결과 (생성: {current_time})'
        
        # 모든 교체 수행
        new_html = template
        for old, new in replacements.items():
            new_html = new_html.replace(old, new)
        
        # 새로운 대시보드 파일 저장
        try:
            with open(self.output_path, 'w', encoding='utf-8') as f:
                f.write(new_html)
            print(f"✨ 대시보드 생성 완료: {self.output_path}")
            return True
        except Exception as e:
            print(f"❌ 대시보드 저장 실패: {str(e)}")
            return False

def main():
    generator = DashboardGenerator()
    
    # 1. 뉴스 수집
    generator.collect_news()
    
    # 2. 대시보드 생성
    if generator.generate_dashboard():
        # 3. 브라우저에서 열기
        os.startfile(generator.output_path)

if __name__ == "__main__":
    main() 