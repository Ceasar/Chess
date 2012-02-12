from itertools import product

from player import Color
from move import Move


class Piece(object):
    """Abstract base class for pieces."""
    def __init__(self, owner, location):
        self.owner = owner
        self.x, self.y = location

    def get_location(self):
        return self.x, self.y
    def set_location(self, value):
        self.x, self.y = value
    location = property(get_location, set_location)

    def reachable(self, board):
        """Get all the square reachable from the piece's current location."""
        pass

    def moves(self, board):
        """Get all the possible moves for the piece."""
        for square in self.reachable(board):
            yield Move(self, square)

    def can_reach(self, board, square):
        """Check if the given square is reachable."""
        return any(s == square for s in self.reachable(board))

    def __repr__(self):
        return "%s %s" % (self.__class__, self.location)


class Pawn(Piece):
    def reachable(self, board):
        if self.owner.color == Color.WHITE:
            vector = 1
            start_rank = 1
        else:
            vector = -1
            start_rank = 6
        forward_1 = self.x, self.y + vector
        if not board.piece_at(forward_1):
            yield forward_1
            if self.y == start_rank:
                forward_2 = self.x, self.y + vector * 2
                if not board.piece_at(forward_2):
                    yield forward_2
        attack1 = self.x - 1, self.y + vector
        piece = board.piece_at(attack1)
        if piece is not None and piece.owner != self.owner:
            yield attack1
        attack2 = self.x + 1, self.y + vector
        piece = board.piece_at(attack2)
        if piece is not None and piece.owner != self.owner:
            yield attack2


class Bishop(Piece):
    def reachable(self, board):
        # TODO: Don't bs this
        yield self.x + 1, self.y + 1


class Knight(Piece):
    def reachable(self, board):
        yield self.x + 1, self.y + 2
        yield self.x + 1, self.y - 2
        yield self.x - 1, self.y + 2
        yield self.x - 1, self.y - 2

        yield self.x + 2, self.y + 1
        yield self.x + 2, self.y - 1
        yield self.x - 2, self.y + 1
        yield self.x - 2, self.y - 1


class Rook(Piece):
    def reachable(self, board):
        x = self.x + 1
        while x < board.width:
            loc = (x, self.y)
            piece = board.piece_at(loc)
            if piece is None:
                yield loc
            else:
                if piece.owner != self.owner:
                    yield loc
                break
            x += 1
        

        x = self.x - 1
        while x >= 0:
            loc = (x, self.y)
            piece = board.piece_at(loc)
            if piece is None:
                yield loc
            else:
                if piece.owner != self.owner:
                    yield loc
                break
            x -= 1

        y = self.y - 1
        while y >= 0:
            loc = (self.x, y)
            piece = board.piece_at(loc)
            if piece is None:
                yield loc
            else:
                if piece.owner != self.owner:
                    yield loc
                break
            y -= 1

        y = self.y + 1
        while y < board.height:
            loc = (self.x, y)
            piece = board.piece_at(loc)
            if piece is None:
                yield loc
            else:
                if piece.owner != self.owner:
                    yield loc
                break
            y += 1


class King(Piece):
  def reachable(self, board):
    for x, y in product(range(-1, 2), range(-1, 2)):
      if not (x == y == 0):
        to = new_x, new_y = (self.x + x, self.y + y)
        if 7 >= new_x >= 0 and 7 >= new_y >= 0:
          piece = board.piece_at(to)
          if piece is None or piece.owner != self.owner:
            yield to


class Queen(Piece):
  def reachable(self, board):
    #TODO: Do this right
    for x, y in product(range(-1, 2), range(-1, 2)):
      if not (x == y == 0):
        to = new_x, new_y = (self.x + x, self.y + y)
        if 7 >= new_x >= 0 and 7 >= new_y >= 0:
          piece = board.piece_at(to)
          if piece is None or piece.owner != self.owner:
            yield to
