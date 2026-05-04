import pytest
import subprocess
import time
from appium import webdriver
from appium.options.android import UiAutomator2Options 

def ensure_device_connected():
    """기기 연결 상태 확인 및 ADB 재시작"""
    try:
        result = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
        if "R5CY53A0ESH" not in result.stdout:
            subprocess.run(['adb', 'kill-server'], check=True)
            subprocess.run(['adb', 'start-server'], check=True)
            time.sleep(2)
    except:
        pass

@pytest.fixture(scope="module")
def driver():
    ensure_device_connected()
    
    # 이제 이 클래스를 정상적으로 호출할 수 있습니다.
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.automation_name = "UiAutomator2"
    options.udid = "R5CY53A0ESH"
    
    # Android 16 안정성 옵션
    options.set_capability("appium:noReset", True)
    options.set_capability("appium:newCommandTimeout", 3600)
    options.set_capability("appium:uiautomator2ServerLaunchTimeout", 90000)
    options.set_capability("appium:appPackage", "com.example.jesus_worship_calendar_app")
    options.set_capability("appium:appActivity", ".MainActivity")

    try:
        driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
        yield driver
    finally:
        if 'driver' in locals():
            driver.quit()