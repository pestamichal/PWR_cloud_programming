
import json
from channels.generic.websocket import WebsocketConsumer
from . models import GameSession

class GameSessionConsumer(WebsocketConsumer):

    def connect(self):
        self.accept()
        self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': 'You are now connected!'
        }))

    def disconnect(self, code):
        pass

    def receive(self, text_data=None, bytes_data=None):

        text_data_json = json.loads(text_data)
        message_type = text_data_json['type']
        session_id = text_data_json['session_id']
        game_session = GameSession.objects.filter(session_id=session_id).first()

        if message_type == 'cancel':
            game_session.active = False
            game_session.save()
            self.send(text_data=json.dumps({
                'type': 'cancel',
                'session_id': session_id
            }))
        elif message_type == 'move':
            row = text_data_json['row']
            col = text_data_json['col']
            player_type = text_data_json['player_type']
            last_move = game_session.last_move
            if last_move != player_type:
                game_session.last_move = player_type
                game_session.board_state[row][col] = player_type
                game_session.save()
                self.send(text_data=json.dumps({
                    'type': 'move',
                    'session_id': session_id,
                    'board_state': game_session.board_state
                }))
        elif message_type == 'joined' and game_session.player2 != '':
            self.send(text_data=json.dumps({
                'type': 'begin_game',
                'session_id': session_id
            }))