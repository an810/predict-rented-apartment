import requests
import re
from bs4 import BeautifulSoup

def scrape_data(url):
    response = requests.get(url)
    response.raise_for_status()  # Kiểm tra xem có lỗi trong quá trình tải không

    html_content = response.text

    data = {
        "Tên": "",
        "Diện tích": "",
        "Chiều ngang": "",
        "Mức giá": "",
        "Hướng": "",
        "Số phòng ngủ": "",
        "Số toilet": "",
        "Nội thất": "",
        "Pháp lý": "",
        "lat": "",
        "lon": "",
        "Địa chỉ": "",
        "Quận": "",
        "Thành phố": ""
    }

    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract tên
    data["Tên"] = soup.find('h1').text.strip()

    # Extract địa chỉ
    address = soup.find('div', class_='address').find('span', class_='value').text

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


    # Extract diện tích và giá
    more_info = soup.find('div', class_='moreinfor')
    values = more_info.find_all('span', class_='value')
    data["Mức giá"] = values[0].text.strip()
    data["Diện tích"] = values[1].text.strip()

    # Find the table within the div with class 'infor'
    table = soup.find('div', class_='infor').find('table')

    # Extract data from the table
    for row in table.find_all('tr'):
        columns = row.find_all('td')
        for i in range(0, len(columns), 2):
            key = columns[i].text.strip()
            value = columns[i + 1].text.strip()
            if key in data:
                data[key] = value

    # Dictionary to map old keys to new keys
    key_mapping = {
        "Hướng": "Hướng nhà",
        "Chiều ngang": "Mặt tiền"
    }

    updated_data = {key_mapping.get(old_key, old_key): value for old_key, value in data.items()}

    return updated_data


if __name__ == "__main__":
    # Gọi hàm scrape_data với URL nhận được
    scraped_data = scrape_data("https://alonhadat.com.vn/nguyen-van-tuyet-90m2-mat-tien-9-m-5-tang-vuong-43-ty-kinh-doanh-qua-dinh-15898067.html")

    # In ra kết quả hoặc làm gì đó với dữ liệu scrape được
    print(scraped_data)
