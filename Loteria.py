import requests

TOKEN = '7896864022:AAFGP_lufIKlGw7t-raj866FuKCAzUWGwSM'
CHAT_ID = '1018589617'

def enviar_mensagem(mensagem):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {'chat_id': CHAT_ID, 'text': mensagem, 'parse_mode': 'HTML'}
    response = requests.post(url, data=payload)

    if response.status_code == 200:
        print("Mensagem enviada com sucesso!")
    else:
        print(f"Erro ao enviar a mensagem: {response.status_code}")

# Enviar notificações manualmente
mensagem_8h = "🕗 Boa manhã! Hora de conferir as loterias acumuladas!"
mensagem_15h = "📌 Não se esqueça de fazer os jogos acumulados para o(s) sorteio(s) de hoje!"
mensagem_18h45 = "❗ATENÇÃO ❗\nFaltam 15 minutos para o encerramento dos jogos!"

# Enviar as mensagens para testar
enviar_mensagem(mensagem_8h)
enviar_mensagem(mensagem_15h)
enviar_mensagem(mensagem_18h45)
