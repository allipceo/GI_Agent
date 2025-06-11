// 뉴스 데이터 로드
async function loadNewsData() {
    try {
        const response = await fetch('data/news_data.json');
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('뉴스 데이터 로드 실패:', error);
        return null;
    }
}

// 뉴스 항목 HTML 생성
function generateNewsItemHtml(news) {
    return `
        <div class="news-item">
            <div class="news-title">${news.title}</div>
            <div class="news-date">${news.date}</div>
        </div>
    `;
}

// 카테고리별 뉴스 표시
function displayCategoryNews(category, newsList) {
    const titleElement = document.getElementById(`${category}Title`);
    const contentElement = document.getElementById(`${category}Content`);
    
    titleElement.textContent = `${getCategoryName(category)} 분야 (${newsList.length}건)`;
    
    if (newsList.length === 0) {
        contentElement.innerHTML = '<p class="text-muted">수집된 뉴스가 없습니다.</p>';
        return;
    }
    
    contentElement.innerHTML = newsList.map(generateNewsItemHtml).join('');
}

// 카테고리 이름 변환
function getCategoryName(category) {
    const names = {
        'energy': '에너지',
        'defense': '방산',
        'insurance': '보험'
    };
    return names[category] || category;
}

// 대시보드 업데이트
async function updateDashboard() {
    const data = await loadNewsData();
    if (!data) {
        showError('데이터를 불러올 수 없습니다.');
        return;
    }
    
    // 카테고리별 뉴스 표시
    displayCategoryNews('energy', data.energy || []);
    displayCategoryNews('defense', data.defense || []);
    displayCategoryNews('insurance', data.insurance || []);
    
    // 총계 업데이트
    const total = (data.energy || []).length + 
                 (data.defense || []).length + 
                 (data.insurance || []).length;
    document.getElementById('totalCount').textContent = `총 수집: ${total}건`;
    
    // 마지막 업데이트 시간 표시
    document.getElementById('lastUpdate').textContent = 
        `마지막 업데이트: ${data.lastUpdate || '알 수 없음'}`;
}

// 에러 메시지 표시
function showError(message) {
    const categories = ['energy', 'defense', 'insurance'];
    categories.forEach(category => {
        document.getElementById(`${category}Content`).innerHTML = 
            `<p class="text-danger"><i class="bi bi-exclamation-triangle"></i> ${message}</p>`;
    });
}

// 페이지 새로고침
function refreshPage() {
    const refreshBtn = document.getElementById('refreshBtn');
    refreshBtn.disabled = true;
    refreshBtn.querySelector('i').classList.add('loading');
    
    setTimeout(() => {
        location.reload();
    }, 1000);
}

// 초기 로드
document.addEventListener('DOMContentLoaded', updateDashboard); 