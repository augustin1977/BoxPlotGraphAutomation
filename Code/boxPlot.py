import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import xlrd

#----------------funções auxiliares ------------------
def inverteDicionario(dicionario):
	#função que recebe um dicionario e devolve um outro dicionario igual, mas com a ordem do elementos invertidos
	#obs: não inverte chave com atributo, somente a ordem dos elementos dentro do dicionário

    chaves=[]
    for chave in dicionario.keys():
        chaves.append(chave)
    chaves.reverse()
    dicionarioInvertido={}
    for chave in chaves:
        dicionarioInvertido[chave]=dicionario[chave]
    return dicionarioInvertido
def geraPlot(arquivo, comMedia, comMediannaBarra,comMediaBarra):
    # ------------- Definições padrões--------------------
    # define tamanho dos textos
    tamanho_texto_super_pequeno="xx-small"
    tamanho_texto_pequeno="small"
    tamanho_texto_normal="large"
    tamanho_texto_grande="x-large"
    # define Verde da média
    verde="#008000"
    #define vermelho da mediana
    vermelho='#950070'
    # cria lista de cores 
    cor=['yellow','orange','pink','lightgreen','green','lightblue','blue','purple', 'brown','gray','black']
    #cor=['yellow','pink','lightblue','red','gray', 'brown','lightgreen','black','purple']
    #endereço do arquivo
    #arquivo= r'C:\Users\ericaugustin\Documents\Prototipos\2021\Box-Plot\boxplot.xls'

    # ------------- Programa--------------------
    # puxando dados planilha
    w = xlrd.open_workbook(arquivo) 

    #define planilha que vai extrair dados

    sheet = w.sheet_by_index(0) # selecionando a segunda planilha

    nomes = sheet.row_values(0) #pega todos os valores da primeira linha (nomes)
    # busca atributos na coluna 2 (1)
    atributos_grafico = sheet.col_values(1)
    #print(atributos_grafico)
    titulo=atributos_grafico[0]
    eixoX= atributos_grafico[1]
    eixoY = atributos_grafico[2]
    numero_ensaios= int(atributos_grafico[3])+1
     

    #Numero de colunas da planilha
    #cols = sheet.ncols # opção antiga
    cols=0
    for i in nomes:
        if (i!=""):
            cols+=1
    if (cols>20):
        tamanho_texto=tamanho_texto_super_pequeno
    elif (cols>10):
        tamanho_texto=tamanho_texto_pequeno
    else:
        tamanho_texto=tamanho_texto_normal

    # busca as familias dos ensaios na planilha
    familias = sheet.row_values(59)[3:]

    #cria biblioteca de cores
    corGrafico={}
    j=0;
    for i in familias:
        if i not in corGrafico:
            if (str(i).upper()=="REFERENCIA"or str(i).upper()=="REFERÊNCIA" or str(i).upper()=="REF" or str(i).upper()=="REFERENCE"):
                numero_linha_media_referencia=j
                corGrafico[i]='red'
            else:
                corGrafico[i]=cor[j];
            j=j+1

    #inverte o dicionário para manter o padrão na primeira posição da legenda
    corGrafico=inverteDicionario(corGrafico)

    #Define numero de ensaios
    rows=numero_ensaios
    # busca dados de linahs e colunas excluindo a primeira linha e as 3 primeiras colunas
    col_data = [sheet.row_values(i, 3, cols) for i in range(rows)]
    row_data = [sheet.col_values(i, 1, rows) for i in range(2,cols)]

    # monta matriz clean e media
    clean = []
    media=[]

    #Faz p calculo da media e monta a matriz clean limpando os valores vazios ou strings ou outros erros
    for i in range(1,cols-2):
            c = row_data[i]	
            erro=True
            # Parte do principio que tem um erro e entra no loop para verificar
            while(erro):
                try:
                    # se detecta erro despreza o valor do vetor fazendo pop no except
                    media.append(np.average(c))
                    # se não encontra erra faz erro = false e sai do loop
                    erro=False
                except:
                    # excluir o ultimo numero do vetor até não acontecer mais erros
                    c.pop(len(c)-1)

            # adiciona a linha c no vetor clean 	
            clean.append(c)

    # criando area de plotagem e definindo variaves globais como nome do grafico
    fig1, ax1 = plt.subplots()



    # agrupando colunas de dados no [dataset] e nomesdas colunas no [nomes] usando numpy
    #dataset=np.array(clean,float) # não mais utilizado devido refatoração do codigo
    dataset=clean


    #nomes= np.array(["Nome1","Nome2","Nome3"]) # não mais utilizado devido refatoração do codigo
    #nomes=nomes[3:numero_ensaios+2]
    nomes=nomes[3:]
    if (len(nomes)==len(dataset)):
        print("Numero de nomes:",len(nomes))
        print("numero de dados:",len(dataset))

        # cria propriedades da linha de media e da mediana
        if comMediannaBarra:
            propriedades_medianas={'color':vermelho,'linewidth':1.5}
        else:
            propriedades_medianas={'color':vermelho,'linewidth':0}
        if comMediaBarra:
            propriedades_medias={"linestyle":"-","color":verde}
        else:
            propriedades_medias={"linestyle":"-","color":verde}
        # cria boxplot mostrando medias e linha de medias(showmean e meanline True) com dados na vertical (vert=False) sem outliers(showfliers=False) 
        #graf=ax1.boxplot(dataset,labels=nomes,vert=False,showmeans=True,meanline=True,medianprops=propriedades_medianas,meanprops=propriedades_medias,flierprops={"marker":"+"},patch_artist=True,showfliers=False)

        # cria boxplot mostrando medias e linha de medias(showmean e meanline True) com dados na vertical (vert=False) com outliers
        graf=ax1.boxplot(dataset,labels=nomes,vert=False,showmeans=comMediaBarra,meanline=comMediaBarra,medianprops=propriedades_medianas,meanprops=propriedades_medias,flierprops={"marker":"+"},patch_artist=True)

        # Coloca um texto com o valor da média de cada coluna no grafico
        if comMediaBarra:
            if len(media)<3:
                offset=1.1
            elif len(media)<4:
                offset=1.2
            else:
                offset=1.3
            for i in range(len(media)):
                if media[i]>1000000:
                    ax1.text(media[i],i+offset,"{:d}".format(media[i]),size=tamanho_texto,color=verde,horizontalalignment ='center')
                elif media [i]>1000:
                    ax1.text(media[i],i+offset,"{:.1f}".format(media[i]),size=tamanho_texto,color=verde,horizontalalignment ='center')
                elif media [i]>1:
                    ax1.text(media[i],i+offset,"{:.2f}".format(media[i]),size=tamanho_texto,color=verde,horizontalalignment ='center')
                elif media [i]>0.0001:
                    ax1.text(media[i],i+offset,"{:.4f}".format(media[i]),size=tamanho_texto,color=verde,horizontalalignment ='center')
                else:
                    ax1.text(media[i],i+offset,"{}".format(media[i]),size=tamanho_texto,color=verde,horizontalalignment ='center')
            
        # define titulo do grafico e dos eixos
        ax1.set_title(titulo, fontsize=tamanho_texto_grande,fontweight="bold")
        ax1.set_xlabel(eixoX,fontsize=tamanho_texto_normal,fontweight="bold")
        ax1.set_ylabel(eixoY,fontsize=tamanho_texto_normal,fontweight="bold")

        #ajustes de posições para melhor enquadramento
        fig1.subplots_adjust(left=0.17,right=0.98,top=0.96,bottom=0.07)

        # Faz a linha media do ensaio de referencia  se comMedia=True(ultimo)
        print(comMedia)
        if comMedia:
            ax1.axvline(media[numero_linha_media_referencia], ymin=0, ymax=len(media),linewidth=1, color=verde,linestyle=':')

        # exibe linha de grade
        #ax1.yaxis.grid(True)
        #ax1.xaxis.grid(True)

        # pinta cada boxplot com a cor de sua familia
        legenda=[] 
        # cria legenda
        for patch, color in zip(graf['boxes'], familias):  
            patch.set_facecolor(corGrafico[color])

        
        
        # define a cor de cada legenda e seus nomes      
        #print(corGrafico)
        for f in corGrafico:
            legenda.append(mpatches.Patch(corGrafico[f],facecolor=corGrafico[f], label=f))
        #constroi a legenda
        ax1.legend(handles=legenda).set_draggable(True)
        # mostra o grafico
        plt.show()
        return True
    else:
        return False
