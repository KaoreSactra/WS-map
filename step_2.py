from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from PySimpleGUI import PySimpleGUI as Sg
from bs4 import BeautifulSoup
from time import sleep
import pandas as Pd

class App:
    def __init__(self):
        self.opts = webdriver.ChromeOptions()
        self.opts.add_experimental_option("detach", True)
        # ↓ Opções (fazem o google n fechar sozinho)
        self.opts.add_argument("--disable-notifications")
        # ↓ Serviço (Pega a versão driver compatível com o navegador)
        self.serv = Service(ChromeDriverManager().install())
        # ↓ Inicia o navegador
        self.nav = webdriver.Chrome(options=self.opts,service=self.serv)
        self.nav.minimize_window()

    def init(self):
        self.janela()

    def janela(self):
        # ↓ Tema e Layout
        Sg.theme('DarkPurple3')
        self.layout = [
            [Sg.Text('Quais lugares gostaria de procurar?')],
            [Sg.Input(key='local'), Sg.Button("Buscar")]
        ]
        # ↓ Janela inicial
        self.painel = Sg.Window('Step 2', self.layout)
        # ↓ While para rodar janela
        while True:
            event, value = self.painel.read()
            if event == Sg.WIN_CLOSED:
                self.nav.close()
                break
            if event == "Buscar":
                self.search(local=value['local'])
                sleep(0.5)
                try:
                    self.get_infos()
                except:
                    print("Erro ao puxar infos")
                try:
                    self.save_infos(local=value['local'])
                except:
                    print("Erro ao salvar infos")
                    self.nav.close()
                    self.painel.close()
        self.painel.close()

    def search(self, local):
        self.nav.maximize_window()
        self.lista_locais=[]
        self.nav.get('https://www.google.com/maps')
        self.nav.find_element('id', 'searchboxinput').send_keys(local)
        self.nav.find_element('id', 'searchbox-searchbutton').click()
        sleep(2)

    def get_infos(self):
        for a in range(3, 13, 2):
            self.nav.find_element('xpath', f'//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[1]/div[1]/div[{a}]/div/a').click()
            sleep(0.5)
            self.page_content = self.nav.page_source
            self.site = BeautifulSoup(self.page_content, 'html.parser')
            self.lugar = self.site.find('div', attrs={'jstcache': '4'})
            try:
                self.get_name()
            except:
                print("Erro ao puxar nomes")
            try:
                self.get_num()
            except:
                print("Erro ao puxar números")
            try:
                self.get_address()
            except:
                print("Erro ao puxar endereços")
            self.lista_locais.append([self.lugar_nome, self.lugar_num, self.lugar_local])
            sleep(1)

    def get_name(self):
        self.lugar_nome = self.lugar.find('h1').text

    def get_num(self):
        self.lugar_num = self.lugar.find('button', attrs={'data-tooltip': 'Copiar número de telefone'}).text

    def get_address(self):
        self.lugar_local = self.lugar.find('button', attrs={'data-tooltip': 'Copiar endereço'}).text

    def save_infos(self, local):
        self.infos = Pd.DataFrame(self.lista_locais, columns=['Nome', 'Número', 'Endereço'])
        self.infos.to_excel(f'Locais em xlsx\{local}.xlsx', index=False)
        self.infos.to_string(f'Locais em txt\{local}.txt', index=False)
        sleep(0.1)
        self.nav.close()
        self.painel.close()

start = App()
start.init()