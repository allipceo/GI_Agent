import json
import random
from datetime import datetime, timedelta

with open('news_data.json', encoding='utf-8') as f:
    data = json.load(f)

result = []
categories = ['보험중개', '신재생에너지', '방산']
for cat in categories:
    cat_items = [item for item in data if item['keyword'] == cat]
    # 복제해서 40개로 맞추기
    while len(cat_items) < 40:
        base = random.choice(cat_items)
        idx = len(cat_items) + 1
        new_item = base.copy()
        # 날짜, 제목, 링크 일부 변경
        new_item['date'] = (datetime.now() - timedelta(days=idx)).strftime('%a, %d %b %Y %H:%M:%S GMT')
        new_item['title'] = f"{base['title']} (더미{idx})"
        new_item['link'] = base['link'] + f"&dummy={idx}"
        cat_items.append(new_item)
    result.extend(cat_items[:40])

with open('news_data.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)