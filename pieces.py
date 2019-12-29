import pygame
from board_assets import number2piece

class Piece():
	def __init__(self, color, coord):
		self.color = color
		self.coord = coord


	#NOTE: where there is != self.color, that means that you are eating a piece.	
	def possible_moves(self, board):
		pass


class Pawn(Piece):
	def __init__(self,color, coord):
		Piece.__init__(self, color, coord)


	def possible_moves(self, board):
		result = []
		x = self.coord[0]
		y = self.coord[1]
		if y > 0:
			if x > 0 and board[x-1][y-1].has_piece:
				if board[x-1][y-1].piece_color != self.color:
					result.append((x-1, y-1))
			if x < 7 and board[x+1][y-1].has_piece:
				if board[x+1][y-1].piece_color != self.color:
					result.append((x+1, y-1))
			if not board[x][y-1].has_piece:
				result.append((x, y-1))
				if y == 6 and not board[x][y-2].has_piece:
					result.append((x, y-2))	
		return result		
		
	def possible_as_enemy_moves(self, board):
		result = []
		x = self.coord[0]
		y = self.coord[1]
		if y < 7:
			if x > 0 and board[x-1][y+1].has_piece:
				if board[x-1][y-1].piece_color != self.color:
					result.append((x-1, y+1))
			if x < 7 and board[x+1][y+1].has_piece:
				if board[x+1][y+1].piece_color != self.color:
					result.append((x+1, y+1))
		return result		
			
	

def bishop_move(piece_obj, board):
	result = []
	color = piece_obj.color
	x = piece_obj.coord[0]
	y = piece_obj.coord[1]	
	while x < 7 and y > 0:
		x+=1
		y-=1
		if not board[x][y].has_piece:
			result.append((x,y))
		else:	
			if board[x][y].piece_color != color:
				result.append((x,y))
			break
	x = piece_obj.coord[0]
	y = piece_obj.coord[1]
	while x < 7	and y < 7:
		x+=1
		y+=1
		if not board[x][y].has_piece:
			result.append((x,y))
		else:
			if board[x][y].piece_color != color:
				result.append((x,y))
			break
	x = piece_obj.coord[0]
	y = piece_obj.coord[1]
	while x > 0 and y > 0:
		x-=1
		y-=1
		if not board[x][y].has_piece:
			result.append((x,y))
		else:
			if board[x][y].piece_color != color:
				result.append((x,y))
			break
	x = piece_obj.coord[0]
	y = piece_obj.coord[1]
	while x > 0 and y < 7:
		x-=1
		y+=1
		if not board[x][y].has_piece:
			result.append((x,y))
		else:
			if board[x][y].piece_color != color:
				result.append((x,y))
			break	
	return result	


class Bishop(Piece):
	def __init__(self,color, coord):
		Piece.__init__(self, color, coord)

	def possible_moves(self, board):
		return bishop_move(self, board)
		



class Knight(Piece):
	def __init__(self,color, coord):
		Piece.__init__(self, color, coord)
	
	def possible_moves(self, board):
		result = []
		x = self.coord[0] + 2
		y = self.coord[1] + 1
		for i in range(2):
			if x >= 0 and x <= 7 and y <= 7 and y >= 0: 
				if not board[x][y].has_piece:
					result.append((x,y))
				else:
					if board[x][y].piece_color != self.color:
						result.append((x,y))
			y-=2	
		x = self.coord[0] + 1 
		y = self.coord[1] + 2	
		for i in range(2):
			if x >= 0 and x <= 7 and y <= 7 and y >= 0: 
				if not board[x][y].has_piece:
					result.append((x,y))
				else:
					if board[x][y].piece_color != self.color:
						result.append((x,y))				
			y-=4
		x = self.coord[0] - 1
		y = self.coord[1] + 2
		for i in range(2):
			if x >= 0 and x <= 7 and y <= 7 and y >= 0: 
				if not board[x][y].has_piece:
					result.append((x,y))
				else:
					if board[x][y].piece_color != self.color:
						result.append((x,y))				
			y-=4
		x = self.coord[0] - 2
		y = self.coord[1] + 1
		for i in range(2):
			if x >= 0 and x <= 7 and y <= 7 and y >= 0: 
				if not board[x][y].has_piece:
					result.append((x,y))
				else:
					if board[x][y].piece_color != self.color:
						result.append((x,y))				
			y-=2
		return result	






