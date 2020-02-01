from tkinter import *
from PIL import Image, ImageTk
from game import Game
from time import sleep
from playsound import playsound
from chess import SQUARE_NAMES as sqn
from matplotlib import pyplot as plt
from math import exp


def mouse_click(event=None):
	global first, second, game, utilities
	if not game.chess.turn or game.chess.board.is_game_over():
		return
	x = event.x
	y = event.y
	for row in range(8):
		for column in range(7, -1, -1):
			if ((row * 100 + 50 - y) ** 2 + (column * 100 + 50 - x) ** 2) ** 0.5 <= 50:
				if first is None:
					first = (7-row) * 8 + column
				else:
					second = (7-row) * 8 + column
					if game(sqn[first] + sqn[second]) or game(sqn[first] + sqn[second] + 'q'):
						board_update()
						playsound('placement.mp3')
						if not game.chess.board.is_game_over():
							utility = game.answer()
							utilities.append(sigmoid(utility))
							board_update()
							statistics_update()
							playsound('placement.mp3')
					first, second = None, None


def board_update():
	global game, master, full_board
	newboard = Image.open('board_planetary_grey.png')
	newboard = newboard.resize((800,800), Image.ANTIALIAS)
	for i in range(8):
		for j in range(8):
			figure = game[(7-i) * 8 + j]
			if figure:
				figure = str(figure)
				newboard.paste(eval(figure), (j*100 , i*100), eval(figure))
	img = ImageTk.PhotoImage(newboard)
	global full_board
	full_board.configure(image=img)
	full_board.image = img
	master.update()
	if game.chess.board != game.kiasa.chess.board:
		print(game.chess.board, game.kiasa.chess.board)


def statistics_update():
	global statistics, label, plt, utilities
	ax.stackplot(list(range(len(utilities))), utilities, colors = ['#ffffff'])
	plt.xticks(list(range(len(utilities))))
	plt.xlim(0, len(utilities)-1)
	plt.savefig('tmp.png')
	img = ImageTk.PhotoImage(Image.open('tmp.png'))
	label.configure(image=img)
	label.image = img
	statistics.update()


if __name__ == '__main__':
	self_play = True
	opening_book = True
	variation = True

	master = Tk()
	master.geometry("800x800+0+0")
	master.title('KIASA Chess-Engine') # (Kasparov Is A Sexist Arsehole)
	board = Image.open('board_planetary_grey.png')
	
	
	R = Image.open('rook_white_2.png')
	N = Image.open('knight_white_2.png')
	B = Image.open('bishop_white_2.png')
	K = Image.open('king_white_2.png')
	Q = Image.open('queen_white_2.png')
	P = Image.open('pawn_white_2.png')
	r = Image.open('rook_black.png')
	n = Image.open('knight_black.png')
	b = Image.open('bishop_black.png')
	k = Image.open('king_black.png')
	q = Image.open('queen_black.png')
	p = Image.open('pawn_black.png')
	
	R = R.resize((100,100), Image.ANTIALIAS)
	N = N.resize((100,100), Image.ANTIALIAS)
	B = B.resize((100,100), Image.ANTIALIAS)
	K = K.resize((100,100), Image.ANTIALIAS)
	Q = Q.resize((100,100), Image.ANTIALIAS)
	P = P.resize((100,100), Image.ANTIALIAS)
	r = r.resize((100,100), Image.ANTIALIAS)
	n = n.resize((100,100), Image.ANTIALIAS)
	b = b.resize((100,100), Image.ANTIALIAS)
	k = k.resize((100,100), Image.ANTIALIAS)
	q = q.resize((100,100), Image.ANTIALIAS)
	p = p.resize((100,100), Image.ANTIALIAS)
	
	tkimage = ImageTk.PhotoImage(board)
	full_board = Label(master, image=tkimage)
	full_board.pack()
	full_board.bind('<ButtonPress-1>', func=mouse_click)
	game = Game(opening_book, variation)
	first, second = None, None
	second = ()
	board_update()

	statistics = Toplevel(master)
	statistics.title('KIASA Statistics')
	statistics.geometry("1000x400+800+0")
	sigmoid = lambda x: 1/(1+exp(-x*0.2))
	utilities = [0.5]

	fig, ax = plt.subplots(figsize=(10, 4))
	ax.stackplot(list(range(len(utilities))), utilities, colors = ['#ffffff'])
	ax.set_xlabel('Move')
	ax.set_ylabel('Winning Percentage')
	ax.set_facecolor("black")

	plt.ylim(0, 1)
	plt.xlim(0, 1)
	plt.xticks(list(range(len(utilities))))
	plt.yticks([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0], labels=[f'{str(x)}%' for x in range(0, 101, 10)])
	plt.savefig('tmp.png')

	tkimage_s = ImageTk.PhotoImage(Image.open('tmp.png'))
	label = Label(statistics, image=tkimage_s)
	label.pack()

	while self_play and not game.chess.board.is_game_over():
		utility = game.answer()
		board_update()
		utilities.append((utilities[-1] + sigmoid(utility))/2)
		statistics_update()
		playsound('placement.mp3')
	master.mainloop()
	