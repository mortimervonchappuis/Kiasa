from board import Board
from kiasa import *


class Game:
	def __init__(self):
		self.chess = Board()
		self.kiasa = Kiasa()

	def __call__(self, move):
		if self.chess.board.is_game_over():
			return False
		try:
			if self.chess.legal(move):
				self.kiasa.chess(move)
				self.chess(move)
				if self.chess.board.is_game_over():
					print('The Game is over!')
				return True
			else:
				return False
		except:
			return False

	def __getitem__(self, pos):
		return self.chess[pos]
		if type(pos) == int:
			return self.chess.board.piece_at(pos)
		elif type(pos) == str:
			return self.chess.board.piece_at(chess.SQUARE_NAMES.index(pos))

	def answer(self):
		move, util = self.kiasa()
		self.chess(move)
		return util
