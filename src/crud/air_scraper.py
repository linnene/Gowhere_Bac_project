from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
import time
import re

from src.schemas.base import DATE, TIME, Itinerary_time
from config import path, id, config
from src.schemas.tools import Air


__all__ = ['get_air_info']


def get_air_info(dep: str, des: str, date: DATE) -> list[Air]:
    
    """
    通过Selenium自动化查询携程航班信息。

    Args:
        dep (str): 出发地，如 "重庆"
        des (str): 目的地，如 "东京"
        date (DATE): 日期类对象，包含年月日

    Returns:
        List[Air]: 返回航班对象列表
    """

    options = webdriver.ChromeOptions()
    # options.add_argument('--headless') 
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)

    try:
        driver.get(path.AIR_SEARCH_PAGE)
        
        for name, value in config.cookie_dict.items():
            driver.add_cookie({
                'name': name,
                'value': value,
                'domain': '.ctrip.com',
                'path': '/',
            })

        time.sleep(config.wait_time)

        # 点击空白区域使页面激活
        signal_BOX = driver.find_element(By.XPATH, id.signal_BOX)
        signal_BOX.click()

        # 填入出发地/目的地
        enter_desdep(driver, id.Dep_BOX, dep)
        enter_desdep(driver, id.Des_BOX, des)

        # 日期选择
        select_date(driver, date)

        # 提交搜索
        search_btn = driver.find_element(By.CLASS_NAME, "search-btn")
        search_btn.click()
        time.sleep(5)

        # 抓取航班信息
        air_list = []
        num = 1
        while True:
            try:
                element = driver.find_element(By.XPATH, id.air_box.format(num=num))
                Price = element.find_element(By.XPATH, ".//span[contains(@class, 'price')]")
                Des_airport = element.find_element(By.XPATH, ".//*[contains(@class, 'arrive-box')]/div[2]")
                Dep_airport = element.find_element(By.XPATH, ".//*[contains(@class, 'depart-box')]/div[2]")
                Des_time = element.find_element(By.XPATH, ".//*[contains(@class, 'arrive-box')]/div[1]")
                Dep_time = element.find_element(By.XPATH, ".//*[contains(@class, 'depart-box')]/div[1]")
                airline = element.find_element(By.XPATH, ".//*[contains(@class, 'airline-name')]")
                
                    # 修改处理到达时间的部分
                des_time_text = Des_time.text.strip()

                # 检查是否包含跨天信息
                next_day = 0
                if '+' in des_time_text:
                    # 分离时间和跨天信息
                    des_time_parts = des_time_text.split('+')
                    next_day = int(des_time_parts[1].replace('天', '').strip())
                    des_time_text = des_time_parts[0].strip()
                    # 提取跨天天数，如 "+1天" 中的 1

                des_hour, des_minute = map(int, des_time_text.split(':'))

                # 创建到达日期（考虑跨天）
                arrival_date = DATE(
                    year=date.year,
                    month=date.month,
                    day=str(int(date.day) + next_day)  # 加上跨天的天数
                )

                air = Air(
                    price=Price.text,
                    dep_air=Dep_airport.text,
                    des_air=Des_airport.text,
                    
                    #TODO：格式化日期
                    dep_time=Itinerary_time(    # 创建正确的Itinerary_time对象
                        date=date,
                        time=TIME(
                            hour=int(Dep_time.text.split(':')[0]),
                            minute=int(Dep_time.text.split(':')[1])
                        )
                    ),
                    des_time=Itinerary_time(
                        date=arrival_date,  
                        time=TIME(hour=des_hour, minute=des_minute)
                    ),

                    airline=airline.text,
                    # flight_number=flight_number.text,
                )

                air_list.append(air)
                num += 1
            except NoSuchElementException:
                print("航班抓取完成")
                break

        return air_list

    finally:
        driver.quit()


def select_date(driver, date: DATE):
    date_input = driver.find_element(By.XPATH, id.Date_But_BOX)
    date_input.click()
    time.sleep(config.wait_time)

    while True:
        year_L = extract_number_from_element(driver, id.Date_year_L_BOX)
        month_L = extract_number_from_element(driver, id.Date_month_L_BOX)
        year_R = extract_number_from_element(driver, id.Date_year_R_BOX)
        month_R = extract_number_from_element(driver, id.Date_month_R_BOX)

        if (year_L == date.year and month_L == date.month):
            driver.find_element(By.XPATH, id.Date_btn_R.format(date=date)).click()
            break
        elif (year_R == date.year and month_R == date.month):
            driver.find_element(By.XPATH, id.Date_btn_R.format(date=date)).click()
            break
        elif (year_L, month_L) > (date.year, date.month):
            driver.find_element(By.XPATH, id.Date_prev_Btn).click()
        else:
            driver.find_element(By.XPATH, id.Date_next_Btn).click()

        time.sleep(config.wait_time)


def extract_number_from_element(driver, xpath: str):
    try:
        element = driver.find_element(By.XPATH, xpath)
        match = re.search(r'\d+', element.text)
        return match.group() if match else None
    except Exception as e:
        print(f"[!] 提取日期数字失败: {e}")
        return None

def enter_desdep(driver, xpath: str, value: str):
    input_box = driver.find_element(By.XPATH, xpath)
    input_box.send_keys(Keys.CONTROL + 'a')
    input_box.send_keys(Keys.BACKSPACE)
    input_box.send_keys(value)
    time.sleep(config.wait_time)
