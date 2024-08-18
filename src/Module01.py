from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib
import requests
import time
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')

def get_titles_with_links1(page_url, list_web):
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(page_url)
    # Sử dụng Explicit Wait
    wait = WebDriverWait(driver, 60)  # Đợi tối đa 10 giây
    # Locate the element using its "name" attribute
    try:
        # Tìm phần tử có tên "g-recaptcha-response"
        url = page_url
        site_key = "6LdZc40jAAAAAD5UwNdx-ZxMNQgYLpM3V1sotiUL"  # Site key của web cần giải
        api_key = "b7c111558cf84eeebcedfd0cd3064a17"  # mà api của 1st
        capcha = driver.find_element("name", "g-recaptcha-response")
        if capcha != None:
            r = requests.get(
                f'https://api.1stcaptcha.com/recaptchav2?apikey={api_key}&sitekey={site_key}&siteurl={urllib.parse.quote(url)}&invisible=false')
            print(r.json())
            ID = r.json()["TaskId"]
            while True:
                r = requests.get(f'https://api.1stcaptcha.com/getresult?apikey={api_key}&taskid={ID}')
                status = r.json()["Status"]
                if 'SUCCESS' == status:
                    print('Dịch vụ giải thành công, kết quả là: \n')
                    print(r.json())
                    result = r.json()["Data"]["Token"]
                    driver.execute_script(f"arguments[0].innerHTML='{result}'", capcha)
                    time.sleep(2)
                    button = driver.find_element(By.ID, "verify")
                    button.click()
                    print("Giải captcha: OK")
                    break
                elif 'ERROR' == status:
                    print('Dịch vụ giải thất bại')
                    print(r.json())
                    break
                time.sleep(1)
        ct_titles = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'content-item')))
        for w in ct_titles:
            list_web.append(w.find_element(By.TAG_NAME, 'a').get_attribute('href'))

        driver.quit()
        # Nếu phần tử tồn tại, thực hiện các tương tác với nó ở đây
        # Ví dụ: element.click() hoặc element.send_keys("...")
    except NoSuchElementException:
        # Nếu phần tử không tồn tại, bạn có thể bỏ qua hoặc thực hiện các hành động khác
        ct_titles = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'content-item')))
        for w in ct_titles:list_web.append(w.find_element(By.TAG_NAME, 'a').get_attribute('href'))
        driver.quit()
    return list_web
def extract_property_info(url):
    try:
        # Use Selenium to navigate to the URL
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        # Wait for the page to load and extract its content
        wait = WebDriverWait(driver, 60)
        try:
            # Tìm phần tử có tên "g-recaptcha-response"
            url = url
            site_key = "6LdZc40jAAAAAD5UwNdx-ZxMNQgYLpM3V1sotiUL"  # Site key của web cần giải
            api_key = "b7c111558cf84eeebcedfd0cd3064a17"  # mà api của 1st
            capcha = driver.find_element("name", "g-recaptcha-response")
            if capcha != None:
                r = requests.get(
                    f'https://api.1stcaptcha.com/recaptchav2?apikey={api_key}&sitekey={site_key}&siteurl={urllib.parse.quote(url)}&invisible=false')
                print(r.json())
                ID = r.json()["TaskId"]
                while True:
                    r = requests.get(f'https://api.1stcaptcha.com/getresult?apikey={api_key}&taskid={ID}')
                    status = r.json()["Status"]
                    if 'SUCCESS' == status:
                        print('Dịch vụ giải thành công, kết quả là: \n')
                        print(r.json())
                        result = r.json()["Data"]["Token"]
                        driver.execute_script(f"arguments[0].innerHTML='{result}'", capcha)
                        time.sleep(2)
                        button = driver.find_element(By.ID, "verify")
                        button.click()
                        print("Giải captcha: OK")
                        break
                    elif 'ERROR' == status:
                        print('Dịch vụ giải thất bại')
                        print(r.json())
                        break
                    time.sleep(2)
                    # Lấy thoongtin từ web
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'moreinfor1')))
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'price')))
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'square')))
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'address')))
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            property_info = {}
            more_info_div = soup.find('div', class_='moreinfor1')
            if more_info_div:
                table_rows = more_info_div.find_all('tr')
                for row in table_rows:
                    table_data = row.find_all('td')
                    for i in range(0, len(table_data), 2):
                        key = table_data[i].get_text(strip=True)
                        value = table_data[i + 1].get_text(strip=True)
                        property_info[key] = value
            price_span = soup.find('span', {'class': 'price'})
            if price_span:
                property_info['Giá'] = price_span.find('span', {'class': 'value'}).text
            square_span = soup.find('span', {'class': 'square'})
            if square_span:
                property_info['Diện tích'] = square_span.find('span', {'class': 'value'}).text
            address_div = soup.find('div', {'class': 'address'})
            if address_div:
                property_info['Địa chỉ'] = address_div.find('span', {'class': 'value'}).text
            driver.quit()
        except NoSuchElementException:
            # Lấy thoongtin từ web
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'moreinfor1')))
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'price')))
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'square')))
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'address')))
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            property_info = {}
            more_info_div = soup.find('div', class_='moreinfor1')
            if more_info_div:
                table_rows = more_info_div.find_all('tr')
                for row in table_rows:
                    table_data = row.find_all('td')
                    for i in range(0, len(table_data), 2):
                        key = table_data[i].get_text(strip=True)
                        value = table_data[i + 1].get_text(strip=True)
                        property_info[key] = value
            price_span = soup.find('span', {'class': 'price'})
            if price_span:
                property_info['Giá'] = price_span.find('span', {'class': 'value'}).text
            square_span = soup.find('span', {'class': 'square'})
            if square_span:
                property_info['Diện tích'] = square_span.find('span', {'class': 'value'}).text
            address_div = soup.find('div', {'class': 'address'})
            if address_div:
                property_info['Địa chỉ'] = address_div.find('span', {'class': 'value'}).text
            driver.quit()
        return property_info
    except Exception as e:
        # Handle any other errors with an error message
        print(e)
        return None
