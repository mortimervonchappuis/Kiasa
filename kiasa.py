from copy import deepcopy as copy
from board import Board
import pathos.pools as p


class Kiasa:
	def __init__(self, depth=4, offset=2):
		self.chess = Board()
		self.min_depth = depth
		self.max_depth = depth + offset


	def __call__(self):
		moves = self.chess.legal_moves()
		if len(list(moves)) == 1:
			move = list(moves)[0]
			self.chess(move)
			return move
		with p.ProcessPool(4) as pool:
			func = lambda x: self.alphabeta(copy(self.chess), x, 1)
			values = {k: v for k, v in zip(moves, pool.map(func, moves))}
		try:
			if self.chess.turn():
				move = max(values.items(), key=lambda x: x[1])[0]
				print(f'utility {max(values.items(), key=lambda x: x[1])[1]}')
			else:
				move = min(values.items(), key=lambda x: x[1])[0]
				print(f'utility {min(values.items(), key=lambda x: x[1])[1]}')
			self.chess(move)
			return move
		except:
			print('RESIGN')
			quit()
			


	def alphabeta(self, chess, move, depth, alpha=float('-inf'), beta=float('inf')):
		urgent = chess.is_capture(move)
		chess(move)
		if (depth >= self.min_depth and not urgent) or depth >= self.max_depth:
			return chess.utility()
		moves = chess.legal_moves()
		if len(list(moves)) == 0:
			return chess.utility()
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

