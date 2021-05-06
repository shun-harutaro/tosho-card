from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

# x. Chrome の起動オプションを設定する
options = Options()
options.add_argument('--headless')

# seleniumサーバーに接続
print('connectiong to remote browser...')
driver = webdriver.Remote(
    command_executor='http://localhost:4444/wd/hub',
    desired_capabilities=options.to_capabilities(),
    options=options,
)

# 1. Qiita の Chanmoro のプロフィールページにアクセスする
driver.get('https://www.toshocardnext.ne.jp/tosho/pc/CardUserLoginPage/open.do')
print(driver.current_url)

# ID番号のフォームに入力
id_form = driver.find_element_by_xpath('/html/body/form/table/tbody/tr/td/table[2]/tbody/tr[1]/td/table[1]/tbody/tr/td[4]/table/tbody/tr[3]/td/input')
id_form.send_keys('1119490082825296')

# pinのフォームに入力
pin_form = driver.find_element_by_xpath('/html/body/form/table/tbody/tr/td/table[2]/tbody/tr[1]/td/table[1]/tbody/tr/td[4]/table/tbody/tr[5]/td/input')
pin_form.send_keys('3664')

# ログインボタンをクリック
login_btn = driver.find_element_by_xpath('/html/body/form/table/tbody/tr/td/table[2]/tbody/tr[1]/td/table[3]/tbody/tr[2]/td[1]/input')
login_btn.click()

# 残額を出力
balance = driver.find_elements_by_xpath('/html/body/table/tbody/tr/td/table[2]/tbody/tr/td/div/ul[3]/li[2]/p')
print(balance[0].text)

# 有効期限を出力
date = driver.find_elements_by_xpath('/html/body/table/tbody/tr/td/table[2]/tbody/tr/td/div/ul[2]/li[2]/p')
print(date[0].text)

driver.quit()
