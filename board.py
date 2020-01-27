import chess
from random import randint
from math import sqrt


class Board:
	def __init__(self):
		self.board = chess.Board()
		self.white_castling = False
		self.black_castling = False
		#self.development_white = {'b1': False, 'c1': False, 'd1': False, 'f1': False, 'g1': False, 'a2': True, 'b2': True, 'c2': True, 'd2': True, 'e2': True}
		#self.development_black = {'b8': False, 'c8': False, 'd8': False, 'f8': False, 'g8': False, 'a7': True, 'b7': True, 'c7': True, 'd7': True, 'e7': True}
		#self.development_white_points = 0
		#self.development_black_points = 0
		self.values = {'R': 5.0, 'N': 3.0, 'B': 3.1, 'Q': 9.0, 'P': 1.0, 'K': 0.8, 'r': 5.0, 'n': 3.0, 'b': 3.21, 'q': 9.0, 'p': 1.0, 'k': 0.8}

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
		if move is None:
			return
		if type(move) == str:
			move = chess.Move.from_uci(move)
		#from_square = chess.SQUARE_NAMES[move.from_square]
		#if self.turn():
		#	if from_square in self.development_white and not self.development_white[from_square]:
		#		self.development_white[from_square] = True
		#		self.development_white_points += 1
		#else:
		#	if from_square in self.development_black and not self.development_black[from_square]:
		#		self.development_black[from_square] = True
		#		self.development_black_points += 1
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
		pawn_rank_factor = 0.05
		file_factor = 0.02
		castling_factor = 1.2
		check_factor = 0.8
		balance_factor = 3
		#development_factor = 1.2

		if self.board.is_game_over():
			if self.board.is_checkmate():
				if self.turn():
					return float('-inf')
				else:
					return float('inf')
			else:
				return 0

		score = 0
		score_white = 0
		score_black = 0
		max_fig_score = 40

		for square, piece in self.board.piece_map().items():
			symbol = piece.symbol()
			if symbol.isupper():
				score_white += self.values[symbol]
				if symbol == 'P':
					score += chess.square_rank(square) * pawn_rank_factor
				else:
					score += chess.square_rank(square) * rank_factor
				score += (4. - abs(chess.square_file(square) - 3.7)) * file_factor
			else:
				score_black -= self.values[symbol]
				if symbol == 'p':
					score -= (7 - chess.square_rank(square)) * pawn_rank_factor
				else:
					score -= (7 - chess.square_rank(square)) * rank_factor
				score -= (4. - abs(chess.square_file(square) - 3.7)) * file_factor

		score += (score_white + score_black) * (1 + 1/sqrt((balance_factor * score_white/max_fig_score)**2 + (balance_factor * score_black/max_fig_score)**2))
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
		#score += self.development_white_points * development_factor
		#score -= self.development_black_points * development_factor
		return score

