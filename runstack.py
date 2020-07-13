import os
import json
import time
import datetime


class DragRace:
    def __init__(self):
        with open('db.json', 'r') as fil:
            self.dat = json.load(fil)

        self.smkeys = {
            'instagram': 'sm1',
            'twitter': 'sm2',
            'facebook': 'sm3',
            'tumblrtag': 'sm4',
            'twittertag': 'sm5',
            'sm6': 'sm6',
        }

    def save(self):
        with open('db.json', 'w') as fil:
            json.dump(self.dat, fil, sort_keys=True, indent=6)

    def add_season(self, number, allstars=False):
        if allstars:
            szn = 'AS%d' % number
        else:
            szn = 'DR%d' % number

        self.dat[szn] = {}

    def add_queen(self, name, szn, dob, eth, state, finish):
        if dob < 1900:
            dob = datetime.datetime.now().year - dob

        newdat = {
            'name': name,
            'dob': dob,
            'eth': eth,
            'state': state,
            'finish': finish,
            'sm1': '',
            'sm2': '',
            'sm3': '',
            'sm4': '',
            'sm5': '',
            'sm6': '',
        }
        self.dat[szn][name.lower().replace(' ', '')] = newdat

    def add_sm(self, name, sm, payload):
        dat[szn][name][self.smkeys.get(sm)] = payload

    def update_sm(self, old, new):
        self.smkeys[new] = self.smkeys[old]
        del self.smkeys[old]
