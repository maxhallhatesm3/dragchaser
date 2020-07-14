import json
import requests

from datetime import datetime


def main():
    with open('db.json', 'r') as fil:
        dat = json.load(fil)

    for season in dat:
        for queen in dat[season]:
            instagram_fol, instagram_lik = get_insta(dat[season][queen]['sm1'])
            ddump = {
                'name': queen,
                'ts': datetime.today().strftime('%Y-%m-%d'),
                'sm1': instagram_fol,
                'sm2': get_twitter(dat[season][queen]['sm2']),
                'sm3': get_facebook(dat[season][queen]['sm3']),
                'sm4': 0,
                'sm5': 0,
                'sm6': instagram_lik
            }
            with open('queries.json', 'a') as wfil:
                json.dump(ddump, wfil)
                wfil.write('\n')


def get_insta(username):
    #username = 'jaidaehall'
    r = requests.get('https://www.picuki.com/profile/%s' % username)
    chop = r.text.split('<span data-followers="')[1]

    with open('jaida', 'w') as ofil:
        ofil.write(r.text)

    dump = ''

    for each in chop:
        if each == '"':
            break
        else:
            dump += each


    count = int(dump)

    likes = []
    for each in r.text.split('<span class="flaticon-favorite-heart-button"></span>'):
        ct = ''

        for char in each:
            if char in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']:
                ct += char
            else:
                if char == 'k':
                    ct = int(ct) * 1000
                else:
                    if len(ct) > 0:
                        ct = int(ct)
                break
        if isinstance(ct, int):
            likes.append(ct)
        ct = ''

    lavg = sum(likes) / len(likes)

    return count, lavg


def get_facebook(username):
    return 0


def get_twitter(username):
    return 0


if __name__ == '__main__':
    main()
