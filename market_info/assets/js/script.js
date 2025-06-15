// Bootstrap 탭 활성화 (필요시 확장)
document.addEventListener('DOMContentLoaded', function() {
  var triggerTabList = [].slice.call(document.querySelectorAll('#marketTabs a'));
  triggerTabList.forEach(function(triggerEl) {
    triggerEl.addEventListener('click', function (e) {
      e.preventDefault();
      var tab = new bootstrap.Tab(triggerEl);
      tab.show();
    });
  });
});

// 페이지 로드 완료 후 실행
document.addEventListener('DOMContentLoaded', function() {
    console.log('시장정보 대시보드 로드 완료');
    // MARKET_DATA를 직접 사용 (CORS 문제 해결)
    if (MARKET_DATA) {
        chartInstances = {};
        createMarketSizeChart('insuranceChart', MARKET_DATA.insurance);
        createMarketSizeChart('energyChart', MARKET_DATA.energy);
        createMarketSizeChart('defenseChart', MARKET_DATA.defense);
        updateMarketInfo(MARKET_DATA);
    } else {
        console.error('MARKET_DATA가 정의되지 않았습니다.');
    }
    
    // 탭 전환 시 애니메이션 효과
    const tabTriggerList = document.querySelectorAll('#marketTab button, #marketTab a');
    tabTriggerList.forEach(tabTrigger => {
        tabTrigger.addEventListener('shown.bs.tab', function (event) {
            const targetTab = event.target.getAttribute('href') || event.target.getAttribute('data-bs-target');
            console.log('탭 전환:', targetTab);
            
            // 탭 전환 시 카드 애니메이션
            const targetPane = document.querySelector(targetTab);
            if (targetPane) {
                const cards = targetPane.querySelectorAll('.card');
                cards.forEach((card, index) => {
                    card.style.opacity = '0.5';
                    setTimeout(() => {
                        card.style.opacity = '1';
                        card.style.transition = 'opacity 0.3s ease';
                    }, index * 100);
                });
            }
        });
    });
    
    // 차트 영역 클릭 시 임시 메시지
    const chartPlaceholders = document.querySelectorAll('.chart-placeholder');
    chartPlaceholders.forEach(placeholder => {
        placeholder.addEventListener('click', function() {
            const originalText = this.innerHTML;
            this.innerHTML = '<p class="text-center mt-5 text-primary">💡 차트 데이터 연동 예정</p>';
            setTimeout(() => {
                this.innerHTML = originalText;
            }, 2000);
        });
    });
    
    // 카드 호버 효과
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
            this.style.transition = 'transform 0.2s ease';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
    
    // 마지막 업데이트 시간 표시
    updateLastUpdateTime();
});

// 마지막 업데이트 시간 표시 함수
function updateLastUpdateTime() {
    const now = new Date();
    const timeString = now.toLocaleString('ko-KR');
    // 각 탭의 첫 번째 카드에 업데이트 시간 추가
    const firstCards = document.querySelectorAll('.tab-pane .card:first-child .card-body');
    firstCards.forEach(cardBody => {
        // 기존 표시 제거
        const old = cardBody.querySelector('.update-time');
        if (old) old.remove();
        const updateInfo = document.createElement('small');
        updateInfo.className = 'update-time';
        updateInfo.innerHTML = `<i class="bi bi-clock"></i> 최종 업데이트: ${timeString}`;
        cardBody.style.position = 'relative';
        cardBody.appendChild(updateInfo);
    });
}

// 시장 정보 동적 업데이트 함수
function updateMarketInfo(marketData) {
    try {
        updateTabContent('insurance', marketData.insurance);
        updateTabContent('energy', marketData.energy);
        updateTabContent('defense', marketData.defense);
        console.log('카드 텍스트/리스트 동적 갱신 완료');
    } catch (e) {
        console.error('카드 정보 갱신 중 오류:', e);
        alert('카드 정보 표시 중 오류가 발생했습니다. 새로고침 해주세요.');
    }
}

