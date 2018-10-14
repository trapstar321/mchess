from board import Board

if __name__=="__main__":
    b = Board()

    print(b)

    p = b.board[6][0]
    print(p.validate_move((5, 1)))