def rook_move(piece_obj, board):
	result = []
	color = piece_obj.color
	x = piece_obj.coord[0]
	y = piece_obj.coord[1]
	while x < 7:
		x+=1
		if not board[x][y].has_piece:
			result.append((x,y))
		else:
			if board[x][y].piece_color != color:
				result.append((x,y))
			break
	x = piece_obj.coord[0]
	while x > 0:
		x-=1
		if not board[x][y].has_piece:
			result.append((x,y))
		else:
			if board[x][y].piece_color != color:
				result.append((x,y))
			break
	x = piece_obj.coord[0]
	while y > 0:
		y-=1
		if not board[x][y].has_piece:
			result.append((x,y))
		else:
			if board[x][y].piece_color != color:
				result.append((x,y))
			break		
	y = piece_obj.coord[1]
	while y < 7:
		y+=1
		if not board[x][y].has_piece:
			result.append((x,y))
		else:
			if board[x][y].piece_color != color:
				result.append((x,y))
			break	
	return result

class Rook(Piece):
	def __init__(self,color, coord):
		self.has_moved = False
		Piece.__init__(self, color, coord)

	def possible_moves(self, board):
		return rook_move(self, board)


class Queen(Piece):
	def __init__(self,color, coord):
		Piece.__init__(self, color, coord)

	def possible_moves(self, board):
		return rook_move(self, board) + bishop_move(self, board)


class King(Piece):
	def __init__(self,color, coord):
		self.has_moved = False
		Piece.__init__(self, color, coord)


	def possible_moves(self, board):
		result = []
		x = self.coord[0]
		y = self.coord[1]
		if y+1 <= 7:
			if not board[x][y+1].has_piece:
				result.append((x,y+1))
			else:
				if board[x][y+1].piece_color != self.color:
					result.append((x,y+1))
		if y-1 >= 0:
			if not board[x][y-1].has_piece:
				result.append((x,y-1))
			else:
				if board[x][y-1].piece_color != self.color:
					result.append((x,y-1))
		if x-1 >= 0:
			if not board[x-1][y].has_piece:
				result.append((x-1,y))
			else:
				if board[x-1][y].piece_color != self.color:
					result.append((x-1,y))
		if x+1 <= 7:
			if not board[x+1][y].has_piece:
				result.append((x+1,y))
			else:
				if board[x+1][y].piece_color != self.color:
					result.append((x+1,y))
		if x+1 <= 7 and y+1	<= 7:
			if not board[x+1][y+1].has_piece:
				result.append((x+1,y+1))
			else:
				if board[x+1][y+1].piece_color != self.color:
					result.append((x+1,y+1))		
		if x+1 <= 7 and y-1 >= 0:
			if not board[x+1][y-1].has_piece:
				result.append((x+1,y-1))
			else:
				if board[x+1][y-1].piece_color != self.color:
					result.append((x+1,y-1))				
		if x-1 >= 0 and y-1 >= 0:
			if not board[x-1][y-1].has_piece:
				result.append((x-1,y-1))
			else:
				if board[x-1][y-1].piece_color != self.color:
					result.append((x-1,y-1))												
		if x-1 >= 0 and y+1 <= 7:
			if not board[x-1][y+1].has_piece:
				result.append((x-1,y+1))
			else:
				if board[x-1][y+1].piece_color != self.color:
					result.append((x-1,y+1))
		return result							



