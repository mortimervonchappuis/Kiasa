from board import Board
from kiasa import *


class Game:
	def __init__(self):
		self.chess = Board()
		self.kiasa = Kiasa()

	def __call__(self, move):
		try:
			if self.chess.legal(move):
				self.kiasa.chess(move)
				self.chess(move)
				if self.chess.board.is_game_over():
					print('The Game is over!')
					quit()
				return True
			else:
				return False
		except:
			return False

	def __getitem__(self, pos):
		if type(pos) == int:
			return self.chess.board.piece_at(pos)
		elif type(pos) == str:
			return self.chess.board.piece_at(chess.SQUARE_NAMES.index(pos))

	def answer(self):
		move = self.kiasa()
		self.board = self.chess(move)
