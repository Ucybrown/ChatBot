import json

from bs4 import BeautifulSoup
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer
from flask import Flask, render_template, request, jsonify
from requests import get

# instantiate the class Flask
app = Flask(__name__)

# instantiate the class ChatBot
bot = ChatBot(
    'FirstChatBot',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',  # default one
    database_uri='sqlite:///collHI.sqlite3',
    logic_adapters=[{
        #'chatterbot.logic.MathematicalEvaluation',
        #'chatterbot.logic.TimeLogicAdapter',
        #'chatterbot.logic.UnitConversion'
        'import_path': 'chatterbot.logic.BestMatch',
        'default_response': 'Oh je mi ne.'
    }],
    preprocessors=[
        'chatterbot.preprocessors.convert_to_ascii',
        'chatterbot.preprocessors.unescape_html',
        'chatterbot.preprocessors.clean_whitespace'
    ]
)


# creating a list of question and answer from the nfL6.json file
def create_list():
    train = []
    data = json.loads(open('nfL6.json', 'r').read())  # 87.362
    for k, row in enumerate(data):
        train.append(row['question'])
        train.append(row['answer'])

        if k == 10:
            break
    return train


trainer = ListTrainer(bot)
trainer.train(create_list())

# trainer = ListTrainer(bot)
# trainer.train([
#     "How are you?",
#     "I am happy today",
#     "That is good to hear",
#     "Thank you",
#     "You are welcome"
# ])
# trainer.train([
#     "Greetings!",
#     "Hello"
# ])

# corpus training
# trainer = ChatterBotCorpusTrainer(bot)
# trainer.train(
#     "chatterbot.corpus.english"
# )


@app.route("/")
def index():
    return render_template("chat.html")


@app.route("/ask", methods=['POST'])
def get_bot_response():
    message = str(request.form['msg'])
    print("Message ", message)
    #message = request.args.get('msg')
    bot_response = bot.get_response(message)
    if bot_response.confidence > 0.1:
        return jsonify({'status': 'OK', 'answer': str(bot_response)})
    else:
        try:
            url = "https://en.wikipedia.org/wiki/" + message
            page = get(url).text
            soup = BeautifulSoup(page, "html.parser")
            p = soup.find_all("p")
            return jsonify({'status': 'OK', 'answer': p[1].text})
        except IndexError as error:
            bot_response = "Sorry, I have no idea about your question."
            return jsonify({'status': 'OK', 'answer': str(bot_response)})




# while True:
#     try:
#         user_input = input("YOU: ")
#         bot_response = bot.get_response(user_input)
#         print("BOT: ", bot_response)
#
#     # press ctrl-c or ctrl-d on the keyboard to exit
#     except (KeyboardInterrupt, EOFError, SystemExit):
#         break


app.run(port=5001, debug=True)
