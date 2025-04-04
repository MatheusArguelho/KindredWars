import requests
import os
import datetime


def criar_pasta():
    horario = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    pasta = f"Imagens_cartas_{horario}"
    os.makedirs(pasta, exist_ok=True)
    return pasta


def baixar_imagem_carta(nome_carta, pasta):
    url = f"https://api.scryfall.com/cards/named?exact={nome_carta.replace(' ', '+')}"
    resposta = requests.get(url)

    if resposta.status_code != 200:
        print(f"Erro ao buscar a carta {nome_carta}. Verifique o nome e tente novamente.")
        return

    dados_carta = resposta.json()

    if "prints_search_uri" not in dados_carta:
        print(f"Não foi possível encontrar reimpressões para a carta {nome_carta}.")
        return

    prints_url = dados_carta["prints_search_uri"]
    prints_resposta = requests.get(prints_url)

    if prints_resposta.status_code != 200:
        print(f"Erro ao buscar reimpressões da carta {nome_carta}.")
        return

    prints_dados = prints_resposta.json()
    cartas = prints_dados.get("data", [])

    if not cartas:
        print(f"Nenhuma reimpressão encontrada para a carta {nome_carta}.")
        return

    # Filtrar cartas que não são digitais, variações ou promos
    cartas_filtradas = [carta for carta in cartas if
                        not carta.get("digital", True) and not carta.get("variation", True) and not carta.get("promo",
                                                                                                              True)]

    if not cartas_filtradas:
        print(f"Nenhuma versão válida encontrada para {nome_carta}.")
        return

    # Ordenar as cartas pelas datas de lançamento
    cartas_filtradas.sort(key=lambda c: c.get("released_at", ""))

    mais_antiga = cartas_filtradas[0]
    mais_recente = cartas_filtradas[-1]

    def salvar_imagem(carta, descricao):
        try:
            imagem_url = carta['image_uris']['png']
        except KeyError:
            print(f"Imagem não encontrada para {descricao} da carta {nome_carta}.")
            return

        imagem_resposta = requests.get(imagem_url)
        if imagem_resposta.status_code == 200:
            nome_arquivo = os.path.join(pasta, f"{nome_carta.replace(' ', '_')}_{descricao}.png")
            with open(nome_arquivo, 'wb') as arquivo:
                arquivo.write(imagem_resposta.content)
            print(f"Imagem salva como {nome_arquivo}")
        else:
            print(f"Erro ao baixar a imagem para {descricao} da carta {nome_carta}.")

    salvar_imagem(mais_antiga, "mais_antiga")
    salvar_imagem(mais_recente, "mais_recente")


def processar_lista_cartas(arquivo_txt):
    pasta = criar_pasta()
    with open(arquivo_txt, "r", encoding="utf-8") as file:
        for linha in file:
            partes = linha.strip().split(" ", 1)
            if len(partes) == 2:
                _, nome_carta = partes
                baixar_imagem_carta(nome_carta, pasta)


# Exemplo de uso
processar_lista_cartas("marwyn-20250329-160458.txt")
