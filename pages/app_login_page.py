from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.by import By
import time

class AppLoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    # --- 요소 탐색 함수들 ---
    def get_email_input(self):
        return self.driver.find_elements(By.CLASS_NAME, "android.widget.EditText")[0]

    def get_password_input(self):
        return self.driver.find_elements(By.CLASS_NAME, "android.widget.EditText")[1]

    def get_login_button(self):
        return self.driver.find_elements(By.CLASS_NAME, "android.widget.Button")[0]

    # --- 🎯 테스트 코드(test_app_login.py)에서 호출하는 함수들 정의 ---
    def enter_email(self, email):
        """이메일 입력 (테스트 코드 호환용)"""
        field = self.get_email_input()
        field.click()
        field.clear()
        field.send_keys(email)

    def enter_password(self, password):
        """비밀번호 입력 (테스트 코드 호환용)"""
        field = self.get_password_input()
        field.click()
        field.clear()
        field.send_keys(password)

    def click_login(self):
        """로그인 버튼 클릭 (테스트 코드 호환용)"""
        self.get_login_button().click()

    # --- 기존 로직 유지 ---
    def get_error_message(self):
        for _ in range(10):
            source = self.driver.page_source
            if any(keyword in source for keyword in ["틀렸습니다", "유효하지", "실패"]):
                if "틀렸습니다" in source: return "이메일 혹은 비밀번호가 틀렸습니다."
                if "유효하지" in source: return "유효하지 않은 이메일 형식입니다."
                if "실패" in source: return "로그인에 실패했습니다."
            time.sleep(0.5)
        return ""

    def is_on_login_page(self):
        return len(self.driver.find_elements(By.CLASS_NAME, "android.widget.EditText")) > 0
    
    def login(self, email, password):
        """한 번에 로그인 프로세스 수행"""
        self.enter_email(email)
        self.enter_password(password)
        self.click_login()

    def logout(self):
        """아까 찾은 content-desc='로그아웃' 버튼 클릭"""
        try:
            # 🎯 945, 104 좌표에 있던 그 버튼입니다.
            self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "로그아웃").click()
            print("✅ 이모티콘 로그아웃 버튼 클릭 성공")
            return True
        except Exception as e:
            print(f"❌ 로그아웃 버튼 클릭 실패: {e}")
            # 백업: 좌표 클릭 (bounds="[945,104][1080,239]")
            # self.driver.tap([(1000, 150)]) 
            return False
        
    def ensure_login_page(self):
        """현재 페이지를 확인하고, 메인 페이지라면 로그아웃하여 로그인 페이지로 진입합니다."""
        print("🔍 현재 페이지 상태 확인 중...")
        
        # 1. 로그인 페이지인지 확인 (이메일 입력창 존재 여부)
        if self.is_on_login_page():
            print("✅ 현재 로그인 페이지입니다.")
            return

        # 2. 로그인 페이지가 아니라면 로그아웃 시도
        print("🔄 메인 페이지로 판단됨. 로그아웃을 시도합니다.")
        logout_success = self.logout()
        
        if logout_success:
            # 로그아웃 애니메이션이나 페이지 전환 대기
            time.sleep(2)
            if self.is_on_login_page():
                print("✅ 로그아웃 성공 후 로그인 페이지 진입 완료")
            else:
                print("⚠️ 로그아웃 후에도 로그인 페이지가 아닙니다. 추가 확인 필요.")
        else:
            print("❌ 로그아웃 버튼을 찾지 못했습니다. 이미 로그인 페이지거나 다른 화면일 수 있습니다.")