import os
from selenium import webdriver
from flask import Flask, request, jsonify

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False

def handler(request):
    # Set CORS headers for the preflight request
    if request.method == "OPTIONS":
        # Allows POST requests from any origin with the Content-Type
        # header and caches preflight response for an 3600s
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max_Age': '3600'
        }

        return ('allow CORS', 204, headers)

    # Set CORS headers for the main request
    headers = {
        'Access-Control-Allow-Origin': '*'
    }

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1280x1696')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--hide-scrollbars')
    chrome_options.add_argument('--enable-logging')
    chrome_options.add_argument('--log-level=0')
    chrome_options.add_argument('--v=99')
    chrome_options.add_argument('--single-process')
    chrome_options.add_argument('--ignore-certificate-errors')

    request_json = request.get_json(silent=True)
    #request_args = request.args # for "GET"

    chrome_options.binary_location = os.getcwd() + "/headless-chromium"    
    driver = webdriver.Chrome(os.getcwd() + "/chromedriver",chrome_options=chrome_options)

    # 図書カード残額確認のページにアクセスする
    driver.get('https://www.toshocardnext.ne.jp/tosho/pc/CardUserLoginPage/open.do')
    print(driver.current_url)

    # ID番号のフォームに入力
    id_form = driver.find_element_by_xpath('/html/body/form/table/tbody/tr/td/table[2]/tbody/tr[1]/td/table[1]/tbody/tr/td[4]/table/tbody/tr[3]/td/input')
    id_form.send_keys(request_json['id'])

    # pinのフォームに入力
    pin_form = driver.find_element_by_xpath('/html/body/form/table/tbody/tr/td/table[2]/tbody/tr[1]/td/table[1]/tbody/tr/td[4]/table/tbody/tr[5]/td/input')
    pin_form.send_keys(request_json['pin'])
    
    # ログインボタンをクリック
    login_btn = driver.find_element_by_xpath('/html/body/form/table/tbody/tr/td/table[2]/tbody/tr[1]/td/table[3]/tbody/tr[2]/td[1]/input')
    login_btn.click()

    # 残額を出力
    elements_balance = driver.find_elements_by_xpath('/html/body/table/tbody/tr/td/table[2]/tbody/tr/td/div/ul[3]/li[2]/p')
    balance = elements_balance[0].text
    print(balance)

    # 有効期限を出力
    elements_date = driver.find_elements_by_xpath('/html/body/table/tbody/tr/td/table[2]/tbody/tr/td/div/ul[2]/li[2]/p')
    date = elements_date[0].text
    print(date)

    driver.quit()

    return (jsonify({"balance":balance, "date":date}), 200, headers)

@app.route('/')
def index():
    return handler(request)

if __name__ == "__main__":
    app.run(port=8000)
