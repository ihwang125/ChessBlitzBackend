import pyrebase
from pyrebase.pyrebase import Database, Auth
import random
from typing import Dict, Any, Tuple, List
import re
import chess
from flask import jsonify

def fetch_puzzle(db: Database, puzzle_id: str) -> Dict[str, Any]:
    """Fetches puzzle id from Firebase Database with specified puzzle_id"""
    return db.child("puzzles").child(puzzle_id).get().val()

def fetch_random_puzzle(db: Database) -> Dict[str, Any]:
    """Fetches a random puzzle from Firebase Database"""
    puzzle_ids = fetch_puzzle_ids(db)
    random_puzzle_id = random.choice(puzzle_ids)

    result = fetch_puzzle(db, random_puzzle_id)
    result['ID'] = random_puzzle_id
    return result

def fetch_puzzle_ids(db: Database) -> List[str]:
    return list(db.child("puzzles").shallow().get().val())

def validate_puzzle_id(db: Database, puzzle_id: str) -> Tuple[bool, str]:
    """Validates if the input arguments from the frontend are valid parameters for a puzzle in the database"""
    assert type(db) == Database

    if type(puzzle_id) != str:
        return False, "Puzzle ID must be of type string"
    if len(puzzle_id) != 5:
        return False, "Malformed Puzzle ID input"

    puzzle_ids = fetch_puzzle_ids(db)
    if puzzle_id not in puzzle_ids:
        return False, "Puzzle ID does not exist in the Database"

    return True, ""

def validate_puzzle_move(moves: List[str], move_number: int) -> Tuple[bool, str]:
    """Validates if the move_number is valid for the specified puzzle"""
    if type(move_number) != int:
        return False, "Invalid Move Number, not of type int"
    if move_number-1 < 0:
        return False, "Invalid Move Number, must be greater than or equal to 0"
    if move_number-1 >= len(moves):
        return False, "Invalid Move Number, must be less than length of puzzle"
    return True, ""

def validate_puzzle(puzzle: Dict[str, Any]) -> bool:
    """Validates if a puzzle is a valid puzzle"""
    if puzzle is None:
        return False
    return True

def validate_email(email: str) -> Tuple[bool, str]:
    """Validates if the email is in the correct format"""
    if type(email) != str:
        return False, "Email must be of type string"
    if len(email) < 5 or "@" not in email:
        return False, "Malformed Email input"
    return True, ""

def validate_password(password: str) -> Tuple[bool, str]:
    """Validates if the password is in the correct format"""
    if type(password) != str:
        return False, "Password must be of type string"
    if len(password) < 6:
        return False, "Password must be at least 6 characters long"
    if not re.search(r"\d+", password):
        return False, "Password must contain at least one digit"
    return True, ""

# Sign in function
def sign_in(auth: Auth, email: str, password: str) -> Tuple[Dict[str, Any], str]:
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        message = f"Signed in successfully: {user}"
        return user, message
    except Exception as e:
        message = f"Error: {e}"
        return None, message
    
# Sign-up function
def sign_up(auth: Auth, email: str, password: str) -> Tuple[Dict[str, Any], str]:
    try:
        user = auth.create_user_with_email_and_password(email, password)
        message = f"User created successfully: {user}"
        return user, message
    except Exception as e:
        message = f"Error: {e}"
        return None, message
    
def sign_up_page(db: Database, userid: str, name: str, username: str, country: str) -> Tuple[Dict[str, Any], int]:
    try:
        user_data = {
            "name": name,
            "username": username,
            "country": country,
            "friends": []
        }
        db.child("users").child(userid).set(user_data)

        user_record = db.child("users").child(username).get().val()
        if user_record:
            message = f"User created successfully: {username}"
            return jsonify({"message": message, "user": user_record}), 201
        else:
            return jsonify({"message": "User creation failed"}), 400
    except Exception as e:
        return jsonify({"error": f"Error signing up: {e}"}), 500

def get_fen(fen: str, moves: list, move: int) -> str:
   """
   Returns the fen after move number of specified moves from the moves list applied to the original fen

   Parameters:
   - fen (str): current fen
   - moves (list): a list of moves to apply to the fen
   - move (int): the number of moves into the puzzle

   Returns:
       str: the fen after the moves have been applied
   """
   temp_fen = fen
   for i in range(0, move):
       current_move = moves[i]
       temp_fen = update_fen(temp_fen, current_move)
   return temp_fen


def update_fen(fen: str, move: str) -> str:
   """
   Update a FEN string with a given move in UCI format.


   Parameters:
   - fen (str): The FEN string of the current board position.
   - move (str): The move in UCI format (e.g., "e2e4", "e7e8q").


   Returns:
   - str: The updated FEN string after the move.
   """
   board = chess.Board(fen)
   uci_move = chess.Move.from_uci(move)


   #if uci_move not in board.legal_moves:
   #    raise ValueError(f"Illegal move: {move}")


   board.push(uci_move)
   return board.fen()

def get_current_player(fen: str) -> str:
    """ 
    Gets the current player of a game defined by an input fen string

    Parameters:
    - fen (str): current fen

    Returns:
    - str: The current player
    """
    board = chess.Board(fen)

    return "white" if board.turn else "black"
