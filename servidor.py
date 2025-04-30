from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer
import requests
import html
import random

# Banco de perguntas para jogadores
perguntas_por_jogador = {}

def obter_perguntas(jogador_id):
    url = f"https://opentdb.com/api.php?amount=10&category=15&difficulty=medium&type=multiple"
    response = requests.get(url)
    data = response.json()
    
    perguntas = []
    for item in data['results']:
        pergunta = html.unescape(item['question'])
        alternativas = [html.unescape(opt) for opt in item['incorrect_answers']] + [html.unescape(item['correct_answer'])]
        random.shuffle(alternativas)
        perguntas.append({
            "pergunta": pergunta,
            "alternativas": alternativas,
            "correta": html.unescape(item['correct_answer'])
        })
    
    perguntas_por_jogador[jogador_id] = perguntas
    return perguntas

def verificar_resposta(jogador_id, pergunta_texto, resposta):
    perguntas = perguntas_por_jogador.get(jogador_id, [])
    for pergunta in perguntas:
        if pergunta["pergunta"] == pergunta_texto:
            correta = pergunta["correta"]
            return resposta == correta
    return False

server = SimpleJSONRPCServer(('localhost', 8080))
server.register_function(obter_perguntas, 'obter_perguntas')
server.register_function(verificar_resposta, 'verificar_resposta')
print("Servidor JSON-RPC rodando em localhost:8080...")
server.serve_forever()
