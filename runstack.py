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
        self.save()

    def add_queen(self, name, szn, dob, eth, born, state, finish):
        if dob < 1900:
            dob = datetime.datetime.now().year - dob

        newdat = {
            'name': name,
            'dob': dob,
            'eth': eth,
            'state': state,
            'state_fmr': born,
            'finish': finish,
            'sm1': '',
            'sm2': '',
            'sm3': '',
            'sm4': '',
            'sm5': '',
            'sm6': '',
        }
        self.dat[szn][name.lower().replace(' ', '')] = newdat
        self.save()

    def add_sm(self, name, sm, payload):
        for each in self.dat:
            if name in self.dat[each]:
                self.dat[each][name][self.smkeys.get(sm)] = payload
                self.save()

    def update_sm(self, old, new):
        self.smkeys[new] = self.smkeys[old]
        del self.smkeys[old]

    def update_place(self, name, season, finish):
        self.dat[season][name]['finish'] = finish
        self.save()


if __name__ == '__main__':
    dr = DragRace()
