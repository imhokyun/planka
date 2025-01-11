import requests
import json

def login_planka(url: str, username: str, password: str) -> str:
    """
    Planka 로그인하고 토큰을 반환합니다
    """
    login_url = f"{url}/api/access-tokens"
    payload = {
        "emailOrUsername": username,
        "password": password
    }
    
    response = requests.post(login_url, json=payload)
    if response.status_code == 200:
        # 응답 구조 확인을 위해 출력
        print("API 응답:", response.json())
        return response.json()['item']  # item이 직접 토큰 문자열
    else:
        raise Exception(f"로그인 실패: {response.status_code}")

def list_projects(url: str, token: str):
    """
    모든 프로젝트를 조회합니다
    """
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    projects_url = f"{url}/api/projects"
    
    try:
        response = requests.get(projects_url, headers=headers)
        if response.status_code == 200:
            projects = response.json()['items']
            print("\n=== 프로젝트 목록 ===")
            for project in projects:
                print(f"프로젝트 이름: {project['name']}")
                print(f"프로젝트 ID: {project['id']}")
                print("---")
        else:
            print("프로젝트 조회 실패")
            
    except Exception as e:
        print(f"에러 발생: {str(e)}")

def list_boards_in_project(url: str, token: str, project_id: str):
    """
    특정 프로젝트의 모든 보드를 조회합니다
    """
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    # URL 끝에 슬래시가 있다면 제거
    if url.endswith('/'):
        url = url[:-1]
    
    # 프로젝트 상세 정보 조회 URL (보드 정보 포함)
    project_url = f"{url}/api/projects/{project_id}"
    
    try:
        response = requests.get(project_url, headers=headers)
        
        if response.status_code == 200:
            project_data = response.json()
            boards = project_data.get('included', {}).get('boards', [])
            
            print(f"\n=== 프로젝트 ID {project_id}의 보드 목록 ===")
            for board in boards:
                print(f"보드 이름: {board.get('name', 'No name')}")
                print(f"보드 ID: {board['id']}")
                print("---")
            
            return boards
        else:
            print(f"보드 조회 실패: {response.status_code}")
            print(f"에러 메시지: {response.text}")
            
    except Exception as e:
        print(f"에러 발생: {str(e)}")
        print(f"에러 타입: {type(e)}")

def list_cards_in_board(url: str, token: str, board_id: str):
    """
    특정 보드의 모든 카드를 조회합니다
    """
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    if url.endswith('/'):
        url = url[:-1]
    
    # 보드 상세 정보 조회 URL (카드 정보 포함)
    board_url = f"{url}/api/boards/{board_id}"
    
    try:
        response = requests.get(board_url, headers=headers)
        
        if response.status_code == 200:
            board_data = response.json()
            cards = board_data.get('included', {}).get('cards', [])
            
            print(f"\n=== 보드 ID {board_id}의 카드 목록 ===")
            for card in cards:
                print(f"카드 이름: {card.get('name', 'No name')}")
                print(f"카드 ID: {card['id']}")
                print("---")
            
            return cards
        else:
            print(f"카드 조회 실패: {response.status_code}")
            print(f"에러 메시지: {response.text}")
            
    except Exception as e:
        print(f"에러 발생: {str(e)}")
        print(f"에러 타입: {type(e)}")

def get_card_details(url: str, token: str, card_id: str):
    """
    특정 카드의 상세 정보를 조회합니다
    """
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    if url.endswith('/'):
        url = url[:-1]
    
    # 카드 상세 정보 조회 URL
    card_url = f"{url}/api/cards/{card_id}"
    
    try:
        response = requests.get(card_url, headers=headers)
        
        if response.status_code == 200:
            card_data = response.json()
            
            print(f"\n=== 카드 ID {card_id}의 상세 정보 ===")
            
            # 기본 정보
            print("\n[기본 정보]")
            print(f"카드 이름: {card_data.get('item', {}).get('name')}")
            print(f"설명 내용: {card_data.get('item', {}).get('description')}")
            
            # 태스크 정보
            if 'included' in card_data and 'tasks' in card_data['included']:
                print("\n[태스크 목록]")
                for task in card_data['included']['tasks']:
                    status = "✓" if task.get('isCompleted') else "□"
                    print(f"{status} {task.get('name')}")
            
            # 첨부파일 정보
            if 'included' in card_data and 'attachments' in card_data['included']:
                print("\n[첨부파일 목록]")
                for attachment in card_data['included']['attachments']:
                    print(f"- {attachment.get('name')}")
                    print(f"  URL: {attachment.get('url')}")
            
            return card_data
        else:
            print(f"카드 조회 실패: {response.status_code}")
            print(f"에러 메시지: {response.text}")
            
    except Exception as e:
        print(f"에러 발생: {str(e)}")
        print(f"에러 타입: {type(e)}")

def get_card_description(url: str, token: str, card_id: str):
    """
    특정 카드의 설명 정보만 조회합니다
    """
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    if url.endswith('/'):
        url = url[:-1]
    
    # 카드 상세 정보 조회 URL
    card_url = f"{url}/api/cards/{card_id}"
    
    try:
        response = requests.get(card_url, headers=headers)
        
        if response.status_code == 200:
            card_data = response.json()
            print("\nAPI 응답:", card_data)  # 전체 응답 데이터 확인
            
            # 메인 데이터에서 description 가져오기
            description = card_data.get('description', '설명 없음')
            
            print(f"\n=== 카드 ID {card_id}의 설명 ===")
            print(f"카드 이름: {card_data.get('name', 'No name')}")
            print(f"설명 내용:\n{description}")
            
            return description
        else:
            print(f"카드 조회 실패: {response.status_code}")
            print(f"에러 메시지: {response.text}")
            
    except Exception as e:
        print(f"에러 발생: {str(e)}")
        print(f"에러 타입: {type(e)}")

# 사용 예시:
if __name__ == "__main__":
    PLANKA_URL = "https://planka.multion-dev.synology.me"
    USERNAME = "multion2019@gmail.com"
    PASSWORD = "qwer7410"
    
    # 로그인하여 토큰 받기
    token = login_planka(PLANKA_URL, USERNAME, PASSWORD)
    
    # 모든 프로젝트 리스트
    list_projects(PLANKA_URL, token)
    
    # 특정 프로젝트의 보드 리스트
    project_id = "1420747059631227907"  # 매장관리 프로젝트
    list_boards_in_project(PLANKA_URL, token, project_id)
    
    # 특정 보드의 카드 리스트
    board_id = "1420747113528034309"  # 매장관리 보드
    list_cards_in_board(PLANKA_URL, token, board_id)
    
    # 특정 카드의 상세 정보 조회
    card_id = "1420747291735622669"
    get_card_details(PLANKA_URL, token, card_id)
    
    # # 특정 카드의 설명 정보 조회
    # card_id = "1420747291735622669"
    # get_card_description(PLANKA_URL, token, card_id)