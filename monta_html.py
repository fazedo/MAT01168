import sys
import os

# import numpy as np

professores = {"ESE":"Esequia Sauter",
               "FSA":"Fabio Azevedo",
               "LGD":"Leonardo Guidi",
               "JBC":"João Batista",
               "IRE":"Irene Strauch",
               "E_F":"Esequia/Fabio"}

turmas = {"A":"A", "B":"B", "C":"C", "D":"D"} ## pode-se inserir "h":"A1", "H":"A2 etc.

template_area = r"""
        <tr>
          <td><a href="___DIRNAME___/___FILENAME___"> ___DESCRICAO___</a></td> 
          <td></td>
          <td>___GABARITO___</td>
        </tr>
"""
template_gabarito = r"""<a href="___DIRNAME___/___FILENAME___">Gabarito</a>"""

def parse_nome(nome): # provaAAAAS_T_PRO[gab].pdf" aaaa=ano  S=semestre T=turma PRO=professor
    gab = nome[17:20] == "gab" # isso não é um erro mesmo que a string tenha menos de 20 caracteres.
    
    l = len(nome)   
    l_valido = (l == 20 and not gab) or (l == 24 and gab) # há apenas dois comprimentos válidos
    
    if  not l_valido:
        print("Nome de arquivo inválido:", l)
        return None
    
    # A partir daqui, sabe-se que nome tem pelo menos 20 caracteres

    if nome[10] != "_" or nome[12] != "_" or (gab and nome[16] != "_"):
        print("Nome de arquivo inválido.")
        return None
        
    if  nome[0:5] != "prova": 
        print("Não é prova:", nome)
        return None
    
    if  nome[-4:] != ".pdf": 
        print("Não é .pdf:", nome)
        return None
    
    # numero   = nome[5] # só serve para testar o nome do arquivo - excluido
    ano      = nome[5:9]
    semestre = nome[9]
    turma    = nome[11]
    prof     = nome[13:16]
    
    if turma not in turmas:
        print("Turma inválida:", turma)
        return None

    try:
        ano_int = int(ano)
        semestre_int = int(semestre)
        # numero_int = int(numero)
    except:
        print("Ano inválido ou semestre inválido inválido:", ano, semestre) # ou número
        return None

    if not (2010 < ano_int < 2040):
        print("Tem certeza que o ano está correto?!:", ano)
        return None

    if not (1 <= semestre_int <= 2):
        print("Semestre inválido:", semestre)
        return None

#    if not (1 <= numero_int <= 3):
#       print("Que área é essa, tchê? ", numero)
#        return None


    if prof not in professores:
        print("Professor inválido:", prof)
        return None
    
    nome_prof = professores[prof]

    # print(turma, ano, semestre, gab, nome_prof)
    return (turma, ano, semestre, gab, nome_prof)




def completa_template_area(sdirname):
    provas    = {}
    gabaritos = {}
    
    for nome in os.listdir(sdirname):
        if "pdf" != nome[-3:]:
            continue

        p = parse_nome(nome)
        if p == None:
            print("Erro!!  ", nome)
            quit()
        
        turma, ano, semestre, gab, nome_prof = p

        ## Vou guardar em dicionários por mais que o nome tenha formato fixo.
        ## Talvez queiramos mudar algo no futuro.
        ## As chaves dos gabaritos são tuplas, é muito estranho não usar os nomes, mas me parece mais flexível.

        if gab:
            gabaritos[(turma, ano, semestre, nome_prof)] = nome
        else:
            provas[(turma, ano, semestre, nome_prof)] = nome


    lista_provas = []

    for prova in provas:
        (turma, ano, semestre, nome_prof) = prova
        gab = prova in gabaritos

        nome_arq = provas[prova]
        comentario = f"Turma {turmas[turma]} {ano}/{semestre} - prof. {nome_prof}"
        texto_gabarito = template_gabarito.replace("___DIRNAME___", sdirname)\
                                        .replace("___FILENAME___", gabaritos[prova]) if gab else ""
        
        texto_questao = template_area.replace("___DIRNAME___", sdirname)     \
                                     .replace("___FILENAME___", nome_arq)    \
                                     .replace("___DESCRICAO___", comentario) \
                                     .replace("___GABARITO___", texto_gabarito)
        
        lista_provas.append((ano, semestre, turmas[turma], texto_questao))

    lista_provas.sort(reverse=True, key=lambda x:(x[0], x[1], [-ord(t) for t in x[2]], x[3])) # ordem decrescente do ano/semestre, mas crescente na turma
    texto_final = "\n".join([t[-1] for t in lista_provas])
    # print(texto_final)
    return texto_final


with open("template_provas.tl", "r") as f:
    template_pagina = f.read()

# print(template_pagina)

texto_final = template_pagina.replace("___PROVAS___VETORIAL___", completa_template_area("Vetorial"))\
                             .replace("___PROVAS___LAPLACE___",  completa_template_area("Laplace")) \
                             .replace("___PROVAS___FOURIER___",  completa_template_area("Fourier"))


# print(texto_final)

with open("provas.html", "w") as f:
    f.write(texto_final)