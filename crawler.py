from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import sqlite3

db = sqlite3.connect('database.sqlite')

cursor = db.cursor()

options = webdriver.ChromeOptions()
options.add_argument('--disable-notifications')
options.add_argument('--disable-popup-blocking')

driver = webdriver.Chrome(options=options)
URL = "https://www.infomoney.com.br/cotacoes/b3/indice/ibovespa/"
driver.get(URL)

driver.maximize_window()
# table = driver.execute_script("""return document.querySelector("#high > tbody").innerText""")
# print(table)

driver.execute_script("""
    as = document.querySelector("#high > tbody").querySelectorAll('a')
    as.forEach(
        (x)=>{x.setAttribute("target","_blank")}
    )
""")

table = driver.find_element(by='css selector',value="#high > tbody")
rows = table.find_elements(by='css selector',value='tr')

iframe = driver.find_element(by='tag name',value='iframe')
driver.switch_to.frame(iframe)

time.sleep(5)

driver.execute_script("""
    document.querySelector('[id="fechar"]').click()
""")

driver.switch_to.default_content()

try: 
    driver.execute_script("""
        document.querySelector("body > cookies-policy").shadowRoot.querySelector("soma-context > cookies-policy-disclaimer > div > soma-card > div > div.uWq1-disclaimer-button-wrapper > soma-button.uWq1-disclaimer-button.soma-button.secondary.md.inverse.hydrated").shadowRoot.querySelector("button").click()
    """)
except Exception as e: 
    pass

actions = ActionChains(driver)

for row in rows:
    link = row.find_element(by='css selector',value='a')    
    actions.move_to_element(link).click().perform()
    driver.switch_to.window(driver.window_handles[1])
    print(driver.current_url)

    table_dict = {}
    Upper_table = driver.find_element(by='css selector',value="#header-quotes > div.tables > table:nth-child(1) > tbody")
    Upper_table_rows = Upper_table.find_elements(by='css selector',value='tr')
    for upper_table_row in Upper_table_rows:
        key = upper_table_row.find_elements(by='css selector',value='td')[0].text
        value = upper_table_row.find_elements(by='css selector',value='td')[1].text
        table_dict[key] = value

    Lower_table = driver.find_element(by='css selector',value="#header-quotes > div.tables > table:nth-child(2) > tbody")
    Lower_table_rows = Lower_table.find_elements(by='css selector',value='tr')
    for lower_table_row in Lower_table_rows:
        key = lower_table_row.find_elements(by='css selector',value='td')[0].text
        value = lower_table_row.find_elements(by='css selector',value='td')[1].text
        table_dict[key] = value
    print(table_dict)

    cursor.execute('''insert into ativos (details) values (?)''', (str(table_dict),))
    db.commit()

    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(5)
