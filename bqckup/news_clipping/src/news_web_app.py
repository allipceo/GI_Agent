from flask import Flask, render_template_string, jsonify
from auto_dashboard_generator import DashboardGenerator
from datetime import datetime
import threading
import time

app = Flask(__name__)

# 전역 상태 관리
class CollectionStatus:
    def __init__(self):
        self.is_collecting = False
        self.last_collection = None
        self.message = ""

status = CollectionStatus()

# HTML 템플릿
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GI Agent 뉴스 대시보드</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        .card { margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .card-energy .card-header { background-color: #28a745; color: white; }
        .card-defense .card-header { background-color: #007bff; color: white; }
        .card-insurance .card-header { background-color: #fd7e14; color: white; }
        .news-item { padding: 8px 0; border-bottom: 1px solid #eee; }
        .news-item:last-child { border-bottom: none; }
        .news-date { color: #666; font-size: 0.9em; }
        .total-count { font-size: 1.2em; font-weight: bold; color: #333; padding: 15px; background-color: #f8f9fa; border-radius: 5px; margin-top: 20px; }
        #status-message { transition: all 0.3s ease; }
        .collecting { color: #007bff; }
        .success { color: #28a745; }
        .error { color: #dc3545; }
    </style>
</head>
<body class="bg-light">
    <div class="container py-4">
        <header class="pb-3 mb-4 border-bottom">
            <div class="d-flex align-items-center justify-content-between">
                <div>
                    <h1 class="display-5 fw-bold">GI Agent 뉴스 대시보드</h1>
                    <p id="status-message" class="text-muted">
                        {% if last_collection %}
                            마지막 수집: {{ last_collection }}
                        {% else %}
                            수집 대기 중...
                        {% endif %}
                    </p>
                </div>
                <button id="refreshBtn" class="btn btn-primary" onclick="refreshNews()">
                    <span id="refreshIcon" class="bi bi-arrow-clockwise"></span> 새로고침
                </button>
            </div>
        </header>

        <div id="dashboard-content">
            {{ dashboard_content|safe }}
        </div>
    </div>

    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.7.2/font/bootstrap-icons.css">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        function updateStatus() {
            fetch('/status')
                .then(response => response.json())
                .then(data => {
                    const statusMsg = document.getElementById('status-message');
                    const refreshBtn = document.getElementById('refreshBtn');
                    
                    if (data.is_collecting) {
                        statusMsg.textContent = '뉴스 수집 중...';
                        statusMsg.className = 'collecting';
                        refreshBtn.disabled = true;
                    } else {
                        statusMsg.textContent = '마지막 수집: ' + data.last_collection;
                        statusMsg.className = 'success';
                        refreshBtn.disabled = false;
                    }
                });
        }

        function refreshNews() {
            const refreshBtn = document.getElementById('refreshBtn');
            refreshBtn.disabled = true;
            
            fetch('/refresh')
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'started') {
                        // 상태 확인 시작
                        const checkStatus = setInterval(() => {
                            fetch('/status')
                                .then(response => response.json())
                                .then(statusData => {
                                    if (!statusData.is_collecting) {
                                        clearInterval(checkStatus);
                                        location.reload();
                                    }
                                });
                        }, 1000);
                    }
                });
        }

        // 페이지 로드 시 상태 확인
        updateStatus();
    </script>
</body>
</html>
'''

def collect_news_async():
    """비동기로 뉴스를 수집합니다."""
    try:
        status.is_collecting = True
        generator = DashboardGenerator()
        generator.collect_news()
        generator.generate_dashboard()
        status.last_collection = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        status.message = "수집 완료"
    except Exception as e:
        status.message = f"수집 실패: {str(e)}"
    finally:
        status.is_collecting = False

@app.route('/')
def index():
    """메인 대시보드 페이지를 표시합니다."""
    try:
        with open('news_clipping/output/auto_dashboard.html', 'r', encoding='utf-8') as f:
            dashboard_content = f.read()
            # 본문 내용만 추출
            content_start = dashboard_content.find('<div class="row">')
            content_end = dashboard_content.find('</div>\n\n    <!-- Bootstrap Icons -->')
            if content_start != -1 and content_end != -1:
                dashboard_content = dashboard_content[content_start:content_end]
    except Exception:
        dashboard_content = '<p class="text-center text-muted">대시보드를 불러올 수 없습니다.</p>'

    return render_template_string(
        HTML_TEMPLATE,
        dashboard_content=dashboard_content,
        last_collection=status.last_collection
    )

@app.route('/refresh')
def refresh():
    """뉴스 수집을 시작합니다."""
    if not status.is_collecting:
        thread = threading.Thread(target=collect_news_async)
        thread.start()
        return jsonify({'status': 'started'})
    return jsonify({'status': 'already_running'})

@app.route('/status')
def get_status():
    """현재 수집 상태를 반환합니다."""
    return jsonify({
        'is_collecting': status.is_collecting,
        'last_collection': status.last_collection,
        'message': status.message
    })

if __name__ == '__main__':
    # 초기 뉴스 수집
    if not status.last_collection:
        collect_news_async()
        while status.is_collecting:
            time.sleep(1)
    
    # 서버 실행
    print("🌐 웹 서버 시작 - http://localhost:5000")
    app.run(host='0.0.0.0', port=5000) 