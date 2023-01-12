from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd


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

navegador.get('https://www.google.com.br/')

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
