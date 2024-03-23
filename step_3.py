from PySimpleGUI import PySimpleGUI as Sg
from time import sleep
import pywhatkit
import os

class App:
    def init(self):
        self.janela()

    def janela(self):
        # ↓ Tema e Layout
        Sg.theme('DarkPurple3')
        self.numbers = []
        self.list_numbers = Sg.Listbox(self.numbers, key='list', size=(30, 10))
        self.layout = [
            [Sg.Text('Escreva o telefone (ex: 11 4002-8922)')],
            [Sg.Input(key='number', size=(28)), Sg.Button('+'), Sg.Button('Enviar Mensagem', size=(19))],
            [self.list_numbers, Sg.Multiline(key='text', size=(20, 10))],
            [Sg.Button('Apagar'), Sg.Button('Limpar')]
        ]
        # ↓ Janela inicial
        self.painel = Sg.Window('Step 3', self.layout)
        # ↓ While para rodar janela
        while True:
            event, value = self.painel.read()
            if event == Sg.WIN_CLOSED:
                break
            elif event == '+':
                if value['number'] != '':
                    self.numbers.append(value['number'])
                    self.painel['list'].update(self.numbers)
                else:
                    print('Sem número inserido')
            elif event == 'Apagar':
                try:
                    val = self.list_numbers.get()[0]
                    self.numbers.remove(val)
                    self.painel['list'].update(self.numbers)
                except:
                    print('Não selecionado')
            elif event == 'Limpar':
                self.numbers=[]
                self.painel['list'].update(self.numbers)
            elif event == 'Enviar Mensagem':
                if value['text'] != '':
                    self.send_message(message=value[f'text'], number='+55'+(self.list_numbers.get()[0]))
                else:
                    print('Sem mensagem escrita')
        self.painel.close()

    def send_message(self, message, number):
        pywhatkit.sendwhatmsg_instantly(number, message, 7, True, 3)
        os.remove('PyWhatKit_DB.txt')

start = App()
start.init()