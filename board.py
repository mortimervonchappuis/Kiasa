import chess
from random import randint


class Board:
	def __init__(self):
		self.board = chess.Board()
		self.white_castling = False
		self.black_castling = False

	def get_colour(self, pos):
		if type(pos) == int:
			return self.board.color_at(pos)
		elif type(pos) == str:
			return self.board.color_at(chess.SQUARE_NAMES.index(pos))

	def __getitem__(self, pos):
		if type(pos) == int:
			return self.board.piece_at(pos)
		elif type(pos) == str:
			return self.board.piece_at(chess.SQUARE_NAMES.index(pos))

	def __call__(self, move):
		if type(move) == str:
			move = chess.Move.from_uci(move)
		if self.board.is_castling(move):
			if self.turn():
				self.white_castling = True
			else:
				self.black_castling = True
		self.board.push(move)

	def is_capture(self, move):
		return self.board.is_capture(move)

	def legal(self, move):
		return self.board.is_legal(chess.Move.from_uci(move))

	def legal_moves(self):
		return [move for move in self.board.legal_moves if self.board.is_legal(move)]

	def turn(self):
		return self.board.turn

	def utility(self):
		rank_factor = 0.1
		file_factor = 0.02
		castling_factor = 1.2
		check_factor = 0.8

		if self.board.is_game_over():
			if self.board.is_checkmate():
				if self.turn():
					return float('-inf')
				else:
					return float('inf')
			else:
				return 0
		score = 0
		pieces = self.board.piece_map()
		values = {'R': +5.0, 'N': +3.0, 'B': +3.2, 'Q': +9.0, 'P': +1.0, 'K': +0, 'r': -5.0, 'n': -3.0, 'b': -3.2, 'q': -9.0, 'p': -1.0, 'k': -0}
		for square, piece in pieces.items():
			symbol = piece.symbol()
			score += values[symbol]
			if symbol.isupper():
				score += chess.square_rank(square)*rank_factor
				score += (4 - abs(4 - chess.square_file(square)))*file_factor
			else:
				score -= (7 - chess.square_rank(square)) * rank_factor
				score -= (4 - abs(4 - chess.square_file(square)))*file_factor
		if self.white_castling:
			score += castling_factor
		elif not self.board.has_castling_rights(True):
			score -= castling_factor
		if self.black_castling:
			score -= castling_factor
		elif not self.board.has_castling_rights(False):
			score += castling_factor
		if self.board.is_check():
			if self.turn():
				score -= check_factor
			else:
				score += check_factor
		return score

