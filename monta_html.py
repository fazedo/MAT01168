import os


professores = {
    "ESE": "Esequia Sauter",
    "FSA": "Fabio Azevedo",
    "LGD": "Leonardo Guidi",
    "JBC": "João Batista",
    "IRE": "Irene Strauch",
    "E_F": "Esequia/Fabio",
}

turmas = {
    "A": "A",
    "A1": "A1",
    "A2": "A2",
    "B": "B",
    "C": "C",
    "C1": "C1",
    "C2": "C2",
    "D": "D",
}


template_area = """
        <tr>
          <td class="prova">
            <a href="___DIRNAME___/___FILENAME___">___DESCRICAO___</a>
          </td>
          <td class="gabarito">
            ___GABARITO___
          </td>
        </tr>
"""

template_gabarito = """
<a class="link-gabarito"
   href="___DIRNAME___/___FILENAME___">Gabarito</a>
"""


def parse_nome(nome):
    """
    Interpreta nomes no formato:

        provaAAAAS_T_PRO.pdf
        provaAAAAS_T_PRO_gab.pdf

    onde:

        AAAA = ano
        S    = semestre
        T    = turma
        PRO  = código do professor
    """

    if not nome.startswith("prova"):
        print("Não é prova:", nome)
        return None

    if not nome.endswith(".pdf"):
        print("Não é PDF:", nome)
        return None

    partes = nome[5:-4].split("_")

    if len(partes) == 3:
        gab = False
    elif len(partes) == 4 and partes[3] == "gab":
        gab = True
    else:
        print("Formato inválido:", nome)
        return None

    ano_semestre, turma, prof = partes[:3]

    if len(ano_semestre) != 5:
        print("Ano/semestre inválido:", nome)
        return None

    try:
        ano = int(ano_semestre[:4])
        semestre = int(ano_semestre[4])
    except ValueError:
        print("Ano ou semestre inválido:", nome)
        return None

    if not 2010 < ano < 2040:
        print("Tem certeza que o ano está correto?!:", ano)
        return None

    if semestre not in (1, 2):
        print("Semestre inválido:", semestre)
        return None

    if turma not in turmas:
        print("Turma inválida:", turma)
        return None

    if prof not in professores:
        print("Professor inválido:", prof)
        return None

    return turma, ano, semestre, gab, prof


def completa_template_area(dirname):
    provas = {}
    gabaritos = {}

    for nome in os.listdir(dirname):
        if not nome.endswith(".pdf"):
            continue

        dados = parse_nome(nome)

        if dados is None:
            raise ValueError(f"Arquivo inválido: {nome}")

        turma, ano, semestre, gab, prof = dados
        chave = (turma, ano, semestre, prof)

        if gab:
            if chave in gabaritos:
                raise ValueError(
                    f"Gabarito duplicado para {chave}: {nome}"
                )

            gabaritos[chave] = nome

        else:
            if chave in provas:
                raise ValueError(
                    f"Prova duplicada para {chave}: {nome}"
                )

            provas[chave] = nome

    lista_provas = []

    for chave, nome_prova in provas.items():
        turma, ano, semestre, prof = chave
        nome_prof = professores[prof]

        comentario = (
            f"Turma {turmas[turma]} "
            f"{ano}/{semestre} - prof. {nome_prof}"
        )

        if chave in gabaritos:
            texto_gabarito = (
                template_gabarito
                .replace("___DIRNAME___", dirname)
                .replace("___FILENAME___", gabaritos[chave])
            )
        else:
            texto_gabarito = ""

        texto_questao = (
            template_area
            .replace("___DIRNAME___", dirname)
            .replace("___FILENAME___", nome_prova)
            .replace("___DESCRICAO___", comentario)
            .replace("___GABARITO___", texto_gabarito)
        )

        lista_provas.append(
            (
                ano,
                semestre,
                turmas[turma],
                nome_prof,
                texto_questao,
            )
        )

    # Ano e semestre em ordem decrescente;
    # turma e professor em ordem crescente.
    lista_provas.sort(
        key=lambda x: (
            -x[0],
            -x[1],
            x[2],
            x[3],
        )
    )

    return "\n".join(item[-1] for item in lista_provas)


def main():
    with open(
        "template_provas.tl",
        "r",
        encoding="utf-8",
    ) as arquivo:
        template_pagina = arquivo.read()

    texto_final = (
        template_pagina
        .replace(
            "___PROVAS___VETORIAL___",
            completa_template_area("Vetorial"),
        )
        .replace(
            "___PROVAS___LAPLACE___",
            completa_template_area("Laplace"),
        )
        .replace(
            "___PROVAS___FOURIER___",
            completa_template_area("Fourier"),
        )
    )

    arquivo_saida = "provas.html"

    with open(
        arquivo_saida,
        "w",
        encoding="utf-8",
    ) as arquivo:
        arquivo.write(texto_final)

    print(f"Arquivo {arquivo_saida} criado com sucesso.")


if __name__ == "__main__":
    main()
