import pathos.pools as p
import chess.polyglot as opening
from random import shuffle
from copy import deepcopy as copy
from board import *
from time import time, sleep
from math import exp


class Kiasa:
	def __init__(self, opening_book=True, variation=True, depth=3, offset=3):
		self.chess = Board()
		self.opening_book = opening_book
		self.variation = variation
		self.min_depth = depth
		self.max_depth = depth + offset
		self.count = 0


	def __call__(self):
		with opening.open_reader("data/performance.bin") as book:
			moves = [entry.move for entry in book.find_all(self.chess.board)]
			if moves and self.opening_book:
				if self.variation:
					shuffle(moves)
				phi = lambda x: 1/(1+exp(-x))-0.5
				move = moves[0]
				self.chess(move)
				sleep(1)
				print(f"""
OPENING MODE
MOVE: {move}
""")
				return move, phi(self.chess.util)
		t = time()
		moves = self.chess.legal_moves()
		if len(list(moves)) == 1:
			move = list(moves)[0]
			self.chess(move)
			return move, self.chess.utility()

		alpha=float('-inf')
		beta=float('inf')
		result = None
		boards = sorted(((copy(self.chess)(move), False, move) for move in moves), key=lambda x: x[0].util, reverse=self.chess.turn())
		self.count = 0
		if self.chess.turn():
			value = float('-inf')
			for board, urgent, move in boards:
				self.count += 1
				alphabeta_result = self.alphabeta(board, urgent, 1, alpha, beta)
				if value <= alphabeta_result:
					value = alphabeta_result
					result = move
				alpha = max(value, alpha)
				if alpha >= beta:
					break
		else:
			value = float('inf')
			for board, urgent, move in boards:
				self.count += 1
				alphabeta_result = self.alphabeta(board, urgent, 1, alpha, beta)
				if value >= alphabeta_result:
					value = alphabeta_result
					result = move
				beta = min(value, beta)
				if alpha >= beta:
					break
		if result is None:
			move = 'RESIGN'
		else:
			move = result.uci().upper()
		timer = round(time()-t, 1)
		print(f"""
MOVE: {move}
UTIL: {round(value, 3)}
TIME: {timer} s
NODE: {self.count}
ONCE: {round(timer/self.count*1e3, 3)} ms""")
		self.chess(result)
		return result, value


	def alphabeta(self, chess, urgent, depth=0, alpha=float('-inf'), beta=float('inf')):
		if chess.board.is_repetition(2):
			return 0
		if chess.board.is_game_over():
			return chess.util

		if (depth >= self.min_depth and not urgent) or depth >= self.max_depth:
			return chess.util
		boards = sorted(((copy(chess)(move), chess.is_capture(move) or chess.board.is_check()) for move in chess.legal_moves()), key=lambda x: x[0].util, reverse=chess.turn())
		if chess.turn():
			value = float('-inf')
			for board, urgent in boards:
				self.count += 1
				value = max(value, self.alphabeta(board, urgent, depth+1, alpha, beta))
				alpha = max(value, alpha)
				if alpha >= beta:
					break
			return value
		else:
			value = float('inf')
			for board, urgent in boards:
				self.count += 1
				value = min(value, self.alphabeta(board, urgent, depth+1, alpha, beta))
				beta = min(value, beta)
				if alpha >= beta:
					break
			return value
