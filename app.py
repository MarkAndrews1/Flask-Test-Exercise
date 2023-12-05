from flask import Flask, request, render_template, session, jsonify
from boggle import Boggle

boggle_game = Boggle()

app = Flask(__name__)
app.config["SECRET_KEY"] = "Secret-key"

@app.route("/")
def home_page():
    board = boggle_game.make_board()
    session['board'] = board
    highscore = session.get("highscore", 0)
    numplays = session.get('numplays', 0)
    return render_template('game.html', board = board, highscore = highscore, numplays = numplays)

@app.route("/word-check")
def check_word():
    word = request.args['word']
    board = session['board']
    res = boggle_game.check_valid_word(board, word)
    return jsonify({'result': res})

@app.route("/get-score", methods=['post'])
def get_score():
    score = request.json["score"]
    highscore = session.get("highscore", 0)
    numplays = session.get("numplays", 0)
    session["highscore"] = max(score, highscore)
    session["numplays"] = numplays + 1
    return jsonify(brokenRec = score > highscore)
