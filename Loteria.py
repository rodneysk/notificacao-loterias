import requests
from locale import setlocale, LC_ALL

# Define a localidade para usar o formato de moeda brasileiro
setlocale(LC_ALL, 'pt_BR.UTF-8')

# Token do seu bot (obtido do BotFather)
TOKEN = '7896864022:AAFGP_lufIKlGw7t-raj866FuKCAzUWGwSM'

# Chat ID (obtido após enviar a mensagem ao bot)
CHAT_ID = '1018589617'  # Substitua com o Chat ID correto

# Função para enviar a mensagem no Telegram
def enviar_mensagem(mensagem):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID,
        'text': mensagem
    }
    response = requests.post(url, data=payload)
    
    if response.status_code == 200:
        print("Mensagem enviada com sucesso!")
    else:
        print(f"Erro ao enviar a mensagem: {response.status_code}")

# Função para consultar as loterias e enviar notificação se acumularem
def consultar_loterias():
    loterias_urls = [
        'https://loteriascaixa-api.herokuapp.com/api/megasena/latest',
        'https://loteriascaixa-api.herokuapp.com/api/lotofacil/latest',
        'https://loteriascaixa-api.herokuapp.com/api/quina/latest',
        'https://loteriascaixa-api.herokuapp.com/api/lotomania/latest',
        'https://loteriascaixa-api.herokuapp.com/api/duplasena/latest',
        'https://loteriascaixa-api.herokuapp.com/api/diadesorte/latest',
        'https://loteriascaixa-api.herokuapp.com/api/supersete/latest'
    ]

    for url in loterias_urls:
        resposta = requests.get(url)
        dados = resposta.json()

        # Coleta dos dados principais
        loteria = dados.get('nome', 'N/A')
        concurso = dados.get('numero', 'N/A')
        data = dados.get('data', 'N/A')
        acumulou = dados.get('acumulou', False)
        valor_acumulado = dados.get('valorEstimadoProximoConcurso', 0.0)
        data_proximo_sorteio = dados.get('dataProximoConcurso', 'N/A')

        # Corrige o valor acumulado para o formato brasileiro
        valor_acumulado_formatado = f"R$ {valor_acumulado:,.2f}".replace(",", "#").replace(".", ",").replace("#", ".")

        # Se acumulou, enviar mensagem
        if acumulou:
            mensagem = f"⚠️ O concurso da {loteria} acumulou!\n" \
                       f"🔢 Número do Concurso: {concurso}\n" \
                       f"🗓️ Data do Sorteio: {data}\n" \
                       f"🗓️ Data do Próximo Sorteio: {data_proximo_sorteio}\n" \
                       f"💵 Valor Acumulado: {valor_acumulado_formatado}"
            enviar_mensagem(mensagem)
        else:
            print(f"O concurso da {loteria} não acumulou.")

# Chama a função para consultar as loterias
consultar_loterias()
