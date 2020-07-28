import os
import json
import time
import datetime


class DragRace:
    def __init__(self):
        with open('db2.json', 'r') as fil:
            self.dat = json.load(fil)

        self.smkeys = {
            'instagram': 'sm1',
            'twitter': 'sm2',
            'facebook': 'sm3',
            'tumblrtag': 'sm4',
            'twittertag': 'sm5',
            'instagram_likes_avg': 'sm6',
        }

    def save(self):
        with open('db2.json', 'w') as fil:
            json.dump(self.dat, fil, sort_keys=True, indent=6)

    def load(self):
        with open('db2.json', 'r') as fil:
            self.dat = json.load(fil)

    def add_queen(self, name, szn, finish, dob, eth, born, state):
        if dob < 1900:
            dob = datetime.datetime.now().year - dob

        newdat = {
            "name": name,
            "dob": dob,
            "eth": eth,
            "finish": [finish],
            "seasons": [szn],
            "sm1": "",
            "sm2": "",
            "sm3": "",
            "sm4": "",
            "sm5": "",
            "sm6": "",
            "state": state,
            "state_fmr": born
        }

        if name.lower().replace(' ', '') in self.dat:
            print('exists.......................')
            return

        self.dat[name.lower().replace(' ', '')] = newdat
        self.save()


if __name__ == '__main__':
    dr = DragRace()
