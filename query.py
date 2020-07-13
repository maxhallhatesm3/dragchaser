import json
import requests

from datetime import datetime


def main():
    with open('db.json', 'r') as fil:
        dat = json.load(fil)

    for season in dat:
        for queen in dat[season]:
            ddump = {
                'name': queen,
                'ts': datetime.today().strftime('%Y-%m-%d'),
                'sm1': get_insta(dat[season][queen]['sm1']),
                'sm2': get_twitter(dat[season][queen]['sm2']),
                'sm3': get_facebook(dat[season][queen]['sm3']),
                'sm4': 0,
                'sm5': 0,
                'sm6': 0
            }
            with open('queries.json', 'a') as wfil:
                json.dump(ddump, wfil)
                wfil.write('\n')


def get_insta(username):
    #username = 'jaidaehall'
    r = requests.get('https://www.instagram.com/%s/?hl=en' % username)
    chop = r.text.split('"edge_followed_by":')[1]

    dump = ''

    for each in chop:
        dump += each
        if each != '}':
            continue
        else:
            break

    count = json.loads(dump).get('count', None)

    return count


def get_facebook(username):
    return 0


def get_twitter(username):
    return 0


if __name__ == '__main__':
    main()