function updateTabContent(tabId, data) {
    try {
        const tabPane = document.getElementById(tabId);
        if (!tabPane) throw new Error(tabId + ' 탭 DOM 없음');
        // 주요 이슈 업데이트 - 첫 번째 row의 두 번째 카드
        const issuesCard = tabPane.querySelector('.row:first-child .col-md-6:nth-child(2) .card-body');
        if (!issuesCard) throw new Error(tabId + ' 주요이슈 카드 없음');
        issuesCard.innerHTML = data.keyIssues.map(issue => `<li>${issue}</li>`).join('');
        issuesCard.innerHTML = `<ul>${issuesCard.innerHTML}</ul>`;
        // 핵심 기업 동향 업데이트 - 두 번째 row의 첫 번째 카드
        const companiesTable = tabPane.querySelector('.row:nth-child(2) .col-md-6:first-child tbody');
        if (!companiesTable) throw new Error(tabId + ' 기업 테이블 없음');
        companiesTable.innerHTML = data.keyCompanies.map(company => 
            `<tr><td><strong>${company.name}</strong></td><td>${company.status}</td></tr>`
        ).join('');
        // 정책/규제 변화 업데이트 - 두 번째 row의 두 번째 카드
        const policiesCard = tabPane.querySelector('.row:nth-child(2) .col-md-6:nth-child(2) .card-body');
        if (!policiesCard) throw new Error(tabId + ' 정책 카드 없음');
        policiesCard.innerHTML = data.policies.map(policy => `<li>${policy}</li>`).join('');
        policiesCard.innerHTML = `<ul>${policiesCard.innerHTML}</ul>`;
        // 시장 규모 텍스트 업데이트 (차트 하단)
        const currentYear = new Date().getFullYear();
        const latestSize = data.marketSize[data.marketSize.length - 1];
        const latestGrowth = data.growthRate[data.growthRate.length - 1];
        const chartCard = tabPane.querySelector('.card:first-child .card-body');
        if (!chartCard) throw new Error(tabId + ' 차트 카드 없음');
        const existingInfo = chartCard.querySelector('.market-info');
        if (existingInfo) existingInfo.remove();
        const marketInfo = document.createElement('div');
        marketInfo.className = 'market-info mt-2';
        marketInfo.innerHTML = `
            <small class="text-muted">
                <strong>${currentYear}년 시장규모:</strong> ${latestSize}조원 | 
                <strong>연평균 성장률:</strong> ${latestGrowth}%
            </small>
        `;
        chartCard.appendChild(marketInfo);
    } catch (e) {
        console.error(`[${tabId}] 카드 내용 동적 생성 오류:`, e);
    }
}

// 차트 인스턴스 저장용
let chartInstances = {};

function updateAllCharts(marketData) {
    try {
        ['insurance', 'energy', 'defense'].forEach((key) => {
            const chartId = key + 'Chart';
            if (chartInstances[chartId]) {
                chartInstances[chartId].destroy();
            }
            chartInstances[chartId] = createMarketSizeChart(chartId, marketData[key]);
        });
        console.log('차트 전체 갱신 완료');
    } catch (e) {
        console.error('차트 전체 갱신 중 오류:', e);
        alert('차트 표시 중 오류가 발생했습니다. 새로고침 해주세요.');
    }
}

// 데이터 새로고침 함수 개선
async function refreshMarketData() {
    console.log('시장 데이터 새로고침 시작...');
    const refreshBtn = document.querySelector('.btn-outline-success');
    const originalText = refreshBtn.innerHTML;
    refreshBtn.innerHTML = '🔄 새로고침 중...';
    refreshBtn.disabled = true;
    try {
        // 데이터는 이미 MARKET_DATA에 있음
        updateAllCharts(MARKET_DATA);
        updateMarketInfo(MARKET_DATA);
        updateLastUpdateTime();
        console.log('데이터 새로고침 완료');
    } catch (error) {
        console.error('새로고침 실패:', error);
        alert('데이터 새로고침 중 오류가 발생했습니다.');
    } finally {
        refreshBtn.innerHTML = originalText;
        refreshBtn.disabled = false;
    }
}

