import requests
import os
from datetime import datetime

# Carregar variáveis de ambiente
TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def enviar_mensagem(mensagem):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {'chat_id': CHAT_ID, 'text': mensagem, 'parse_mode': 'HTML'}
    response = requests.post(url, data=payload)
    
    if response.status_code == 200:
        print("Mensagem enviada com sucesso!")
    else:
        print(f"Erro ao enviar a mensagem: {response.status_code}")

# Função para consultar as loterias e enviar mensagem às 8h
def notificar_8h():
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

# Função para enviar mensagem das 15h
def notificar_15h():
    mensagem_15h = "📌 Não se esqueça de fazer os jogos acumulados para o(s) sorteio(s) de hoje!"
    enviar_mensagem(mensagem_15h)

# Função para enviar mensagem das 18h45
def notificar_18h45():
    mensagem_18h45 = "❗ATENÇÃO ❗\nFaltam 15 minutos para o encerramento dos jogos!"
    enviar_mensagem(mensagem_18h45)

# Obter a hora atual
hora_atual = datetime.now().hour
minuto_atual = datetime.now().minute

# Enviar notificações com base no horário
if hora_atual == 8 and minuto_atual == 0:
    notificar_8h()
elif hora_atual == 15 and minuto_atual == 0:
    notificar_15h()
elif hora_atual == 18 and minuto_atual == 45:
    notificar_18h45()
else:
    print("Não é hora de enviar mensagens.")
