import os
import sys
import json
import time
import requests

from datetime import datetime


def main():
    with open('db2.json', 'r') as fil:
        dat = json.load(fil)

    for queen in dat:
        try:
            instagram_fol, instagram_lik = get_insta(dat[queen]['sm1'])
        except:
            err_log('instagram global fault: %s' % queen)
        try:
            facebook_impr = get_facebook(dat[queen]['sm3'])
        except:
            err_log('facebook global fault: %s' % queen)
        try:
            twitter_fol, twitter_twts = get_twitter(dat[queen]['sm2'])
        except:
            err_log('twitter global fault: %s' % queen)

        extract = dat[queen]

        extract.update(
            {
                '_ts': datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
                'insta_f': instagram_fol,
                'twitr_f': twitter_fol,
                'faceb_f': facebook_impr,
                'sm4': 0,
                'twitr_t': twitter_twts,
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

    if not username:
        err_log('username null')
        return 0, 0
    if len(username) < 2:
        err_log('username len fail: %s' % username)
        return 0, 0

    try:
        r = requests.get('https://www.picuki.com/profile/%s' % username)
    except:
        err_log('request fail, https://www.picuki.com/profile/%s' % username)
        return 0, 0
    try:
        chop = r.text.split('<span data-followers="')[1]
    except:
        filen = os.path.join('logs', str(int(time.time())) + '.err')
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
    if len(likes) > 0:
        lavg = sum(likes) / len(likes)
    else:
        err_log('zero div fail, ig likes, https://www.picuki.com/profile/%s' % username)
        return 0, 0

    return count, lavg


def get_facebook(username):
    if not username:
        err_log('username null: %s' % username)
        return 0
    if len(username) < 2:
        err_log('username len fail: %s' % username)
        return 0
    try:
        r = requests.get('https://www.facebook.com/%s' % username)
    except:
        err_log('request fail, https://www.facebook.com/%s' % username)
        return 0

    try:
        rough = r.text.split('people like this')[0].split('<div>')[-1]
        likes = int(rough.strip().replace(',', ''))
    except:
        filen = os.path.join('logs', str(int(time.time())) + '.err')
        err_log('chop fail: %s;  %s' % (username, filen))
        with open(filen, 'w') as errr:
            errr.write(r.text)
        return 0

    try:
        rough = r.text.split('people follow this')[0].split('<div>')[-1]
        follows = int(rough.strip().replace(',', ''))
    except:
        filen = os.path.join('logs', str(int(time.time())) + '.err')
        err_log('chop fail: %s;  %s' % (username, filen))
        with open(filen, 'w') as errr:
            errr.write(r.text)
        return 0

    return likes + follows


def get_twitter(username):
    if not username:
        err_log('username null: %s' % username)
        return 0, 0
    if len(username) < 2:
        err_log('username len fail: %s' % username)
        return 0, 0
    try:
        r = requests.get('https://tweettunnel.com/%s' % username)
    except:
        err_log('request fail, https://tweettunnel.com/%s' % username)
        return 0, 0

    try:
        follows = r.text.split('Following</span> &nbsp;&nbsp;')[1].split('<span')[0]
        tweets = r.text.split('Followers</span> &nbsp;&nbsp;')[1].split('<span')[0]
        follows = follows.strip().replace(',', '')
        tweets = tweets.strip().replace(',', '')
    except:
        filen = os.path.join('logs', str(int(time.time())) + '.err')
        err_log('chop fail: %s;  %s' % (username, filen))
        with open(filen, 'w') as errr:
            errr.write(r.text)
        return 0, 0

    return follows, tweets


def err_log(string):
    fn = '%s.log' % datetime.now().strftime('%Y-%m-%d-%H')
    erlog = os.path.join('logs', fn)
    with open(erlog, 'a') as log:
        log.write('%s\tERR: %s' % (datetime.now().strftime('%Y-%m-%dT%H:%M:%S'), string))
        log.write('\n')
    sys.stdout.write('E')
    sys.stdout.flush()


if __name__ == '__main__':
    main()
