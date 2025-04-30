import requests
import json
import html
import string

print("Welcome to the Quiz Game!")

while True:
    dificuldade = input("You can choose the difficulty level: easy, medium, or hard.\n").lower()
    if dificuldade in ["easy", "medium", "hard"]:
        break
    else:
        print("Invalid difficulty level. Please choose easy, medium, or hard.")

url = f"https://opentdb.com/api.php?amount=10&category=15&difficulty={dificuldade}&type=multiple"

response = requests.get(url)
data = response.json()
pontos = 0

for i, question in enumerate(data['results'], start=1):
    pergunta = html.unescape(question['question'])  
    print(f"\nQuestion {i}: {pergunta}")
    opcoes = [html.unescape(opt) for opt in question['incorrect_answers'] + [question['correct_answer']]]
    opcoes = sorted(opcoes) 
    letras = string.ascii_lowercase[:len(opcoes)]  # Gerar letras (a, b, c, ...)
    mapa_opcoes = dict(zip(letras, opcoes))  # Mapear letras para opções
    
    # Exibir as opções com letras
    for letra, opcao in mapa_opcoes.items():
        print(f"{letra}) {opcao}")
    
    while True:
        resposta = input("\nChoose your answer: ").lower() 
        
        if resposta == "":
            print("You didn't answer the question. Please choose an option.")
        elif resposta == "exit":
            print("Exiting the game. Goodbye!")
            exit()
        elif resposta in mapa_opcoes:
            
            if mapa_opcoes[resposta] == html.unescape(question['correct_answer']):
                pontos += 1
                print(f"\n✅ Correct! Your new score is: {pontos}")
            else:
                print(f"\n❌ Wrong! The correct answer is: {html.unescape(question['correct_answer'])}")
            break 
        else:
            print("\nInvalid option. Please choose a valid letter.\n")

print(f"\nYour final score is: {pontos} out of {len(data['results'])}")