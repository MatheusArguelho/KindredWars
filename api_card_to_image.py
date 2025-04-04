import requests
import os


def criar_pasta(nome_carta):
    pasta_principal = nome_carta.replace(" ", "_")
    pasta_png = os.path.join(pasta_principal, "PNG")
    pasta_art_crop = os.path.join(pasta_principal, "Art_Crop")
    os.makedirs(pasta_png, exist_ok=True)
    os.makedirs(pasta_art_crop, exist_ok=True)
    return pasta_png, pasta_art_crop


def baixar_imagem(url, caminho):
    resposta = requests.get(url)
    if resposta.status_code == 200:
        with open(caminho, 'wb') as arquivo:
            arquivo.write(resposta.content)
        print(f"Imagem salva: {caminho}")
    else:
        print(f"Erro ao baixar imagem: {url}")


def baixar_todas_artes(nome_carta):
    url = f"https://api.scryfall.com/cards/search?q=%21%22{nome_carta.replace(' ', '%20')}%22+new%3Aart+is%3Abooster&unique=prints"
    resposta = requests.get(url)

    if resposta.status_code != 200:
        print(f"Erro ao buscar a carta {nome_carta}.")
        return

    dados = resposta.json()
    if "data" not in dados:
        print(f"Nenhuma arte encontrada para {nome_carta}.")
        return

    pasta_png, pasta_art_crop = criar_pasta(nome_carta)

    for carta in dados["data"]:
        if "image_uris" in carta:
            if "png" in carta["image_uris"]:
                caminho_png = os.path.join(pasta_png, f"{carta['id']}.png")
                baixar_imagem(carta["image_uris"]["png"], caminho_png)
            if "art_crop" in carta["image_uris"]:
                caminho_art_crop = os.path.join(pasta_art_crop, f"{carta['id']}.jpg")
                baixar_imagem(carta["image_uris"]["art_crop"], caminho_art_crop)


# Exemplo de uso
baixar_todas_artes("Angelic Page")
