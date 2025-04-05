import pyrebase
from pyrebase.pyrebase import Database
import random
from typing import Dict, Any, Tuple, List


def fetch_puzzle(db: Database, puzzle_id: str) -> Dict[str, Any]:
    """Fetches puzzle id from Firebase Database with specified puzzle_id"""
    return db.child("puzzles").child(puzzle_id).get().val()

def fetch_random_puzzle(db: Database) -> Dict[str, Any]:
    """Fetches a random puzzle from Firebase Database"""
    puzzle_ids = fetch_puzzle_ids(db)
    random_puzzle_id = random.choice(puzzle_ids)

    return fetch_puzzle(db, random_puzzle_id)

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

    return True

def validate_puzzle_move(moves: List[str], move_number: int) -> Tuple[bool, str]:
    """Validates if the move_number is valid for the specified puzzle"""
    assert type(moves) == List[str]

    if type(move_number) != int:
        return False, "Invalid Move Number, not of type int"
    if move_number-1 < 0:
        return False, "Invalid Move Number, must be greater than or equal to 0"
    if move_number-1 > len(moves):
        return False, "Invalid Move Number, must be less than length of puzzle"
    return True

def validate_puzzle(puzzle: Dict[str, Any]) -> bool:
    """Validates if a puzzle is a valid puzzle"""
    if puzzle is None:
        return False
    return True
