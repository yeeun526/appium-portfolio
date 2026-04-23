from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class AppCalendarPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    def click_add_button(self):
        """+ 버튼 클릭 (캘린더 화면 FAB)"""
        self.driver.tap([(928, 1884)])
        time.sleep(1)

    def enter_title(self, title):
        """일정 제목 입력"""
        field = self.driver.find_element(By.CLASS_NAME, "android.widget.EditText")
        field.click()
        field.clear()
        field.send_keys(title)

    def click_save_button(self):
        """저장 버튼 클릭"""
        self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "저장").click()
        time.sleep(1)

    def click_cancel_button(self):
        """취소 버튼 클릭"""
        self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "취소").click()
        time.sleep(1)

    def is_add_dialog_open(self):
        """일정 추가 다이얼로그가 열렸는지 확인"""
        return "일정 추가" in self.driver.page_source

    def is_event_added(self, title):
        """일정이 캘린더에 추가됐는지 확인"""
        for _ in range(10):
            if title in self.driver.page_source:
                return True
            time.sleep(0.5)
        return False
    
    def ensure_add_dialog_open(self):
        """다이얼로그가 닫혀있으면 다시 열기"""
        if not self.is_add_dialog_open():
            self.click_add_button()
            time.sleep(1)

    def click_delete_button_of_first_event(self):
        """첫 번째 일정의 삭제 버튼 클릭 (두 번째 버튼)"""
        from selenium.webdriver.common.by import By
        # 일정 카드 안의 버튼들 중 두 번째가 삭제
        events = self.driver.find_elements(By.XPATH, 
            '//android.view.View[contains(@content-desc, "테스트 일정")]')
        if not events:
            return False
        # 첫 번째 일정 카드 안의 버튼 2개 중 두 번째(삭제)
        buttons = events[0].find_elements(By.CLASS_NAME, "android.widget.Button")
        buttons[1].click()
        time.sleep(1)
        return True

    def is_event_gone(self, title):
        """일정이 화면에서 사라졌는지 확인"""
        time.sleep(2)
        return title not in self.driver.page_source