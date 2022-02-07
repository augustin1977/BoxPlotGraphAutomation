import os

import tkinter as tk
from tkinter import filedialog
import boxPlot

class Tela:
    def __init__(self):
        self.root= tk.Tk()
        self.root.title('Abrir Arquivo')
        #self.linha= tk.Label(self.root,text="Deseja exibir linha com a \nmedia da análise de referencia?")
        #self.linha.pack()
        self.linha2=tk.Label(self.root,text="\n\n",fg='red')
        self.linha2.pack(side=tk.BOTTOM,fill='both',expand=True)
        self.chkValue = tk.BooleanVar() 
        self.caixa=tk.Checkbutton(self.root,text="Deseja exibir linha com a \nmedia da análise de referencia?",var=self.chkValue)
        self.caixa.pack()
        self.botao1=tk.Button(self.root,text="Executar Box-Plot",command=self.executaboxplot)
        self.botao1.pack(side=tk.RIGHT)
        self.botao2=tk.Button(self.root,text="Selecionar Arquivo",command=self.carregaArquivo)
        self.botao2.pack(side=tk.LEFT)
        self.arquivo=""
        self.nome=""
    def carregaArquivo(self):
        self.arquivo=filedialog.askopenfilename()
        self.nome=self.arquivo
        self.linha2['text']= "arquivo selecionado:\n"+ajustaLinha(self.arquivo,40)
        
    def getNomearquivo(self):
        return self.arquivo
    def getmedia(self):
        return self.chkValue.get()
    def executaboxplot(self):
        try :
            if (self.getNomearquivo()!=""):
                numero_cabecalhos_e_dados_ok = boxPlot.geraPlot(self.arquivo, self.getmedia())
                if numero_cabecalhos_e_dados_ok : 
                    self.root.destroy()
                else:
                    self.linha2['text']="Numero de cabeçalhos e colunas incorreta!\nVerifique se todas as colunas tem cabeçalho!"             
            else:
                self.linha2['text']="Verifique se selecionou um Arquivo"
        except Exception as err:
            self.linha2['text']=ajustaLinha("Ocorreu um erro"+str(err),40)
def ajustaLinha(palavra,tamanho):
    if len(palavra)>tamanho:
            for a in range(tamanho,len(palavra),tamanho):
                palavra=palavra[:a]+"\n"+palavra[a:]
    return palavra    