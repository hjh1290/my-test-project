import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

def zdnet_final_scraper():
    # 1. 대상 주소 (최신 뉴스 페이지)
    url = "https://www.zdnet.co.kr/news/?lstcode=0000"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        # 2. 뉴스 제목 요소를 찾는 여러 가지 방법 (백업 플랜 포함)
        # 방법 1: 최신 리스트 구조 (.news_content h2 또는 h3)
        # 방법 2: 기존 리스트 구조 (.assetText h3)
        news_items = soup.select(".news_content h2") or \
                     soup.select(".news_content h3") or \
                     soup.select(".assetText h3") or \
                     soup.find_all('h3') # 최후의 수단: 모든 h3 태그

        data_list = []
        for item in news_items:
            title = item.get_text(strip=True)
            # 부모 혹은 본인 태그에서 링크 추출
            link_tag = item.find('a') if item.find('a') else item.parent
            link = link_tag.get('href', '') if link_tag.name == 'a' else ""
            
            # 주소가 상대 경로일 경우 절대 경로로 변환
            if link and not link.startswith("http"):
                link = "https://www.zdnet.co.kr" + link

            # 제목이 일정 길이 이상인 진짜 뉴스만 선별
            if len(title) > 5:
                data_list.append({
                    "수집일시": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "뉴스제목": title,
                    "링크": link
                })

        # 3. 결과 저장 및 확인
        if data_list:
            df = pd.DataFrame(data_list)
            file_name = "zdnet_final_result.xlsx"
            df.to_excel(file_name, index=False)
            print(f"✅ [성공] 총 {len(data_list)}개의 최신 기술 뉴스를 찾았습니다.")
            print(f"📂 파일명: {file_name}")
            # 첫 번째 제목 샘플 출력
            print(f"📌 샘플 제목: {data_list[0]['뉴스제목']}")
        else:
            print("❌ 여전히 데이터를 찾지 못했습니다. 사이트에서 '봇'으로 인식해 차단했을 수 있습니다.")

    except Exception as e:
        print(f"❌ 접속 오류 발생: {e}")

# 실행
zdnet_final_scraper()
