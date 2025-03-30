from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re

def scrape_data(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')
    if 'Please try again later!' in soup.find('body').get_text():
        driver.refresh()
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')
    if soup.find('div', class_='NotFound_warning__dwnf5'):
        driver.quit()
        return None
    try:
        # Kiểm tra xem nút "Xem thêm" có tồn tại không
        button = WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Xem thêm')]")))
        # driver.execute_script("arguments[0].scrollIntoView();", button)
        driver.execute_script("arguments[0].click();", button)
    except TimeoutException:
        # Trường hợp không tìm thấy nút "Xem thêm"
        print("No 'Xem thêm' button found on " + url)
    #
    # # Click the button using JavaScript
    # driver.execute_script("arguments[0].click();", button)

    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')
    driver.quit()

    data = {
        "Tên": "",
        "Diện tích đất": "",
        "Chiều ngang": "",
        "Mức giá": "",
        "Hướng cửa chính": "",
        "Số phòng ngủ": "",
        "Số phòng vệ sinh": "",
        "Tình trạng nội thất": "",
        "Giấy tờ pháp lý": "",
        "lat": "",
        "lon": "",
        "Địa chỉ": "",
        "Quận": "",
        "Thành phố": ""
    }


    # data["Tên"] = soup.find('h1', class_='AdDecriptionVeh_adTitle__vEuKD').text.strip()
    data["Tên"] = soup.find('div', class_='cd9gm5n').find('h1').text.strip()

    # Get giá
    # price_span = soup.find('span', class_='AdDecriptionVeh_price__u_N83')
    price_span = soup.find('b', class_='pyhk1dv')
    # data["Mức giá"] = price_span.text.split('-')[0].strip()
    data["Mức giá"] = price_span.text

    # Get địa chỉ
    # parent_span = soup.find('div', class_='media-body media-middle AdParam_address__5wp1F AdParam_addressClickable__coDWA').find('span', class_='fz13')
    address_span = soup.find('div', class_='sf0dbrp r9vw5if').find('span', class_='bwq0cbs')
    # if parent_span:
    #     for child in parent_span.find('span', class_='AdParam_addressClickableLoadMap__FLeKT'):
    #         child.extract()
    address = address_span.text.strip()

    data["Địa chỉ"] = address

    # Extract information after the last comma
    thanhpho = re.search(r',\s*([^,]+)$', address)

    if thanhpho:
        thanhpho_text = thanhpho.group(1).strip()
        data["Thành phố"] = thanhpho_text

    # Extract information after "Quận", "Huyện", "Thị xã" and before the next comma
    quan = re.search(r'(Quận|Huyện|Thị xã)\s*([^,]+)', address)
    if quan:
        quan_text = quan.group(2).strip()
        data["Quận"] = quan_text

    # Get tọa độ
    script_tags = soup.find_all('script')
    text = ""
    for tag in script_tags:
        if "longitude" in str(tag) and "latitude" in str(tag):
            text = str(tag)
            break

    # Check if longitude and latitude are found
    if text:
        index_longitude = text.find('longitude":') + len('longitude":')
        index_latitude = text.find('latitude":') + len('latitude":')
        longitude = float(text[index_longitude:text.find(',', index_longitude)])
        latitude = float(text[index_latitude:text.find(',', index_latitude)])
        data["lon"] = longitude
        data["lat"] = latitude

    # specs_items = soup.find_all('div', class_='media-body media-middle')
    specs_items = soup.find_all('div', class_='col-xs-6 abzctes')
    # specs_items = soup.find_all('div', class_='a4ep88f')

    for item in specs_items:
        label = item.find('div', class_='a4ep88f').text.strip()
        value = item.find('strong', class_='a3jfi3v').text.strip()
        data[label] = value

    print(data)

    # Dictionary to map old keys to new keys
    key_mapping = {
        "Diện tích đất": "Diện tích",
        "Chiều ngang": "Mặt tiền",
        "Hướng cửa chính": "Hướng nhà",
        "Số phòng vệ sinh": "Số toilet",
        "Tình trạng nội thất": "Nội thất",
        "Giấy tờ pháp lý": "Pháp lý"
    }

    updated_data = {key_mapping.get(old_key, old_key): value for old_key, value in data.items()}

    return updated_data

if __name__ == "__main__":
    scraped_data = scrape_data("https://www.nhatot.com/mua-ban-nha-dat-quan-cau-giay-ha-noi/123912003.htm")
    print(scraped_data)
