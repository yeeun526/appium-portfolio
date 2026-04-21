import pytest
from pages.app_login_page import AppLoginPage

# tests/test_app_login.py 상단에 추가

@pytest.fixture(autouse=True)
def setup_login_page(driver):
    """모든 테스트 시작 전 자동으로 로그인 페이지 상태를 보장함"""
    login_page = AppLoginPage(driver)
    login_page.ensure_login_page()
    yield

def test_login_fail(driver):
    """잘못된 계정으로 로그인 실패"""
    login_page = AppLoginPage(driver)
    login_page.login("wrong@test.com", "wrongpassword")
    error = login_page.get_error_message()
    print(f"에러 메시지: {error}")
    assert "실패" in error or "틀렸습니다" in error

def test_invalid_email_format(driver):
    """이메일 형식 오류"""
    login_page = AppLoginPage(driver)
    login_page.login("abc", "123456")
    error = login_page.get_error_message()
    print(f"에러 메시지: {error}")
    assert "유효하지" in error

def test_empty_password(driver):
    """비밀번호 빈칸"""
    login_page = AppLoginPage(driver)
    login_page.login("test@naver.com", "")
    error = login_page.get_error_message()
    print(f"에러 메시지: {error}")
    assert "실패" in error or "틀렸습니다" in error

def test_empty_email(driver):
    """이메일 빈칸"""
    login_page = AppLoginPage(driver)
    login_page.login("", "123456")
    error = login_page.get_error_message()
    print(f"에러 메시지: {error}")
    assert "실패" in error or "틀렸습니다" in error

def test_short_password(driver):
    """비밀번호 6자리 미만"""
    login_page = AppLoginPage(driver)
    login_page.login("test@naver.com", "123")
    error = login_page.get_error_message()
    print(f"에러 메시지: {error}")
    assert "틀렸습니다" in error or "실패" in error

def test_login_and_logout_success(driver):
    login_page = AppLoginPage(driver)
    
    #login_page.ensure_login_page()

    # 1. 로그인 수행
    login_page.enter_email("test@naver.com")
    login_page.enter_password("123456")
    login_page.click_login()
    
    # 2. 로그인 후 메인 화면 전환 대기 (필요시 time.sleep 혹은 WebDriverWait)
    import time
    time.sleep(3) 
    