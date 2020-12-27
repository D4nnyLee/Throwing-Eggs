import os
import struct

from transitions.extensions import GraphMachine
from Game.utils import send_push_message, send_reply_message

class GameMachine(GraphMachine):
    def __init__(self, user_id, **machine_configs):
        self.machine = GraphMachine(model = self, **machine_configs)
        self.user_id = user_id
        self.ans = 0
        self.remain_times = 0
        self.remain_eggs = 0

    def help(self, event):
        return not (self.get_info(event) or self.query(event) or self.answer(event))

    def get_info(self, event): # "#"
        param = event.message.text.split()
        return len(param) == 1 and param[0] == '#'

    def query(self, event): # "? xxx"
        param = event.message.text.split()
        return len(param) == 2 and param[0] == '?' and param[1].isdigit()

    def answer(self, event): # "! xxx"
        param = event.message.text.split()
        return len(param) == 2 and param[0] == '!' and param[1].isdigit()

    def on_enter_reset(self, event):
        self.forward()

    def on_exit_reset(self):
        send_push_message(
                user_id = self.user_id,
                text = '''Now you have 3 eggs, I want to know the
MAX number X such that the egg won't break
if I throw it from Xth floor of the building.

The range for X is 0 ~ 1000.

Note that if the egg is not broken,
it will be thrown in the next trial.

Please help me to find the number X within at most 30 trials.
You only have 1 chance to check the answer.

Type "help" for more information.

(It's always possible to find X in such restriction, 
you can try to figure out how to do that. ^^)'''
        )

        self.remain_times = 30
        self.remain_eggs = 3
        self.ans = struct.unpack('>Q', os.urandom(8))[0] % 1001 # answer is 0 ~ 1000

    def on_enter_usage(self, event):
        send_reply_message(
                reply_token = event.reply_token,
                text = '''Usage:
    # : Get the information of remain throwing times and eggs.
    ? N : Query the result of throwing egg from Nth floor.
    ! N : Check whether N is the answer or not and restart game.
    None of above : Print this message.'''
        )

        self.forward()

    def on_enter_info(self, event):
        status = f'''Remain:
    Eggs:  {self.remain_eggs}
    Times: {self.remain_times}'''

        send_reply_message(
            reply_token = event.reply_token,
            text = status
        )

        self.forward()

    def on_enter_reply(self, event):
        if self.remain_eggs == 0:
            send_reply_message(
                reply_token = event.reply_token,
                text = 'No remaining egg for you to try.'
            )
        elif self.remain_times == 0:
            send_reply_message(
                reply_token = event.reply_token,
                text = 'You try too many times.'
            )
        else:
            param = event.message.text.split()

            broken = int(param[1]) > self.ans
            if broken:
                self.remain_eggs -= 1
            self.remain_times -= 1

            send_reply_message(
                reply_token = event.reply_token,
                text = 'Broken' if broken else 'Safe'
            )

        self.forward()

    def on_enter_judge(self, event):
        param = event.message.text.split()

        send_reply_message(
            reply_token = event.reply_token,
            text = 'Correct!' if int(param[1]) == self.ans else 'Wrong answer :('
        )

        self.forward(event)
