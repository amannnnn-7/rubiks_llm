#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import random
import os
from cube import RubiksCube
from together import Together

os.environ['TOGETHER_API_KEY'] = '****'
api_key = os.environ.get("TOGETHER_API_KEY")
if not api_key:
    raise ValueError("API key not found. Please set the TOGETHER_API_KEY environment variable.")

client = Together(api_key=api_key)

def generate_llm_prompt(cube):
    prompt = """You are an expert at solving Rubik's Cubes. Your task is to solve a scrambled Rubik's Cube step by step. The cube configuration is represented as a 3D array (6 faces x 3 rows x 3 columns) where each entry is a color ('W' for White, 'G' for Green, 'R' for Red, 'B' for Blue, 'O' for Orange, 'Y' for Yellow).

The sides are ordered : Top, Front, Right, Back, Left, Bottom.

The present cube configuration is:
"""
    for i, side in enumerate(['Top', 'Front', 'Right', 'Back', 'Left', 'Bottom']):
        prompt += f"{side}:\n{cube.cube[i].tolist()}\n\n"

    prompt += """The move notations are as follows:
- A single letter (F - Front, B - Back, R - Right, L - Left, U - Up / Top Face, D - Down / Bottom Face) refers to a clockwise 90-degree rotation of that face.
- A letter followed by an apostrophe (F', B', R', L', U', D') means a counterclockwise 90-degree rotation.
- A letter followed by '2' (F2, B2, R2, L2, U2, D2) means a 180-degree rotation.

Your objective is to solve this cube. For each move:
1. Provide a single move notation (e.g., "F", "R'", "U2").
2. State whether this move results in a solved cube: either "SOLVED" or "UNSOLVED".

Example of your response :
F'
UNSOLVED

Follow this response format.
Give your next move:
"""
    return prompt

def get_llm_move(cube):
    prompt = generate_llm_prompt(cube)
    
    messages = [
        {"role": "user", "content": prompt}
    ]
    
    response = client.chat.completions.create(
        model="meta-llama/Llama-3-70b-chat-hf",
        messages=messages,
        temperature=0.2
    )
    
    response_content = response.choices[0].message.content
    print("LLM output:", response_content)
    
    lines = response_content.strip().split('\n')
    move = lines[0].strip()
    status = lines[1].strip() if len(lines) > 1 else "UNSOLVED"
    
    return move, status

cube = RubiksCube()
scramble_moves = cube.scramble(100)
print("Cube scrambled with 100 random moves.")
cube.display()

move_count = 0
while True:
    move, status = get_llm_move(cube)
    print("\nMove Number : ", move_count)
    print(f"\nLLM move: {move}")
    print(f"\nLLM status: {status}")
    
    if move in cube.moves:
        cube.moves[move]()
        move_count += 1
    else:
        print(f"Invalid move: {move}")
        continue

    if status == "SOLVED":
        break

    if move_count >= 300:  
        print("Maximum moves reached. Stopping.")
        break
    
if cube.is_solved():
    print(f"Cube solved in {move_count} moves!")
else:
    print("LLM incorrectly claimed the cube was solved or the move limit was reached. The cube is still unsolved.")

print("\nFinal cube configuration:")
cube.display()
