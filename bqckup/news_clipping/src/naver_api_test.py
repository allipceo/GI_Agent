import json
import requests
from pathlib import Path
from datetime import datetime

def load_api_config():
    """Load API configuration from config file."""
    try:
        config_path = Path(__file__).parent.parent / 'config' / 'api_config.json'
        print("📂 Loading API configuration...")
        
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        print("✓ API configuration loaded successfully")
        return config['naver_news']
    except Exception as e:
        print(f"❌ Error loading API configuration: {str(e)}")
        raise

def test_naver_api():
    """Test Naver News API connection with basic search."""
    # Load API credentials
    api_config = load_api_config()
    
    # API endpoint
    url = "https://openapi.naver.com/v1/search/news.json"
    
    # Request headers
    headers = {
        "X-Naver-Client-Id": api_config['client_id'],
        "X-Naver-Client-Secret": api_config['client_secret']
    }
    
    # Search parameters
    params = {
        "query": "신재생에너지",
        "display": 5,
        "sort": "date"
    }
    
    try:
        print("\n🔍 Testing API with search query '신재생에너지'...")
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        # Parse results
        results = response.json()
        
        print("✓ API connection successful")
        print(f"✓ Found {results['total']} total results")
        print("\n📰 Latest 5 News Articles:")
        print("-" * 80)
        
        for idx, item in enumerate(results['items'], 1):
            # Clean the title by removing HTML tags
            title = item['title'].replace('<b>', '').replace('</b>', '')
            
            # Format the date
            pub_date = datetime.strptime(item['pubDate'], '%a, %d %b %Y %H:%M:%S +0900')
            date_str = pub_date.strftime('%Y-%m-%d %H:%M')
            
            print(f"\n[{idx}] {title}")
            print(f"📅 Published: {date_str}")
            print(f"🔗 Link: {item['link']}")
            print("-" * 80)
            
    except requests.exceptions.RequestException as e:
        print(f"❌ API Request Error: {str(e)}")
        raise
    except json.JSONDecodeError as e:
        print(f"❌ JSON Parsing Error: {str(e)}")
        raise
    except Exception as e:
        print(f"❌ Unexpected Error: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        print("🚀 Starting Naver News API Test...")
        test_naver_api()
        print("\n✨ Test completed successfully!")
    except Exception as e:
        print("\n❌ Test failed. Please check the error messages above.") 