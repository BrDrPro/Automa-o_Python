from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time

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

driver.execute_script("""
    document.querySelector('[id="fechar"]').click()
""")

driver.switch_to.default_content()

driver.execute_script("""
    document.querySelector("body > cookies-policy").shadowRoot.querySelector("soma-context > cookies-policy-disclaimer > div > soma-card > div > div.uWq1-disclaimer-button-wrapper > soma-button.uWq1-disclaimer-button.soma-button.secondary.md.inverse.hydrated").shadowRoot.querySelector("button").click()
""")

actions = ActionChains(driver)

for row in rows:
    link = row.find_element(by='css selector',value='a')    
    actions.move_to_element(link).click().perform()
    time.sleep(10)
