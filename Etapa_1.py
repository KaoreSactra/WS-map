from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from PySimpleGUI import PySimpleGUI as sg
import os

# Opções (fazem o google n fechar sozinho)
opts = webdriver.ChromeOptions()
opts.add_experimental_option("detach", True)
opts.add_argument("--disable-notifications")

# Serviço (Pega a versão driver compatível com o navegador)
serv = Service(ChromeDriverManager().install())
nav = webdriver.Chrome(options=opts,service=serv)
nav.minimize_window()

# Função de procura
def search(local):
    nav.maximize_window()
    nav.get('https://www.google.com/maps')
    nav.find_element('xpath', '//*[@id="searchboxinput"]').send_keys('Padaria')
    nav.find_element('xpath', '//*[@id="searchbox-searchbutton"]').click()

# Tema e Layout
sg.theme('DarkPurple3')
layout = [
    [sg.Text('Oque deseja?')],
    [sg.Input(key='local'), sg.Button("Buscar")]
]

# Janela inicial
janela = sg.Window('Fase 1', layout)

while True:
    event, value = janela.read()
    if event == sg.WIN_CLOSED:
        nav.close()
        break
    if event == "Buscar":
        search(local=value['local'])
janela.close()