from flask import Flask, request, jsonify
from flask_cors import CORS  # To handle cross-origin requests
import requests
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

# Stockfish API endpoint
# STOCKFISH_API_URL = "https://stockfish.online/api/s/v2.php"

@app.route("/puzzles/random/", methods=["GET"])
def get_random_puzzle() -> Tuple[Dict[str, Any], int]:
    """Returns random puzzle from Firebase realtime database of puzzles"""
    return jsonify({"error": "Function Development In Progress"}), 500

@app.route("/puzzles/{puzzle_id}/best-moves/{move_number}", methods=["GET"])
def get_best_move(puzzle_id: int, move_number: int) -> Tuple[Dict[str, Any], int]:
    """Gets best move based on the puzzle_id and current move_number"""
    # fen = "" # Depends on how we store puzzle_id in Firebase DB

    return jsonify({"error": "Function Development In Progress"}), 500
    """
    if not fen:
        return jsonify({"error": "FEN notation missing"}), 400

    # Call Stockfish API with GET request
    params = {"fen": fen, "depth": 15}  # Default depth 15
    response = requests.get(STOCKFISH_API_URL, params=params)

    if response.status_code == 200:
        stockfish_data = response.json()
        if stockfish_data.get("success"):
            best_move_raw = stockfish_data.get("bestmove", "Unknown")
            best_move = best_move_raw.split()[1] if len(best_move_raw.split()) > 1 else "Unknown"
            eval_score = stockfish_data.get("evaluation", "N/A")
            return jsonify({
                "best_move": best_move,
                "evaluation": eval_score
            })
        else:
            return jsonify({"error": stockfish_data.get("data", "Unknown error")}), 400
    else:
        return jsonify({"error": "Stockfish API request failed."}), 500
    """

@app.route("/puzzles/{puzzle_id}/hints/{move_number}", methods=["GET"])
def gethint(puzzle_id: int, move_number: int, modelversion: str = "gpt-4-turbo") -> Tuple[Dict[str, Any], int]:
    """Send the puzzle_id and move_number to OpenAI for explanation."""
    return jsonify({"error": "Function Development In Progress"}), 500
    """
    try:
        fen = puzzle_id # str. Need to change this to get the fen from the puzzle_id <- depends on how we store puzzle_id
        player = move_number # str. Need to figure this out based on the puzzle and the move_number
        best_move = "d4" # str. Need to figure this out based on the puzzle and move_number
        response = openaiclient.responses.create(
            model=modelversion,
            instructions="You are a chess tutor, and you know how to play chess. You are tutoring a student, and you don't want to provide the best move explicitly, but guide the student towards their own discovery of the move.",
            input=f"In the position: {fen} ; the move is for {player}, and the best move is: {best_move}. Please provide a hint to the student that is not obvious and is not too informative or easy, but reasonable enough."
        )
        return response.output_text if response else "No explanation available."
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return "Error fetching explanation."
    """

if __name__ == "__main__":
    app.run(debug=True)