// 차트 생성 함수들
function createMarketSizeChart(canvasId, marketData) {
    if (typeof Chart === 'undefined') {
        console.error('Chart.js 로딩 실패: Chart 객체가 없습니다.');
        const canvas = document.getElementById(canvasId);
        if (canvas) {
            const ctx = canvas.getContext('2d');
            ctx.font = '16px sans-serif';
            ctx.fillStyle = '#dc3545';
            ctx.fillText('Chart.js 로딩 실패', 10, 50);
        }
        return;
    }
    // 기존 차트 코드 유지
    return new Chart(document.getElementById(canvasId).getContext('2d'), {
        type: 'line',
        data: {
            labels: ['2020', '2021', '2022', '2023', '2024(E)'],
            datasets: [{
                label: '시장규모 (조원)',
                data: marketData.marketSize,
                borderColor: '#2c5aa0',
                backgroundColor: 'rgba(44, 90, 160, 0.1)',
                tension: 0.4,
                fill: true
            }, {
                label: '성장률 (%)',
                data: marketData.growthRate,
                borderColor: '#dc3545',
                backgroundColor: 'rgba(220, 53, 69, 0.1)',
                yAxisID: 'y1',
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { position: 'top' }
            },
            scales: {
                y: { beginAtZero: true, title: { display: true, text: '시장규모 (조원)' }},
                y1: { 
                    type: 'linear', 
                    position: 'right', 
                    beginAtZero: true,
                    title: { display: true, text: '성장률 (%)' }
                }
            }
        }
    });
}

// 데이터 직접 삽입 (CORS 회피)
const MARKET_DATA = {
  "insurance": {
    "marketSize": [1.2, 1.3, 1.5, 1.7, 1.9],
    "growthRate": [8.3, 15.4, 13.3, 6.7, 11.8],
    "keyIssues": [
      "보험중개사 법적 지위 강화 방안 논의",
      "디지털 보험중개 플랫폼 확산",
      "기업보험 시장 성장세 지속"
    ],
    "keyCompanies": [
      {"name": "록톤코리아", "status": "글로벌 1위 보험중개사"},
      {"name": "마시중개", "status": "국내 대형 중개사"},
      {"name": "인슈어런스", "status": "디지털 중개 플랫폼"}
    ],
    "policies": [
      "보험업법 개정안 발의 (2024.12)",
      "보험중개사 수수료 투명화 의무",
      "기업보험 중개시장 활성화 정책"
    ]
  },
  "energy": {
    "marketSize": [12.5, 15.2, 18.7, 22.1, 26.8],
    "growthRate": [21.6, 23.0, 18.2, 21.3, 19.0],
    "keyIssues": [
      "RE100 도입 기업 급증",
      "태양광 폐패널 재활용 기술 확산",
      "에너지저장장치(ESS) 시장 진출 확대"
    ],
    "keyCompanies": [
      {"name": "한화솔루션", "status": "태양광 모듈 글로벌 3위"},
      {"name": "두산에너빌리티", "status": "풍력발전 기술개발"},
      {"name": "LG에너지솔루션", "status": "ESS 시장 진출"}
    ],
    "policies": [
      "제10차 전력수급기본계획 수립",
      "탄소배출권 거래제도 강화",
      "RE100 이행지원 세제혜택"
    ]
  },
  "defense": {
    "marketSize": [4.1, 4.8, 5.8, 6.7, 7.2],
    "growthRate": [17.1, 20.8, 15.5, 7.5, 12.3],
    "keyIssues": [
      "수출 확대로 방산업체 실적 개선",
      "첨단 무기체계 개발 R&D 투자 증가",
      "방산 R&D 투자 확지"
    ],
    "keyCompanies": [
      {"name": "한화에어로스페이스", "status": "항공엔진 수출확대"},
      {"name": "LIG넥스원", "status": "첨단 무기체계 개발"},
      {"name": "현대로템", "status": "방산차량 수출 성장"}
    ],
    "policies": [
      "방산기술 수출 규제완화",
      "첨단기술 수출허가 간소화",
      "방산수출 금융지원 확대"
    ]
  }
};

// 기존 loadMarketData 함수 및 fetch 관련 코드 완전 제거 