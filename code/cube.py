#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import numpy as np

class RubiksCube:
    def __init__(self):
        # Initialize a solved cube
        self.cube = np.array([
            [['W']*3 for _ in range(3)],  # Top (White)
            [['G']*3 for _ in range(3)],  # Front (Green)
            [['R']*3 for _ in range(3)],  # Right (Red)
            [['B']*3 for _ in range(3)],  # Back (Blue)
            [['O']*3 for _ in range(3)],  # Left (Orange)
            [['Y']*3 for _ in range(3)]   # Bottom (Yellow)
        ])
        self.moves = {
            'F': self.F, 'F\'': self.F_prime, 'F2': self.F2,
            'B': self.B, 'B\'': self.B_prime, 'B2': self.B2,
            'R': self.R, 'R\'': self.R_prime, 'R2': self.R2,
            'L': self.L, 'L\'': self.L_prime, 'L2': self.L2,
            'U': self.U, 'U\'': self.U_prime, 'U2': self.U2,
            'D': self.D, 'D\'': self.D_prime, 'D2': self.D2
        }

    def set_state(self, state):
        self.cube = np.array(state)

    def get_state(self):
        return self.cube

    def display(self):
        sides = ['Top', 'Front', 'Right', 'Back', 'Left', 'Bottom']
        for i, side in enumerate(sides):
            print(f"{side}:")
            print(self.cube[i])
            print()

    def rotate_face(self, face):
        self.cube[face] = np.rot90(self.cube[face], k=-1)

    def F(self):
        self.rotate_face(1)
        top, right, bottom, left = self.cube[0], self.cube[2], self.cube[5], self.cube[4]
        # Store the original values in temporary variables
        temp_top = np.copy(top[2])
        temp_right = np.copy(right[:, 0])
        temp_bottom = np.copy(bottom[0])
        temp_left = np.copy(left[:, 2])
        
        # Assign new values
        top[2] = temp_left[::-1]
        right[:, 0] = temp_top
        bottom[0] = temp_right[::-1]
        left[:, 2] = temp_bottom[::-1]
        
    def B(self):
        self.rotate_face(3)
        top, left, bottom, right = self.cube[0], self.cube[4], self.cube[5], self.cube[2]
        
        temp_top = np.copy(top[0])
        temp_left = np.copy(left[:, 0])
        temp_bottom = np.copy(bottom[2])
        temp_right = np.copy(right[:, 2])
        
        top[0] = temp_right[::-1]
        left[:, 0] = temp_top
        bottom[2] = temp_left[::-1]
        right[:, 2] = temp_bottom

    def R(self):
        self.rotate_face(2)
        top, front, bottom, back = self.cube[0], self.cube[1], self.cube[5], self.cube[3]
        
        temp_top = np.copy(top[:, 2])
        temp_front = np.copy(front[:, 2])
        temp_bottom = np.copy(bottom[:, 2])
        temp_back = np.copy(back[:, 0])
        
        top[:, 2] = temp_front
        front[:, 2] = temp_bottom
        bottom[:, 2] = temp_back[::-1]
        back[:, 0] = temp_top[::-1]

    def L(self):
        self.rotate_face(4)
        top, front, bottom, back = self.cube[0], self.cube[1], self.cube[5], self.cube[3]
        
        temp_top = np.copy(top[:, 0])
        temp_front = np.copy(front[:, 0])
        temp_bottom = np.copy(bottom[:, 0])
        temp_back = np.copy(back[:, 2])
        
        top[:, 0] = temp_back[::-1]
        front[:, 0] = temp_top
        bottom[:, 0] = temp_front
        back[:, 2] = temp_bottom[::-1]

    def U(self):
        self.rotate_face(0)
        front, right, back, left = self.cube[1], self.cube[2], self.cube[3], self.cube[4]
        
        temp_front = np.copy(front[0])
        temp_right = np.copy(right[0])
        temp_back = np.copy(back[0])
        temp_left = np.copy(left[0])
        
        front[0] = temp_right
        right[0] = temp_back
        back[0] = temp_left
        left[0] = temp_front

    def D(self):
        self.rotate_face(5)
        front, right, back, left = self.cube[1], self.cube[2], self.cube[3], self.cube[4]
        
        temp_front = np.copy(front[2])
        temp_right = np.copy(right[2])
        temp_back = np.copy(back[2])
        temp_left = np.copy(left[2])
        
        front[2] = temp_left
        right[2] = temp_front
        back[2] = temp_right
        left[2] = temp_back

    def F_prime(self):
        for _ in range(3): self.F()

    def F2(self):
        for _ in range(2): self.F()

    def B_prime(self):
        for _ in range(3): self.B()

    def B2(self):
        for _ in range(2): self.B()

    def R_prime(self):
        for _ in range(3): self.R()

    def R2(self):
        for _ in range(2): self.R()

    def L_prime(self):
        for _ in range(3): self.L()

    def L2(self):
        for _ in range(2): self.L()

    def U_prime(self):
        for _ in range(3): self.U()

    def U2(self):
        for _ in range(2): self.U()

    def D_prime(self):
        for _ in range(3): self.D()

    def D2(self):
        for _ in range(2): self.D()
        
    def scramble(self, n):
        moves = []
        for _ in range(n):
            move = random.choice(list(self.moves.keys()))
            self.moves[move]()
            moves.append(move)
        return moves
    
    def apply_moves(self, move_string):
        moves = move_string.split()
        for move in moves:
            if move in self.moves:
                self.moves[move]()
            else:
                print(f"Invalid move: {move}")
