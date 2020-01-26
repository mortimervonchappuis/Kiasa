from tkinter import *
from PIL import Image, ImageTk
from game import Game
from time import sleep
from playsound import playsound
from chess import SQUARE_NAMES as sqn


def mouse_click(event=None):
	global first, second, game
	if not game.chess.turn:
		return
	x = event.x
	y = event.y
	for row in range(8):
		for column in range(7, -1, -1):
			if ((row * 100 + 50 - y) ** 2 + (column * 100 + 50 - x) ** 2) ** 0.5 <= 50:
				if not first:
					first = (7-row) * 8 + column
				else:
					second = (7-row) * 8 + column
					if game(sqn[first] + sqn[second]) or game(sqn[first] + sqn[second] + 'q'):
						board_update()
						playsound('placement.mp3')
						game.answer()
						board_update()
						playsound('placement.mp3')
					first, second = (), ()


def board_update():
	global game, master, full_board
	newboard = Image.open("board.png")
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
	return


if __name__ == '__main__':
	master = Tk()
	master.title("KIASA Chess-Engine") # (Kasparov Is A Sexist Arsehole)
	board = Image.open("board.png")
	
	R = Image.open("rook_white.png")
	N = Image.open("knight_white.png")
	B = Image.open("bishop_white.png")
	K = Image.open("king_white.png")
	Q = Image.open("queen_white.png")
	P = Image.open("pawn_white.png")
	r = Image.open("rook_black.png")
	n = Image.open("knight_black.png")
	b = Image.open("bishop_black.png")
	k = Image.open("king_black.png")
	q = Image.open("queen_black.png")
	p = Image.open("pawn_black.png")
	
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
	full_board.bind("<ButtonPress-1>", func=mouse_click)
	game = Game()
	first = ()
	second = ()
	board_update()
	#while True:
	#	board_update()
	#	playsound('placement.mp3')
	#	game.answer()
	master.mainloop()
	