"""
Simple Facebook Echo bot: Respond with exactly what it receives
Standalone version
"""

import sys, json, traceback, requests
import textwrap
import time
import random

npc_server = 'http://127.0.0.1:10000/SHIHbot/'

def processIncoming(message):
    data = {
        "q": message,
        "from": 'test'
    }
    try:
        r = requests.post(npc_server, data=data)
    except ConnectionError:
        return 'I\'m away from keyboard, will come back in a moment, your message {}'.format(message)

    if r.status_code != requests.codes.ok:
        return 'I\'m away from keyboard, will come back in a moment'
    if r.text == '':
        return 'I don\'t understand your question: {}, try a different one?'.format(message)
    return r.text


def send_message(token, user_id, text):
    """Send the message text to recipient with id recipient.
    """
    new_sentences = textwrap.fill(text, 300).split('\n')
    for s in new_sentences:
        time.sleep(random.randint(0, 2))
        r = requests.post("https://graph.facebook.com/v2.6/me/messages",
                          params={"access_token": token},
                          data=json.dumps({
                              "recipient": {"id": user_id},
                              "message": {"text": s}
                          }),
                          headers={'Content-type': 'application/json'})
        if r.status_code != requests.codes.ok:
            print r.text


def readBatchMessages(path):
    with open(path, 'r') as qs:
        questions = map(lambda q: q.strip(), qs.readlines())
    return questions


# Allows running with simple `python <filename> <port>`
if __name__ == '__main__':
    qs = readBatchMessages('nyQ100.test.txt')
    results = map(lambda q: processIncoming(q), qs)
    for i, (q, r) in enumerate(zip(qs, results)):
        print 'question {}: {}'.format(i, q)
        print 'answer {}: {}'.format(i, r.encode('utf-8'))
        print ''
