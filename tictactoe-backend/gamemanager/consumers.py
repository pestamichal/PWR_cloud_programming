
import json
from channels.generic.websocket import WebsocketConsumer
from . models import GameSession
from asgiref.sync import async_to_sync

class GameSessionConsumer(WebsocketConsumer):

    def connect(self):
        self.room_group_name = 'game_sessions'
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, code):
        pass

    def receive(self, text_data=None, bytes_data=None):

        text_data_json = json.loads(text_data)
        message_type = text_data_json['type']
        session_id = text_data_json['session_id']
        game_session = GameSession.objects.filter(session_id=session_id).first()
        if game_session is None:
            self.send(json.dumps({
                'type': 'gamenotfound',
                'session_id': session_id
            }))
            return

        if message_type == 'cancel':
            game_session.active = False
            game_session.save()
            self.broadcast({
                    'type': 'cancel',
                    'session_id': session_id
                }
            )
        elif message_type == 'move':
            row = text_data_json['row']
            col = text_data_json['col']
            player_type = text_data_json['player_type']
            last_move = game_session.last_move
            board_state = game_session.board_state

            if last_move == player_type:
                return
            if last_move == ' ' and player_type == 'O':
                return
            if board_state[row][col] != ' ':
                return

            game_session.last_move = player_type
            game_session.board_state[row][col] = player_type
            game_session.save()
            board_state = game_session.board_state

            move_count = 0
            for i in range(len(board_state)):
                for j in range(len(board_state[i])):
                    if board_state[i][j] == 'X' or board_state[i][j] == 'O':
                        move_count += 1

            is_winner = self.win_check(board_state, row, col, player_type)
            is_draw = move_count == len(board_state) ** 2

            self.broadcast({
                    'type': 'move',
                    'session_id': session_id,
                    'board_state': game_session.board_state
                }
            )
            if is_winner or is_draw:
                self.broadcast({
                    'type': 'result',
                    'session_id': session_id,
                    'winner': is_winner,
                    'player_type': player_type,
                    'draw': is_draw
                })

        elif message_type == 'joined' and game_session.player2 != '':
            self.broadcast({
                    'type': 'begin_game',
                    'session_id': session_id
                }
            )

        elif message_type == 'init':
            is_active = game_session.active
            players_ready = game_session.player2 != ''
            board_state = game_session.board_state
            self.send(json.dumps({
                'type': 'init',
                'session_id': session_id,
                'is_active': is_active,
                'players_ready': players_ready,
                'board_state': board_state
            }))

        elif message_type == 'playagain':
            game_session.board_state = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
            if game_session.last_move != ' ':
                game_session.last_move = ' '
            else:
                self.broadcast({
                    'type': 'begin_game',
                    'session_id': session_id,
                })
            game_session.save()


    def broadcast(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'send_message',
                'message': message
            }
        )

    def send_message(self, event):
        self.send(text_data=json.dumps(event['message']))

    def win_check(self, board_state, x, y, symbol):
        column_counter = 0
        row_counter = 0
        diagonal_count = 0
        reversed_diagonal_count = 0
        n = len(board_state)
        for i in range(len(board_state)):
            if board_state[x][i] == symbol:
                column_counter += 1
            if board_state[i][y] == symbol:
                row_counter += 1
            if board_state[i][i] == symbol:
                diagonal_count += 1
            if board_state[i][n - 1 - i] == symbol:
                reversed_diagonal_count += 1

        return row_counter == n or column_counter == n or diagonal_count == n or reversed_diagonal_count == n



