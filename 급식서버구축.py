import http.server
import socketserver
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# 현재 날짜와 시간 가져오기
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
    ymd = [tag.text[6:] for tag in ymd_tags]

    meal_tags = soup.find_all('DDISH_NM')
    meal = [tag.text for tag in meal_tags]

    meal_type_tags = soup.find_all('MMEAL_SC_NM')
    meal_types = [tag.text for tag in meal_type_tags]

    lunch_data = []
    dinner_data = []

    for i in range(len(ymd)):
        if meal_types[i] == "중식":
            lunch_data.append((ymd[i], meal[i]))
        elif meal_types[i] == "석식":
            dinner_data.append((ymd[i], meal[i]))

    # 날짜에 맞게 중식과 석식을 병합
    merged_data = {}
    for date, menu in lunch_data:
        if date not in merged_data:
            merged_data[date] = {"lunch": menu, "dinner": ""}
        else:
            merged_data[date]["lunch"] = menu

    for date, menu in dinner_data:
        if date not in merged_data:
            merged_data[date] = {"lunch": "", "dinner": menu}
        else:
            merged_data[date]["dinner"] = menu

    # HTML 생성 함수
    def generate_html():
        html_content = f"""
        <html>
        <head>
            <meta charset="UTF-8">
            <title>급식 정보</title>
            <style>
                body {{
                    display: flex;
                    justify-content: center;
                    align-items: flex-start;
                    height: 100%;
                    margin: 0;
                    font-family: Arial, sans-serif;
                    padding: 20px;
                }}
                .table-container {{
                    overflow: auto;
                    max-height: 90vh;
                    width: 80%;
                    margin: auto;
                }}
                table {{
                    border-collapse: collapse;
                    width: 100%;
                    border-collapse: separate;
                    border-spacing: 0 10px;
                    top: 0;
                    margin-left:auto;
                    margin-right:auto;
                }}
                th, td {{
                    border: 1px solid #dddddd;
                    text-align: left;
                    padding: 8px;
                    text-align: center;
                    border: 3px solid rgb(0, 0, 0);
                    font-size: 20px;
                    padding-top: 0px;
                    padding-bottom: 0px;
                    font-weight : bolder;
                    border-radius: 10px;
                }}
                th {{
                    background-color: #f2f2f2;
                }}
                tr:nth-child(even) {{
                    background-color: #f9f9f9;
                }}
            </style>
        </head>
        <body>

                <table>
                    <tr><th>날짜</th><th>반곡고 {current_month}월 메뉴</th></tr>
        """
        for date, menus in sorted(merged_data.items()):
            combined_menu = menus['lunch']
            if menus['dinner']:
                combined_menu += f"<br/><br/>{menus['dinner']}"
            html_content += f"<tr><td>{date}</td><td>{combined_menu}</td></tr>"
        html_content += "</table></body></html>"
        return html_content

    # 서버 요청 핸들러
    class SimpleHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path == '/':
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(generate_html().encode('utf-8'))
                return

    # 서버 설정 및 실행
    with socketserver.TCPServer(("", 8000), SimpleHTTPRequestHandler) as httpd:
        print("서버 시작")
        httpd.serve_forever()
else:
    print("Failed to fetch data. Status code:", response.status_code)
