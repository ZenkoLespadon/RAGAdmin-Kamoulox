from transformers import AutoTokenizer, AutoModelForCausalLM, TextStreamer
import torch


def set_up_tokenizer(modelPath):
    # Charger le tokenizer et le modèle
    tokenizer = AutoTokenizer.from_pretrained(modelPath)
    model = AutoModelForCausalLM.from_pretrained(modelPath)
    # Si le modèle n'a pas de token de padding, utilisez le token EOS comme padding
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    # Déplacer le modèle sur le GPU si disponible
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)

    return tokenizer, model, device


def generate_text(user_message):
    global streamer
    # Définir les messages, incluant un system prompt en anglais
    messages = [
        {"role": "system",
         "content": "You're an intelligent assistant able to answer all questions concisely and accurately. You always answer in the language in which the question is asked. Don't give out unsolicited information, and always answer directly."},
        {"role": "user", "content": user_message},
    ]
    # Convertir la liste de messages en un format texte
    # Inclure le system prompt et l'utilisateur
    prompt = "".join([f"{message['role']}: {message['content']}\n" for message in messages])
    # Tokeniser le prompt
    question = tokenizer(prompt, return_tensors="pt", padding=True, truncation=True).to(device)
    # Configurer le streamer pour obtenir la sortie progressivement
    streamer = TextStreamer(tokenizer)
    # Générer le texte avec la méthode de streaming
    _ = model.generate(
        **question,
        streamer=streamer,
        pad_token_id=tokenizer.eos_token_id,
        max_length=2048,  # Vous pouvez ajuster cette limite selon vos besoins
        bos_token_id=None,
    )

    print_text_word_by_word()


def print_text_word_by_word():
    # Affichage du texte généré progressivement par le streamer
    for new_text in streamer:
        print(new_text, end="", flush=True)


if __name__ == "__main__":
    # Définir manuellement le nombre de threads pour PyTorch (Obligatoire sinon le LLM n'utilise pas toute la puissance du serveur)
    torch.set_num_threads(10)

    modelPath = "./Meta-Llama-3.1-8B-Instruct"

    tokenizer, model, device = set_up_tokenizer(modelPath)

    user_message = "Qu'est-ce que Python ?"

    generate_text(user_message)
