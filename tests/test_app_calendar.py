import pytest
import time
from pages.app_login_page import AppLoginPage
from pages.app_calendar_page import AppCalendarPage

@pytest.fixture(scope="module", autouse=True)
def login_once(driver):
    """모듈 시작 시 한 번만 로그인"""
    login_page = AppLoginPage(driver)
    login_page.ensure_login_page()
    login_page.login("test@naver.com", "123456")
    time.sleep(3)
    yield  # 이후 로그아웃 없음

def test_add_schedule_success(driver):
    """일정 정상 추가"""
    calendar = AppCalendarPage(driver)
    calendar.click_add_button()
    assert calendar.is_add_dialog_open(), "일정 추가 다이얼로그가 열리지 않음"
    calendar.enter_title("테스트 일정")
    calendar.click_save_button()
    assert calendar.is_event_added("테스트 일정"), "일정이 추가되지 않음"

def test_add_schedule_empty_title(driver):
    """제목 없이 저장 시도"""
    calendar = AppCalendarPage(driver)
    calendar.click_add_button()
    assert calendar.is_add_dialog_open(), "일정 추가 다이얼로그가 열리지 않음"
    calendar.click_save_button()
    assert calendar.is_add_dialog_open(), "빈 제목으로 저장됐음 (버그)"

def test_add_schedule_cancel(driver):
    """취소 버튼으로 다이얼로그 닫기"""
    calendar = AppCalendarPage(driver)
    calendar.ensure_add_dialog_open()  # 추가
    assert calendar.is_add_dialog_open(), "일정 추가 다이얼로그가 열리지 않음"
    calendar.click_cancel_button()
    assert not calendar.is_add_dialog_open(), "취소 후에도 다이얼로그가 열려있음"

def test_delete_schedule(driver):
    """일정 삭제"""
    calendar = AppCalendarPage(driver)

    # 삭제할 일정 추가
    calendar.click_add_button()
    assert calendar.is_add_dialog_open(), "일정 추가 다이얼로그가 열리지 않음"
    calendar.enter_title("삭제테스트")
    calendar.click_save_button()
    time.sleep(2)

    # 삭제 버튼 클릭
    result = calendar.click_delete_button_of_first_event()
    assert result, "삭제할 일정을 찾지 못함"

    # 삭제 확인
    assert calendar.is_event_gone("삭제테스트"), "일정이 삭제되지 않음"