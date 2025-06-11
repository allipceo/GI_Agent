import json
from datetime import datetime
from pathlib import Path

def parse_news_file():
    news_data = {
        'energy': [], 
        'defense': [], 
        'insurance': [], 
        'lastUpdate': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    current_category = None
    
    input_file = Path(__file__).parent.parent / 'output' / 'multi_news_results.txt'
    output_dir = Path(__file__).parent.parent.parent / 'docs' / 'data'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            if line.startswith('=== '):
                category = line.split(' ')[1]
                if category == '에너지':
                    current_category = 'energy'
                elif category == '방산':
                    current_category = 'defense'
                elif category == '보험':
                    current_category = 'insurance'
            elif line.startswith('- '):
                if current_category:
                    title_date = line[2:].rsplit(' (', 1)
                    if len(title_date) == 2:
                        title, date = title_date
                        date = date.rstrip(')')
                        news_data[current_category].append({
                            'title': title,
                            'date': date
                        })
    
    output_file = output_dir / 'news_data.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(news_data, f, ensure_ascii=False, indent=2)
    
    print(f"✨ JSON 데이터 생성 완료: {output_file}")

if __name__ == '__main__':
    parse_news_file() 