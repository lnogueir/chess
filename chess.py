import pygame, numpy, copy
from pieces import *
from board_assets import Block, initialize_board, piece2number, number2piece, transformation_matrix
from player import Player

# For every case that make sense, True represents Black's turn and False represents White's turn. 


COLORS = {
	'lightbrown': (133, 82, 11), 
	'black': (0, 0, 0), 
	'white': (255, 255, 255)
	}


class Window:
	WINDOW_SIZE = 800
	ROWS = 8
	def __init__(self):
		pygame.init()
		self.window = pygame.display.set_mode((self.WINDOW_SIZE, self.WINDOW_SIZE))


	def drawGrid(self):
		sizeBtwn = self.WINDOW_SIZE // self.ROWS
		flag = False
		for i in range(self.ROWS):
			for j in range(self.ROWS):
				if flag:
					pygame.draw.rect(self.window, COLORS['lightbrown'], (j*sizeBtwn, i*sizeBtwn, sizeBtwn, sizeBtwn))
				else:
					pygame.draw.rect(self.window, COLORS['white'], (j*sizeBtwn, i*sizeBtwn, sizeBtwn, sizeBtwn))
				flag = not(flag)
			flag = not(flag)		


	@staticmethod		
	def addCheckMessage(user_in_check):
		pygame.display.set_caption(f'{user_in_check} is in Check! You must take action')

	@staticmethod
	def addCheckMateMessage(winner):
		pygame.display.set_caption(f'CHECKMATE! {winner} is the winner')		

	@staticmethod
	def addTitle():
		pygame.display.set_caption("Lucas' Chess")

	def redraw(self, board):
		self.window.fill(COLORS['white'])
		self.drawGrid()
		for row in board:
			for block in row:
				block.draw_piece(self.window)
				block.draw_possible_moves(self.window)
		pygame.display.update()
	

def reset_check_status(p1, p2):
	p1.is_in_check = False
	p2.is_in_check = False


def will_check(board, checking_player, checked_player):
		for _type in checking_player.pieces:
			for piece in checking_player.pieces[_type]:
				possible_moves = piece.possible_moves(board)
				if checked_player.pieces['king'][0].coord in possible_moves:
					return True
		return False


