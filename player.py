from pieces import *

def init_empty_pieces():
	return {
			 "pawn": [],
			 "bishop":[],
			 "knight": [],
			 "rook": [],
			 "queen": [],
			 "king": [],
			}


class Player:
	def __init__(self, color, is_turn):
		self.color = color
		self.is_turn = is_turn
		self.pieces = init_empty_pieces()
		self.is_in_check = False


	def update_pieces_from_board(self, board):
		self.pieces = init_empty_pieces()
		for i,row in enumerate(board):
			for block in row:
				if block.has_piece and block.piece_color == self.color:
					self.pieces[block.piece_type].append(eval(block.piece_type.capitalize() + "(self.color, block.board_coord)"))					


	def get_piece(self, coord, piece_type):
		for piece in self.pieces[piece_type]:
			if piece.coord == coord:
				return piece
		return None



	def move_piece(self, piece_type, old_coord, new_coord):
		for index in range(len(self.pieces[piece_type])):
			if self.pieces[piece_type][index].coord == old_coord:
				self.pieces[piece_type][index].coord = new_coord


	def get_possible_moves_without_checks(self, coords, board):		
		checks = []
		for piece_type in self.pieces:			
			for piece in self.pieces[piece_type]:
				possible_moves = piece.possible_moves(board) if piece_type != 'pawn' else piece.possible_as_enemy_moves(board)
				for coord in coords:
					if coord in possible_moves:
						checks.append(coord)
		checkless_moves = list(set(coords) - set(checks))
		return checkless_moves


