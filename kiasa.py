from copy import deepcopy as copy
from board import Board
import pathos.pools as p
from time import time


class Kiasa:
	def __init__(self, depth=3, offset=3):
		self.chess = Board()
		self.min_depth = depth
		self.max_depth = depth + offset


	def __call__(self):
		t = time()
		moves = self.chess.legal_moves()
		if len(list(moves)) == 1:
			move = list(moves)[0]
			self.chess(move)
			return move, self.chess.utility()

		alpha=float('-inf')
		beta=float('inf')
		result = None
		if self.chess.turn():
			value = float('-inf')
			for move in moves:
				alphabeta_result = self.alphabeta(copy(self.chess), move, 1)
				if value <= alphabeta_result:
					value = alphabeta_result
					result = move
				alpha = max(value, alpha)
				if alpha >= beta:
					break
		else:
			value = float('inf')
			for move in moves:
				alphabeta_result = self.alphabeta(copy(self.chess), move, 1)
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
		print(f"""
MOVE: {move}
UTIL: {round(value, 3)}
TIME: {round(time()-t, 1)} sec""")
		self.chess(result)
		return result, value


	def alphabeta(self, chess, move, depth=0, alpha=float('-inf'), beta=float('inf')):
		urgent = chess.is_capture(move) or chess.board.is_check()
		chess(move)

		# REPETITION AVOIDANCE
		if chess.board.is_repetition(2):
			return 0

		if (depth >= self.min_depth and not urgent) or depth >= self.max_depth:
			return chess.utility()
		moves = chess.legal_moves()
		if chess.turn():
			value = float('-inf')
			for move in moves:
				value = max(value, self.alphabeta(copy(chess), move, depth+1, alpha, beta))
				alpha = max(value, alpha)
				if alpha >= beta:
					break
			return value
		else:
			value = float('inf')
			for move in moves:
				value = min(value, self.alphabeta(copy(chess), move, depth+1, alpha, beta))
				beta = min(value, beta)
				if alpha >= beta:
					break
			return value

