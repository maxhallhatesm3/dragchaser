import sys
import json
import time
import requests

from datetime import datetime


def main():
    with open('db2.json', 'r') as fil:
        dat = json.load(fil)

    for queen in dat:
        instagram_fol, instagram_lik = get_insta(dat[queen]['sm1'])

        extract = dat[queen]

        extract.update(
            {
                '_ts': datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
                'insta_f': instagram_fol,
                'twitr_f': get_twitter(dat[queen]['sm2']),
                'faceb_f': get_facebook(dat[queen]['sm3']),
                'sm4': 0,
                'sm5': 0,
                'insta_l': instagram_lik
            }
        )

        with open('queries.json', 'a') as wfil:
            json.dump(extract, wfil, sort_keys=True)
            wfil.write('\n')
        sys.stdout.write('∙')
        sys.stdout.flush()
    sys.stdout.write('\n')
    sys.stdout.flush()


def get_insta(username):
    #username = 'jaidaehall'
    try:
        r = requests.get('https://www.picuki.com/profile/%s' % username)
    except:
        err_log('request fail, https://www.picuki.com/profile/%s' % username)
        return 0, 0
    try:
        chop = r.text.split('<span data-followers="')[1]
    except:
        filen = str(int(time.time())) + '.err'
        err_log('chop fail: %s;  %s' % (username, filen))
        with open(filen, 'w') as errr:
            errr.write(r.text)
        return 0, 0

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


def err_log(str):
    with open('err.log', 'a') as log:
        log.write('%s\tERR: %s' % (time.time(), str))
        log.write('\n')
    sys.stdout.write('E')
    sys.stdout.flush()


if __name__ == '__main__':
    main()
