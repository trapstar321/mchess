from NIO_python.common.log_optional import Logger
from server.game_server.messages.CM_GAMEKEY import CM_GAMEKEY
from server.game_server.messages.CM_MOVE import CM_MOVE
from server.game_server.messages.SM_STARTGAME import SM_STARTGAME
from server.game_server.messages.CM_QUIT import CM_QUIT
from server.game_server.messages.SM_MOVEOK import SM_MOVEOK
from server.game_server.messages.SM_MOVEERROR import SM_MOVEERROR
from server.game_server.messages.SM_TURN import SM_TURN
from server.game_server.messages.SM_QUIT import SM_QUIT
from server.game_server.messages.SM_ROUNDINFO import SM_ROUNDINFO
from NIO_python.server.messages.SM_CONNECTED import SM_CONNECTED
from NIO_python.server.messages.SM_DISCONNECTED import SM_DISCONNECTED

from utils.aes import decrypt, from_hex

from random import randint
from constants import X, Y, WHITE, BLACK, EAT
import traceback
import math

logger = Logger(1)
clients = {}
requests = {}
games = {}

from ui.game.board import Board

class Round:
    def __init__(self, round):
        self.round = round
        self.figure1 = None
        self.figure2 = None

        self.result1 = None
        self.result2 = None

    def move(self, figure, result):
        if self.figure1 is None:
            self.figure1 = figure
            self.result1 = result
        else:
            self.figure2 = figure
            self.result2 = result

    def __str__(self):
        pos1 = Board.position_to_cell(self.figure1.position[X], self.figure1.position[Y])
        pos1_str = self.figure1.short_name()+("x" if self.result1 == EAT else "")+pos1[0] + str(pos1[1])

        pos2_str = ""
        if self.figure2 is not None:
            pos2 = Board.position_to_cell(self.figure2.position[X], self.figure2.position[Y])
            pos2_str = self.figure2.short_name()+("x" if self.result2 == EAT else "")+pos2[0] + str(pos2[1])

        return "{0}  {1} {2}".format(self.round, pos1_str, pos2_str)

class Game:
    def __init__(self, board, player1, player2):
        self.board = board
        self.player1 = player1
        self.player2 = player2

        self.move_ = 0
        self.round = 0

        self.rounds = {}

    def move(self, source, result):
        self.move_ += 1
        self.round = math.ceil(self.move_/2)

        if self.round not in self.rounds:
            self.rounds[self.round] = Round(self.round)

        round = self.rounds[self.round]
        round.move(source, result)

        return round

class Player:
    def __init__(self, id, side):
        self.id = id
        self.side = side

def process_messages(messages, conf, client_id):
    try:
        smessages = []
        for message in messages:
            logger.log("Processor received message: {0}".format(message))

            if message["opcode"] == SM_CONNECTED.OP_CODE:
                clients[message["id"]] = {}
            elif message["opcode"] == SM_DISCONNECTED.OP_CODE:
                logger.log("Client {0} disconnected".format(message["id"]))
            elif message["opcode"] == CM_QUIT.OP_CODE:
                msg = CM_QUIT(message["data"])
                game = games[msg.key]

                ret = SM_QUIT(msg.key)
                if message["id"] == game.player1.id:
                    smessages.append({"id": game.player2.id, "opcode": ret.OP_CODE, "data": ret.get_data()})
                else:
                    smessages.append({"id": game.player1.id, "opcode": ret.OP_CODE, "data": ret.get_data()})

                del games[msg.key]
            elif message["opcode"] == CM_GAMEKEY.OP_CODE:
                msg = CM_GAMEKEY(message["data"])

                if msg.key in requests:
                    dest1 = message["id"]
                    dest2 = requests[msg.key]
                    del requests[msg.key]

                    #1=white, 0=black
                    res = randint(0,1)

                    if res==1:
                        p1 = Player(dest1, WHITE)
                        p2 = Player(dest2, BLACK)
                        msg1 = SM_STARTGAME(True)
                        msg2 = SM_STARTGAME(False)
                        games[msg.key] = Game(Board(), p1, p2)
                    else:
                        p1 = Player(dest1, BLACK)
                        p2 = Player(dest2, WHITE)
                        msg1 = SM_STARTGAME(False)
                        msg2 = SM_STARTGAME(True)
                        games[msg.key] = Game(Board(), p1, p2)

                    smessages.append({"id": dest1, "opcode": msg1.OP_CODE, "data": msg1.get_data()})
                    smessages.append({"id": dest2, "opcode": msg2.OP_CODE, "data": msg2.get_data()})
                else:
                    requests[msg.key] = message["id"]
            elif message["opcode"]==CM_MOVE.OP_CODE:
                msg = CM_MOVE(message["data"])
                logger.log("Source: {0}".format(msg.source))
                logger.log("Target: {0}".format(msg.target))
                game = games[msg.key]
                board = games[msg.key].board
                source = board.board[msg.source[X]][msg.source[Y]]
                target = board.board[msg.target[X]][msg.target[Y]]

                ret = board.move(source, target)
                logger.log("Move response = {0}".format(ret))
                if ret[0]:
                    msg = SM_MOVEOK(msg.source, msg.target)
                    smessages.append({"id": game.player1.id, "opcode": msg.OP_CODE, "data": msg.get_data()})
                    smessages.append({"id": game.player2.id, "opcode": msg.OP_CODE, "data": msg.get_data()})

                    round = game.move(source, ret[1])
                    logger.log("Round = {0}".format(round))

                    msg = SM_ROUNDINFO(round.round, str(round))
                    smessages.append({"id": game.player1.id, "opcode": msg.OP_CODE, "data": msg.get_data()})
                    smessages.append({"id": game.player2.id, "opcode": msg.OP_CODE, "data": msg.get_data()})

                    if game.player1.id==message["id"]:
                        msg1 = SM_TURN(False)
                        msg2 = SM_TURN(True)
                        smessages.append({"id": game.player1.id, "opcode": msg1.OP_CODE, "data": msg1.get_data()})
                        smessages.append({"id": game.player2.id, "opcode": msg2.OP_CODE, "data": msg2.get_data()})
                    else:
                        msg1 = SM_TURN(True)
                        msg2 = SM_TURN(False)
                        smessages.append({"id": game.player1.id, "opcode": msg1.OP_CODE, "data": msg1.get_data()})
                        smessages.append({"id": game.player2.id, "opcode": msg2.OP_CODE, "data": msg2.get_data()})
                else:
                    msg = SM_MOVEERROR(msg.source, msg.target)
                    smessages.append({"id": game.player1.id, "opcode": msg.OP_CODE, "data": msg.get_data()})
                    smessages.append({"id": game.player2.id, "opcode": msg.OP_CODE, "data": msg.get_data()})

        for msg in smessages:
            logger.log("Send message {0}".format(msg))

        return smessages
    except Exception as ex:
        logger.log('process_messages exception: {0}'.format(ex))
        traceback.print_tb(ex.__traceback__)