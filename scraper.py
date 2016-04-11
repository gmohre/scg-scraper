import json
import os
import re
from flask import Flask, render_template
app = Flask(__name__)
CARD_RE = re.compile(r'(?P<count>[0-9]+)\s(?P<name>[^\r]+)')
CARD_TEMPLATE = ''
RESOURCE_DIR = './resources'
ALL_CARDS = json.load(
        open('resources/allcards.json')
        )
 
def process_cards(deck_contents):
    maindeck, sideboard = deck_contents.split('Sideboard')
    print('split deck')
    maindeck = sorted([
        dict(
            id=idx,
            card=card[1],
            count=card[0]
            )\
        for idx, card in enumerate(CARD_RE.findall(maindeck))],
            key=lambda k: k['card'])
    print('processed main')
    sideboard = sorted([
            dict(
                id=idx,
                card=card[1],
                count=card[0]
                )\
            for idx, card in enumerate(CARD_RE.findall(sideboard))],
                key=lambda k: k['card'])
    print('processed side')
    return dict(maindeck=maindeck, sideboard=sideboard)

def process_deck(deck):
    deck = dict(contents=process_cards(deck['contents']),
        deckname=deck['deckname'])
    print(deck['contents'].keys())
    return deck
            
@app.route('/')
def hello_world():
    print('loaded cards')
    deck_names = filter(lambda x:x.endswith('txt'), os.listdir(RESOURCE_DIR))
    decks = [\
        dict(deckname=filename,
            contents=open('/'.join((RESOURCE_DIR, filename))).read())\
        for filename in deck_names]
    print('loaded decks')
    processed_decks = [process_deck(deck) for deck in decks]
    print('processed decks')
    return render_template('deck.html', decks=processed_decks, dumps=json.dumps)

if __name__ == '__main__':
    app.run()

