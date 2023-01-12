from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--window-size=1920x1080')
options.add_argument('--verbose')
options.add_argument('--headless')  # if you want it headless
options.add_argument('--no-sandbox')
options.add_argument('--enable-automation')
options.add_argument('--disable-gpu')

display = Display(visible=0, size=(800, 600))
display.start()

options.BinaryLocation = '/usr/bin/chromium-browser'
service = Service('/usr/bin/chromedriver')

self.driver = webdriver.Chrome(service=service, options=options)

navegador = webdriver.Chrome()   # indicando o navegador a ser usado
navegador.get('https://www.google.com.br/')

navegador.find_element(
    By.XPATH,
    '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input',
).send_keys(('cotação dólar'))
navegador.find_element(
    By.XPATH,
    '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input',
).send_keys(Keys.ENTER)
cotacao_dolar = navegador.find_element(
    By.XPATH,
    '//*[@id="knowledge-currency__updatable-data-column"]/div[1]/div[2]/span[1]',
).get_attribute('data-value')

navegador.find_element(
    By.XPATH,
    '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input',
).send_keys(('cotação euro'))
navegador.find_element(
    By.XPATH,
    '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input',
).send_keys(Keys.ENTER)
cotacao_euro = navegador.find_element(
    By.XPATH,
    '//*[@id="knowledge-currency__updatable-data-column"]/div[1]/div[2]/span[1]',
).get_attribute('data-value')

navegador.get('https://www.melhorcambio.com/ouro-hoje')
cotacao_ouro = navegador.find_element(
    By.XPATH, '//*[@id="original"]'
).get_attribute('value')
cotacao_ouro = cotacao_ouro.replace(',', '.')

tabela = pd.read_excel('Produtos.xlsx')
tabela.loc[tabela['Moeda'] == 'Dólar', 'Cotação'] = float(cotacao_dolar)
tabela.loc[tabela['Moeda'] == 'Euro', 'Cotação'] = float(cotacao_euro)
tabela.loc[tabela['Moeda'] == 'Ouro', 'Cotação'] = float(cotacao_ouro)

tabela['Preço de Compra'] = tabela['Preço Original'] * tabela['Cotação']
tabela['Preço de Venda'] = tabela['Preço de Compra'] * tabela['Margem']

tabela.to_excel('Produtos Novos.xlsx', index=False)
