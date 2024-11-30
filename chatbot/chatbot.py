from flask import Flask, request, render_template

app = Flask(__name__)

# Rule-based response function
def chatbot_response(user_input):
    user_input = user_input.lower()

    responses = {
        "hello": "Hi there! How can I help you today?",
        "hi": "Hello! How can I assist you?",
        "how are you": "I'm just a bot, but I'm doing great! How can I assist you?",
        "bye": "Goodbye! Have a great day!",
        "thanks": "You're welcome! Let me know if you need anything else.",
        "what is your name": "I am a simple chatbot. What can I do for you today?",
        "help": "Sure! I can help you with basic queries. Just ask me anything.",
    }

    for key in responses.keys():
        if key in user_input:
            return responses[key]

    return "I'm sorry, I didn't understand that. Can you please rephrase?"


# Define a route for the chatbot interface
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_input = request.form["user_input"]
        response = chatbot_response(user_input)
        return render_template("index.html", user_input=user_input, response=response)
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
