from color import Color


class Board(object):
    def __init__(self, pieces=None):
        self._pieces = pieces or {}
        assert type(self._pieces) == dict

    width = 8
    height = 8
    squares = {(x, y) for x in range(8) for y in range(8)}

    @property
    def pieces(self):
        return self._pieces.values()

    def is_on_board(self, location):
        """Check if a location is on the board."""
        return location in self.squares

    def piece_at(self, location):
        """Get the piece at a given location or None if no piece is found."""
        return self._pieces.get(location, None)

    def add_piece(self, piece):
        """Add a piece to the board."""
        assert self.piece_at(piece.location) is None
        self._pieces[piece.location] = piece
        piece.owner.pieces.add(piece)

    def move_piece(self, piece, loc):
        """Move a piece to the specified square."""
        self.remove_piece(piece)
        piece._location = loc
        self.add_piece(piece)

    def remove_piece(self, piece):
        """Remove a piece from the board."""
        assert self.piece_at(piece.location) == piece
        piece.owner.pieces.remove(piece)
        del self._pieces[piece.location]

    def __eq__(self, other):
        return self._pieces == other._pieces

    def __ne__(self, other):
        return not (self == other)

    def __str__(self):
        a = [[" " for i in xrange(8)] for x in xrange(8)]
        ret = ""
        divide = "+-+-+-+-+-+-+-+-+\n"
        for piece in self.pieces:
            piece_str = str(piece)[0]
            if str(piece) == "Knight":
                piece_str = "N"
            if piece.owner.color == Color.BLACK:
                piece_str = piece_str.lower()
            a[7 - piece.location[1]][piece.location[0]] = piece_str
        for row in a:
            ret += divide
            for sq in row:
                if sq:
                    ret += "|" + sq
            ret += "|\n"
        return ret + divide
