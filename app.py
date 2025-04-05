from flask import Flask, request, jsonify
from flask_cors import CORS  # To handle cross-origin requests
import requests
from functions import *
from typing import Dict, Any, Tuple
from openai import OpenAI
import os
import pyrebase

# Firebase Config Dev Only
config = {
  "apiKey": os.getenv("FIREBASE_API_KEY"),
  "authDomain": "chessblitz-21d26.firebaseapp.com",
  "databaseURL": "https://chessblitz-21d26-default-rtdb.firebaseio.com/",
  "storageBucket": "chessblitz-21d26.firebasestorage.app"
}

firebase = pyrebase.initialize_app(config)

db = firebase.database()

# OpenAI API Config
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openaiclient = OpenAI(
    api_key = OPENAI_API_KEY
)

# Flask Config
app = Flask(__name__)
CORS(app)  # Allow all domains for now (development only)

@app.route("/puzzles/random/", methods=["GET"])
def get_random_puzzle() -> Tuple[Dict[str, Any], int]:
    """Returns random puzzle from Firebase realtime database of puzzles"""
    try:
        puzzle = fetch_random_puzzle(db)
        if not validate_puzzle(puzzle):
            return jsonify(puzzle), 200
        return jsonify({"error": "Puzzle does not exist"}), 404
    except:
        return jsonify({"error": "Server function error"}), 500

@app.route("/puzzles/{puzzle_id}/best-moves/{move_number}", methods=["GET"])
def get_best_move(puzzle_id: int, move_number: int) -> Tuple[Dict[str, Any], int]:
    """Gets best move based on the puzzle_id and current move_number"""
    try:
        # User Input Error Handling
        condpuzzle, errpuzzle = validate_puzzle_id(puzzle_id)
        if not condpuzzle:
            return jsonify({"error": errpuzzle}), 400

        puzzle = fetch_puzzle(db, puzzle_id)
        moves = puzzle["Moves"].split(' ')

        cond, err = validate_puzzle_move(moves, move_number)
        if not cond:
            return jsonify({"error": err}), 400

        # Success
        return jsonify({"best_move": moves[move_number-1]}), 200
    except:
        return jsonify({"error": "Server function error"}), 500

@app.route("/puzzles/{puzzle_id}/hints/{move_number}", methods=["GET"])
def gethint(puzzle_id: int, move_number: int, modelversion: str = "gpt-4-turbo") -> Tuple[Dict[str, Any], int]:
    """Send the puzzle_id and move_number to OpenAI for explanation."""
    try:
        # User Input Error Handling
        condpuzzle, errpuzzle = validate_puzzle_id(puzzle_id)
        if not condpuzzle:
            return jsonify({"error": errpuzzle}), 400

        puzzle = fetch_puzzle(db, puzzle_id)
        moves = puzzle["Moves"].split(' ')

        cond, err = validate_puzzle_move(moves, move_number)
        if not cond:
            return jsonify({"error": err}), 400

        # OpenAI API Call Formation
        move = moves[move_number-1]
        fen = puzzle["FEN"]
        player = "unkown" # STILL IN DEVELOPMENT, NEED TO FIGURE OUT WAY TO IDENTIFY CURRENT PLAYER

        # OpenAI API Call
        response = openaiclient.responses.create(
            model=modelversion,
            instructions="You are a chess tutor, and you know how to play chess. You are tutoring a student, and you don't want to provide the best move explicitly, but guide the student towards their own discovery of the move.",
            input=f"In the position: {fen} ; the move is for {player}, and the best move is: {best_move}. Please provide a hint to the student that is not obvious and is not too informative or easy, but reasonable enough."
        )
        response = response.output_text if response else "No explanation available."

        return jsonify({"hint": response}), 200
    except:
        return jsonify({"error": "Error fetching explanation."}), 500

if __name__ == "__main__":
    app.run(debug=True)
