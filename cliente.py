from jsonrpclib import Server
import string

try:
    server = Server('http://localhost:8080')
except Exception as e:
    print(f"Error connecting to the server: {e}")
    exit()

print("🎮 Welcome to the Quiz Game!")

jogador_id = int(input("Enter your player ID: "))

# while True:
#     dificuldade = input("Choose difficulty (easy, medium, hard): ").lower()
#     if dificuldade in ["easy", "medium", "hard"]:
#         break
#     else:
#         print("Invalid difficulty.")

perguntas = server.obter_perguntas(jogador_id)

pontos = 0

for i, pergunta in enumerate(perguntas, 1):
    print(f"\nQuestion {i}: {pergunta['pergunta']}")
    letras = string.ascii_lowercase[:len(pergunta['alternativas'])]
    mapa = dict(zip(letras, pergunta['alternativas']))
    
    for letra, opcao in mapa.items():
        print(f"{letra}) {opcao}")

    while True:
        resposta_usuario = input("Choose your answer: ").lower()
        if resposta_usuario in mapa:
            break
        print("Invalid option.")

    correta = server.verificar_resposta(jogador_id, pergunta['pergunta'], mapa[resposta_usuario])

    if correta:
        pontos += 1
        print("✅ Correct!")
    else:
        print(f"❌ Wrong! The correct answer was {pergunta['correta']}.")

print(f"\n🎯 Final score: {pontos} out of {len(perguntas)}")
