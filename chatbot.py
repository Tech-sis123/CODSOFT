import re
import random

responses = {
    "greeting": ["Hello!", "Hi there!", "Hey! How can I assist you?"],
    "how_are_you": ["I'm doing great! Thanks for asking.", "I'm just a chatbot, but I'm good!"],
    "name": ["I'm a simple chatbot!", "You can call me ChatBuddy."],
    "bye": ["Goodbye! Have a great day!", "See you later!", "Bye! Take care!"],
    "default": ["I'm not sure I understand.", "Can you rephrase that?", "Hmm, I don't know how to respond to that."]
}

def get_response(user_input):
    user_input = user_input.lower().strip()  

    
    if any(word in user_input for word in ["hello", "hi", "hey"]):
        return random.choice(responses["greeting"])
    elif "how are you" in user_input:
        return random.choice(responses["how_are_you"])
    elif "your name" in user_input:
        return random.choice(responses["name"])
    elif any(word in user_input for word in ["bye", "goodbye", "exit"]):
        return random.choice(responses["bye"])
    
    elif re.search(r"(what|how) (is|are) (your|the) .*", user_input):
        return "That's an interesting question! Can you be more specific?"
    elif re.search(r"(weather|temperature)", user_input):
        return "I can't check the weather yet, but you can try a weather app!"

    return random.choice(responses["default"])

def chat():
    print(" ChatBot: Hello! Type 'exit' to stop chatting.")

    while True:
        user_input = input("You: ")

        if user_input.lower() in ["exit", "bye"]:
            print(" ChatBot:", random.choice(responses["bye"]))
            break
        
        response = get_response(user_input)
        print(" ChatBot:", response)


if __name__ == "__main__":
    chat()