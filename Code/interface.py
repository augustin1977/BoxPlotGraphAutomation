import os

import tkinter as tk
from tkinter import filedialog
import boxPlot

maxSize=60
class Tela:
    def __init__(self):
        self.root= tk.Tk()
        self.root.title('Abrir Arquivo')
       
        self.linha2=tk.Label(self.root,text="\n\n",fg='red')
        self.linha2.pack(side=tk.BOTTOM,fill='both',expand=True)
        self.mediaGeral = tk.BooleanVar() 
        self.caixa=tk.Checkbutton(self.root,text=ajustaLinha("Deseja exibir linha com a media da análise de referencia?",maxSize),justify='left',var=self.mediaGeral)
        self.caixa.pack()
        self.mediaBarra = tk.BooleanVar() 
        self.caixa2=tk.Checkbutton(self.root,text=ajustaLinha("Deseja exibir linha de media nos dados?",maxSize),justify='left',var=self.mediaBarra )
        self.caixa2.pack()
        self.medianaBarra = tk.BooleanVar() 
        self.caixa3=tk.Checkbutton(self.root,text=ajustaLinha("Deseja exibir linha de mediana nos dados?",maxSize),justify='left',var=self.medianaBarra)
        self.caixa3.pack()
        self.botao1=tk.Button(self.root,text="Executar Box-Plot",command=self.executaboxplot)
        self.botao1.pack(side=tk.RIGHT,expand=True)
        self.botao2=tk.Button(self.root,text="Selecionar Arquivo",command=self.carregaArquivo)
        self.botao2.pack(side=tk.LEFT,expand=True)
        self.arquivo=""
        self.nome=""
        self.caixa2.select()
        print(self.mediaGeral.get(), self.mediaBarra.get(), self.medianaBarra.get())
    def carregaArquivo(self):
        self.arquivo=filedialog.askopenfilename()
        self.nome=self.arquivo
        self.linha2['text']= "arquivo selecionado:\n"+ajustaLinha(self.arquivo,maxSize)
        
    def getNomearquivo(self):
        return self.arquivo

    def executaboxplot(self):
        try :
            if (self.getNomearquivo()!=""):
                numero_cabecalhos_e_dados_ok = boxPlot.geraPlot(self.arquivo, self.mediaGeral.get(), self.medianaBarra.get(),self.mediaBarra.get())
                if numero_cabecalhos_e_dados_ok : 
                    self.root.destroy()
                else:
                    self.linha2['text']="Numero de cabeçalhos e colunas incorreta!\nVerifique se todas as colunas tem cabeçalho!"             
            else:
                self.linha2['text']="Verifique se selecionou um Arquivo"
        except Exception as err:
            self.linha2['text']=ajustaLinha("Ocorreu um erro"+str(err),maxSize)
def ajustaLinha(palavra,tamanho=maxSize):
    if len(palavra)>tamanho:
            for a in range(tamanho,len(palavra),tamanho):
                palavra=palavra[:a]+"\n"+palavra[a:]
    else:
        palavra=palavra+" "*(int(tamanho+8)-len(palavra))
    return palavra    