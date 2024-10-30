import os

# import numpy as np

professores = {"ESE": "Esequia Sauter",
               "FSA": "Fabio Azevedo",
               "LGD": "Leonardo Guidi",
               "JBC": "João Batista",
               "IRE": "Irene Strauch",
               "E_F": "Esequia/Fabio"}

# Pode-se inserir "h":"A1", "H":"A2 etc.
turmas = {"A": "A","A1": "A1","A2": "A2", "B": "B", "C": "C", "C1": "C1", "C2": "C2", "D": "D"}

template_area = r"""
        <tr>
          <td><a href="___DIRNAME___/___FILENAME___"> ___DESCRICAO___</a></td>
          <td></td>
          <td>___GABARITO___</td>
        </tr>
"""
template_gabarito = r"""<a href="___DIRNAME___/___FILENAME___">Gabarito</a>"""


def main():
    with open("template_provas.tl", "r") as f:
        template_pagina = f.read()

    texto_final = template_pagina \
        .replace("___PROVAS___VETORIAL___", completa_template_area("Vetorial")) \
        .replace("___PROVAS___LAPLACE___", completa_template_area("Laplace")) \
        .replace("___PROVAS___FOURIER___", completa_template_area("Fourier"))

    arq = "provas.html"
    with open(arq, "w") as f:
        f.write(texto_final)
    print(f"Arquivo {arq} criado com sucesso.")


# provaAAAAS_T_PRO[gab].pdf" aaaa=ano  S=semestre T=turma PRO=professor
def parse_nome(nome): 

    # Testa que início e extensão do nome de arquivo.
    if not nome.startswith("prova"):
        print("Não é prova:", nome)
        return None

    if not nome.endswith(".pdf"):
        print("Não é pdf:", nome)
        return None

    # Remove início e final do nome e quebra em substrings
    partes = nome[5: -4].split("_")
    n_partes = len(partes)

    # Verifica se é gabarito de prova.
    gab = n_partes > 3 and partes[3] == "gab"
    
    if not ((n_partes == 3 and not gab) or (n_partes == 4 and gab)):
        print("Formato inválido:", nome)

    ano_semestre, turma, prof = partes[:3]

    try:
        ano = ano_semestre[:4]
        semestre = ano_semestre[4]
        ano_int = int(ano)
        semestre_int = int(semestre)
    except ValueError:
        print("Ano inválido ou semestre inválido inválido:", nome)
        return None

    if turma not in turmas:
        print("Turma inválida:", turma)
        return None

    if not (2010 < ano_int < 2040):
        print("Tem certeza que o ano está correto?!:", ano_int)
        return None

    if not (1 <= semestre_int <= 2):
        print("Semestre inválido:", semestre_int)
        return None

    if prof not in professores:
        print("Professor inválido:", prof)
        return None

    nome_prof = professores[prof]
    # print((turma, ano, semestre, gab, nome_prof))
    return (turma, ano, semestre, gab, nome_prof)


def completa_template_area(sdirname):
    provas = {}
    gabaritos = {}

    for nome in os.listdir(sdirname):
        if "pdf" != nome[-3:]:
            continue

        p = parse_nome(nome)
        if p is None:
            print("Erro!!  ", nome)
            quit()

        turma, ano, semestre, gab, nome_prof = p

        if gab:
            # print(nome)
            gabaritos[(turma, ano, semestre, nome_prof)] = nome
        else:
            provas[(turma, ano, semestre, nome_prof)]    = nome

    lista_provas = []

    for dados_prova in provas:
        turma_key, ano, semestre, nome_prof = dados_prova
        turma = turma_key

        # Verifica se a prova tem um gabarito associado
        gab = dados_prova in gabaritos

        comentario = f"Turma {turma} {ano}/{semestre} - prof. {nome_prof}"
        if gab:
            texto_gabarito = template_gabarito \
                .replace("___DIRNAME___", sdirname) \
                .replace("___FILENAME___", gabaritos[dados_prova])
        else:
            texto_gabarito = ""

        texto_questao = template_area\
            .replace("___DIRNAME___", sdirname) \
            .replace("___FILENAME___", provas[dados_prova]) \
            .replace("___DESCRICAO___", comentario) \
            .replace("___GABARITO___", texto_gabarito)

        lista_provas.append((ano, semestre, turmas[turma], texto_questao))

    # Ordem decrescente do ano/semestre, mas crescente na turma
    lista_provas.sort(
        reverse=True,
        key=lambda x: (x[0], x[1], [-ord(t) for t in x[2]], x[3])
    )

    texto_final = "\n".join([t[-1] for t in lista_provas])
    # print(texto_final)
    return texto_final


main()
