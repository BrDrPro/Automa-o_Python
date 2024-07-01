from selenium import webdriver
import time

driver = webdriver.Chrome()
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

for row in rows:
    link = row.find_element(by='css selector',value='a')
    link.click()
    time.sleep(10)
