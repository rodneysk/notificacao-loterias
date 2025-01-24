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
        'text': mensagem,
        'parse_mode': 'HTML'  # Aqui você define o uso de Markdown
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
        try:
            resposta = requests.get(url)
            dados = resposta.json()

            # Coleta dos dados principais, com verificação para garantir que não venha N/A
            loteria = dados.get('loteria', 'Desconhecida')
            concurso = dados.get('concurso', 'Desconhecido')
            data = dados.get('data', 'Desconhecida')
            acumulou = dados.get('acumulou', False)
            valor_acumulado = dados.get('valorAcumuladoProximoConcurso', 0.0)
            data_proximo_sorteio = dados.get('dataProximoConcurso', 'Desconhecida')
            proximo_concurso = dados.get('proximoConcurso', 'Desconhecido')
            valor_estimado_proximo_concurso = dados.get('valorEstimadoProximoConcurso', 0.0)

            # Corrige o valor acumulado para o formato brasileiro
            if isinstance(valor_estimado_proximo_concurso, (float, int)):  # Garantir que é numérico
                valor_estimado_formatado = f"R$ {valor_estimado_proximo_concurso:,.2f}".replace(",", "#").replace(".", ",").replace("#", ".")
            else:
                valor_estimado_formatado = "Valor inválido"

            # Exibe os valores para debug (opcional)
            print(f"Concurso: {concurso}, Loteria: {loteria}, Valor Estimado Próximo Concurso: {valor_estimado_formatado}")

            # Se acumulou, enviar mensagem
            if acumulou:
                mensagem = f"💰 <b>O concurso {loteria} acumulou!</b>\n\n" \
                            f"💵 <b>Valor do Próximo Concurso:</b> {valor_estimado_formatado}\n" \
                            f"🔢 <b>Número do Próximo Concurso:</b> {proximo_concurso}\n" \
                            f"🗓️ <b>Data do Sorteio:</b> {data_proximo_sorteio}\n"
                enviar_mensagem(mensagem)
            else:
                print(f"O concurso da {loteria} não acumulou.")
        except Exception as e:
            print(f"Erro ao processar dados da URL {url}: {e}")

# Enviar a mensagem de "Bom dia" primeiro (às 8h)
mensagem_bom_dia = "📅 Bom dia! Não se esqueça de verificar os jogos acumulados para o sorteio de hoje!"
enviar_mensagem(mensagem_bom_dia)

# Enviar mensagem de jogos acumulados (às 8h, após "Bom dia")
consultar_loterias()

# Mensagem das 15h
mensagem_15h = "📌 Não se esqueça de fazer os jogos acumulados para o(s) sorteio(s) de hoje!"
enviar_mensagem(mensagem_15h)

# Mensagem das 18h45
mensagem_18h45 = "❗<b>ATENÇÃO</b> ❗\nFaltam 15 minutos para o encerramento dos jogos!"
enviar_mensagem(mensagem_18h45)
