from copy import deepcopy as copy
from board import *
import pathos.pools as p
from time import time


class Kiasa:
	def __init__(self, depth=4, offset=2):
		self.chess = Board()
		self.min_depth = depth
		self.max_depth = depth + offset
		self.count = 0


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
		self.count = 0
		if self.chess.turn():
			value = float('-inf')
			for move in moves:
				self.count += 1
				alphabeta_result = self.alphabeta(copy(self.chess), move, 1, alpha, beta)
				if value <= alphabeta_result:
					value = alphabeta_result
					result = move
				alpha = max(value, alpha)
				if alpha >= beta:
					break
		else:
			value = float('inf')
			for move in moves:
				self.count += 1
				alphabeta_result = self.alphabeta(copy(self.chess), move, 1, alpha, beta)
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
T/N:  {timer/self.count*1e3} ms""")
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
				self.count += 1
				value = max(value, self.alphabeta(copy(chess), move, depth+1, alpha, beta))
				alpha = max(value, alpha)
				if alpha >= beta:
					break
			return value
		else:
			value = float('inf')
			for move in moves:
				self.count += 1
				value = min(value, self.alphabeta(copy(chess), move, depth+1, alpha, beta))
				beta = min(value, beta)
				if alpha >= beta:
					break
			return value


class Kiasa:
	def __init__(self, depth=4, offset=2):
		self.chess = board()
		self.min_depth = depth
		self.max_depth = depth + offset
		self.count = 0


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
T/N:  {timer/self.count*1e3} ms""")
		self.chess(result)
		return result, value


	def alphabeta(self, chess, urgent, depth=0, alpha=float('-inf'), beta=float('inf')):
		if chess.board.is_repetition(2):
			return 0

		if (depth >= self.min_depth and not urgent) or depth >= self.max_depth:
			return chess.util
			if chess.turn():
				return max((copy(chess)(move).util for move in chess.legal_moves()))
			else:
				return min((copy(chess)(move).util for move in chess.legal_moves()))
		if (depth - 1 >= self.min_depth  and not urgent) or depth - 1 >= self.max_depth:
			boards = ((copy(chess)(move), chess.is_capture(move) or chess.board.is_check()) for move in chess.legal_moves())
		else:
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