class Chess:
	def __init__(self):		
		self.clock = pygame.time.Clock()
		self.white = Player('white', True)
		self.black = Player('black', False)
		self.board = initialize_board('white')
		self.possible_moves = []
		self.selected = None
		self.selected_piece = None
		self.is_check_mate = False


	def rotate_board(self):
		holder_matrix = numpy.zeros((8,8))
		for i,row in enumerate(self.board):
			for j, block in enumerate(row):
				if block.has_piece:
					holder_matrix[i,j] = piece2number[block.piece_color+" "+block.piece_type]
				else:
					holder_matrix[i,j] = 0
		holder_matrix = (transformation_matrix * holder_matrix * transformation_matrix).tolist()
		for i,row in enumerate(holder_matrix):
			for j,piece_id in enumerate(row):
				if int(piece_id) != 0:
					hold_color_and_type = number2piece[piece_id].split(' ') 
					color = hold_color_and_type[0]
					piece_type = hold_color_and_type[1]
					self.board[i][j] = Block((i,j), piece_type, color)
				else:
					self.board[i][j] = Block((i,j))


	def is_checking_mate(self, checking_player, checked_player):
		self.is_check_mate = False
		possible_moves = []
		for _type in checked_player.pieces:
			for piece in checked_player.pieces[_type]:
				possible_moves += self.get_possible_moves(piece)
			break	
		print(possible_moves)		
		self.is_check_mate = len(possible_moves) == 0


	def find_piece_given_coord(self, board_coord_clicked):
		x = board_coord_clicked[0]
		y = board_coord_clicked[1]
		click = self.board[x][y]
		result = {'color': click.piece_color, 'type': click.piece_type, 'board_coord': (board_coord_clicked)}		
		if result['color'] == 'white':
			return self.white.get_piece(board_coord_clicked, result['type'])
		elif result['color'] == 'black':
			return self.black.get_piece(board_coord_clicked, result['type'])
		return None

	def update_possible_moves_on_board(self):		
		for row in self.board:
			for block in row:
				if self.possible_moves and block.board_coord in self.possible_moves:
					block.is_possible_move = True
				else:
					block.is_possible_move = False


	def track_selected_piece(self, clicked_piece): # consertar bug
		if self.selected:
			if self.selected['coord'] !=	clicked_piece.coord:
				self.selected = {'coord':clicked_piece.coord,'color':clicked_piece.color}
				self.board[self.selected['coord'][0]][self.selected['coord'][1]].is_selected = False
			else:
				if self.selected['color'] == clicked_piece.color:
					self.board[self.selected['coord'][0]][self.selected['coord'][1]].is_selected = not self.board[self.selected['coord'][0]][self.selected['coord'][1]].is_selected	
				self.selected = {'coord':clicked_piece.coord,'color':clicked_piece.color}
		else:
			self.selected = {'coord': clicked_piece.coord, 'color': clicked_piece.color}
			self.board[self.selected['coord'][0]][self.selected['coord'][1]].is_selected = False		


	def block_auto_check(self, possible_moves, piece_found):
		checks = []
		piece_type = piece_found.__class__.__name__.lower()
		for move in possible_moves:
			simulation_result = self.get_simulated_board_and_possible_eated_piece(piece_found.coord, move, piece_type, piece_found.color)
			simulated_board = simulation_result[0]
			possible_piece_found = simulation_result[1]
			if self.white.is_turn:
				for p_type in self.black.pieces:
					for piece in self.black.pieces[p_type]:
						enemy_possible_moves = piece.possible_moves(simulated_board) if p_type != 'pawn' else piece.possible_as_enemy_moves(simulated_board)
						if piece_found.__class__.__name__ != 'King':	
							if self.white.pieces['king'][0].coord in enemy_possible_moves:
								checks.append(move)
						else:
							if move in enemy_possible_moves:
								checks.append(move)							
			else:
				for p_type in self.white.pieces:
					for piece in self.white.pieces[p_type]:
						enemy_possible_moves = piece.possible_moves(simulated_board) if p_type != 'pawn' else piece.possible_as_enemy_moves(simulated_board)						
						if piece_found.__class__.__name__ != 'King':
							if self.black.pieces['king'][0].coord in enemy_possible_moves:
								checks.append(move)
						else:
							if move in enemy_possible_moves:
								checks.append(move)	
			if possible_piece_found:
				_type = possible_piece_found.__class__.__name__.lower()
				if possible_piece_found.color == 'white': 
					self.white.pieces[_type].append(possible_piece_found)
				elif possible_piece_found.color == 'black':
					self.black.pieces[_type].append(possible_piece_found)
		checkless_moves = list(set(possible_moves) - set(checks))
		return checkless_moves						


	def get_possible_moves(self, piece_found):
		possible_moves = []
		if piece_found and not self.board[piece_found.coord[0]][piece_found.coord[1]].is_selected:
			possible_moves = piece_found.possible_moves(self.board)
			possible_moves = self.block_auto_check(possible_moves,piece_found)
		else: 
			possible_moves = []
		return possible_moves	


	def handle_board_rotation(self):
		self.rotate_board()
		self.black.update_pieces_from_board(self.board)
		self.white.update_pieces_from_board(self.board)	


	def get_simulated_board_and_possible_eated_piece(self, old_coord, new_coord, piece_type, piece_color):
		simulated_board = copy.deepcopy(self.board)
		simulated_board[old_coord[0]][old_coord[1]].update_piece_status(False)
		piece_found = self.find_piece_given_coord((new_coord[0],new_coord[1]))
		if piece_found:
			piece_found_type = piece_found.__class__.__name__.lower()
			if piece_found.color != piece_color:
				if piece_found.color == 'black':
					self.black.pieces[piece_found_type].remove(piece_found)
				elif piece_found.color == 'white':
					self.white.pieces[piece_found_type].remove(piece_found)
		simulated_board[new_coord[0]][new_coord[1]].update_piece_status(True, piece_type, piece_color)
		return simulated_board, piece_found



	def handle_piece_movement(self, coord):
		reset_check_status(self.white, self.black)
		x, y = coord[0], coord[1]
		piece_type = self.selected_piece.__class__.__name__.lower()
		if self.board[x][y].is_possible_move and self.selected_piece:
			x_old, y_old = self.selected_piece.coord[0], self.selected_piece.coord[1]
			self.board[x_old][y_old].update_piece_status(False)
			piece_found = self.find_piece_given_coord((x,y))
			if piece_found:
				piece_found_type = piece_found.__class__.__name__.lower()
				if piece_found.color == 'black' and self.black.is_turn:
					self.black.pieces[piece_found_type].remove(piece_found)
				elif piece_found.color == 'white' and self.white.is_turn:
					self.white.pieces[piece_found_type].remove(piece_found)	
			self.board[x][y].update_piece_status(True, piece_type, self.selected_piece.color)
			if self.selected_piece.color == 'white' and self.white.is_turn:
				self.white.move_piece(piece_type, self.selected_piece.coord, coord)
				if piece_type == 'king' or piece_type == 'rook' and not self.selected_piece.has_moved:
					i = 0
					while i < len(self.white.pieces[piece_type]):
						if self.white.pieces[piece_type][i].coord == self.selected_piece.coord:
							self.white.pieces[piece_type][i].has_moved = True
							break
					self.white.pieces[piece_type][0].has_moved = True
				self.black.is_in_check = will_check(self.board, self.white, self.black)
				self.white.is_turn = False
				self.black.is_turn = True
				self.handle_board_rotation()
				if self.black.is_in_check:
					self.is_checking_mate(self.white, self.black)
					if not self.is_check_mate:
						Window.addCheckMessage('black')
					else:
						Window.addCheckMateMessage('white')
				return True
			elif self.selected_piece.color == 'black' and self.black.is_turn:	
				self.black.move_piece(piece_type, self.selected_piece.coord, coord)
				if piece_type == 'king' or piece_type == 'rook' and not self.selected_piece.has_moved:
					i = 0
					while i < len(self.white.pieces[piece_type]):
						if self.black.pieces[piece_type][i].coord == self.selected_piece.coord:
							self.black.pieces[piece_type][i].has_moved = True
							break
				self.white.is_in_check = will_check(self.board, self.black, self.white)	
				self.black.is_turn = False
				self.white.is_turn = True
				self.handle_board_rotation()
				if self.white.is_in_check:
					self.is_checking_mate(self.black, self.white)
					if not self.is_check_mate:
						Window.addCheckMessage('white')
					else:
						Window.addCheckMateMessage('black')
				return True
			else:
				return False		
				


	def initialize_players_board(self):
		self.white.update_pieces_from_board(self.board)
		self.black.update_pieces_from_board(self.board)	
		


	def run(self):
		win = Window()
		Window.addTitle()
		self.initialize_players_board()
		crash = False
		will_move=False
		while not crash:
			pygame.time.delay(50)
			self.clock.tick(10)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					crash = True
					break
				if event.type == pygame.MOUSEBUTTONDOWN:
					board_coord_clicked = (event.pos[0]//100, event.pos[1]//100)
					will_move = self.handle_piece_movement(board_coord_clicked)
					clicked_piece = self.find_piece_given_coord(board_coord_clicked)
					if clicked_piece and not will_move:
						if (self.black.is_turn and clicked_piece.color == 'black') or (self.white.is_turn and clicked_piece.color == 'white'):
							self.selected_piece = clicked_piece							
							self.track_selected_piece(clicked_piece)
							self.possible_moves = self.get_possible_moves(self.selected_piece)
					else:
						self.possible_moves = []
			self.update_possible_moves_on_board()		
			win.redraw(self.board)
		pygame.quit()


game = Chess()
game.run()

	



