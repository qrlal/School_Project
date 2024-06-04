import http.server
import socketserver
import requests
from bs4 import BeautifulSoup
from datetime import datetime

now = datetime.now()

# 년월 가져오기
current_year = str(now.year)
current_month = str(now.month).zfill(2)  # Pad month with zero if necessary

current_year_month = current_year + current_month

# 급식 정보 가져오기
url = f"https://open.neis.go.kr/hub/mealServiceDietInfo?KEY=54d9be581c8444989a8a4ad443d876a5&ATPT_OFCDC_SC_CODE=I10&SD_SCHUL_CODE=9300265&MLSV_YMD={current_year_month}"
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'xml')

    # MLSV_YMD, DDISH_NM, MMEAL_SC_NM 태그를 찾음
    ymd_tags = soup.find_all('MLSV_YMD')
    ymd = [i.text[6:] for i in ymd_tags]

    meal_tags = soup.find_all('DDISH_NM')
    meal = [tag.text for tag in meal_tags]

    meal_type_tags = soup.find_all('MMEAL_SC_NM')
    meal_index = [tag.text for tag in meal_type_tags]

    if "석식" in meal_index:
        ind = meal_index.index("석식")

        meal_lunch = meal[:ind]
        meal_dinner = meal[ind:]
        ymd_lunch = ymd[:ind]
        ymd_dinner = ymd[ind:]

        for y in range(len(ymd_lunch)):
            if y >= len(ymd_dinner) or ymd_lunch[y] != ymd_dinner[y]:
                ymd_dinner.insert(y, 'no')

        for i in range(len(ymd_dinner)):
            if ymd_dinner[i] == "no":
                meal_dinner.insert(i, "")

    def generate_html():
        html_content = f"""
        <html>
        <head>
            <meta charset="UTF-8">
            <title>급식 정보</title>
        </head>
        <body>
            <h1>{current_month}월 급식</h1>
            <table border='1'>
                <tr><th>날짜</th><th>메뉴</th></tr>
        """
        for d_l, m_l, d_d, m_d in zip(ymd_lunch, meal_lunch, ymd_dinner, meal_dinner):
            if d_l != d_d:
                html_content += f"<tr><td>{d_l}</td><td>{m_l}</td></tr>"
            else:
                html_content += f"<tr><td>{d_l}</td><td>{m_l}<br/><br/>{m_d}</td></tr>"
        html_content += "</table></body></html>"
        return html_content

    class SimpleHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path == '/':
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(generate_html().encode('utf-8'))
                return

    with socketserver.TCPServer(("", 8000), SimpleHTTPRequestHandler) as httpd:
        print("서버 시작")
        httpd.serve_forever()
else:
    print("Failed to fetch data. Status code:", response.status_code)
