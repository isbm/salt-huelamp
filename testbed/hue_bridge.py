# -*- coding: utf-8 -*-
'''
Example of a simple Salt Proxy Minion for the Philips Hue bridge
'''

# Import python libs
import logging
from time import sleep
import requests

#Morse code table:
MORSE_ALPHABET = {
        'A': '.-',     'B': '-...',   'C': '-.-.', 
        'D': '-..',    'E': '.',      'F': '..-.',
        'G': '--.',    'H': '....',   'I': '..',
        'J': '.---',   'K': '-.-',    'L': '.-..',
        'M': '--',     'N': '-.',     'O': '---',
        'P': '.--.',   'Q': '--.-',   'R': '.-.',
     	'S': '...',    'T': '-',      'U': '..-',
        'V': '...-',   'W': '.--',    'X': '-..-',
        'Y': '-.--',   'Z': '--..',
        
        '0': '-----',  '1': '.----',  '2': '..---',
        '3': '...--',  '4': '....-',  '5': '.....',
        '6': '-....',  '7': '--...',  '8': '---..',
        '9': '----.',
        
        ' ': '   ',
        }


#Define state JSON content for typical actions:

ON = {"on":True, "transitiontime": 0}
OFF = {"on":False, "transitiontime": 0}

ALERT = {"alert": "select"}
LONG_ALERT = {"alert": "lselect"}

DEMO_ON = {"sat": 254, "bri": 254, "effect": "colorloop"}
DEMO_OFF = {"effect":"none"}

BRIGHTER = {"bri_inc": 25}
DIMMER = {"bri_inc": -25}

DIM = {"on": True, "bri": 0, "transitiontime": 0}

WHITE = {"on": True, "sat": 0, "bri": 254, "transitiontime": 0}
RED = {"on": True, "hue": 0, "sat": 254, "bri": 254, "transitiontime": 0}
GREEN = {"on": True, "hue": 25500, "sat": 254, "bri": 254, "transitiontime": 0}
ORANGE = {"on": True, "hue": 12000, "sat": 254, "bri": 254, "transitiontime": 0}
BLUE = {"on": True, "hue": 40000, "sat": 254, "bri": 254, "transitiontime": 0}


# This must be present or the Salt loader won't load this module
__proxyenabled__ = ['hue_bridge']

# Want logging!
log = logging.getLogger(__file__)

CONFIG = {}

#Salt-specifc stuff:

def init(opts):
    '''
    Every proxy module needs an 'init', though you can
    just put a 'pass' here if it doesn't need to do anything.
    '''
    log.debug('rest_sample proxy init() called...')
    CONFIG['url'] = "http://" + opts['proxy']['bridge_url'] + "/api/" + opts['proxy']['api_user']
    

def ping():
    return change("3", BRIGHTER)


def shutdown(opts):
    '''
    For this proxy shutdown is a no-op
    '''
    log.debug('rest_sample proxy shutdown() called...')
    
#Hue-specific stuff:



def change(lamp_id="1", state="on"):
    """ """
    r = requests.put(CONFIG['url']+"/lights/" + lamp_id + "/state", json=state)
    return r.content

def init_hue(light_id):
    """Set all light to on/white"""
    change(light_id, WHITE)    

def alternate():
    """ """
    init_hue("1")
    init_hue("2")
    while True:
        change("1", ON)
        change("2", OFF)
        sleep(1)
        change("1", OFF)
        change("2", ON)
        sleep(1)        

def colors():
    """ """
    init_hue("1")
    init_hue("2")
    while True:
        for state in [RED, ORANGE, GREEN]:
            for id in ["1","2"]:
                change(id, state)
            sleep(1)

def ascii_to_morse(text):
    """ """
    code = ""
    for letter in text:
        code += MORSE_ALPHABET[letter.upper()] + " "
    print code
    return code

def morse(code):
    """ """
    change("1", OFF)
    change("2", OFF)
    sleep(5)
    for letter in code:
        if letter == "-":
            change("1", RED)
            sleep(2)
            change("1", OFF)
            sleep(0.5)
        elif letter == ".":
            change("1", GREEN)
            sleep(0.5)
            change("1", OFF)
            sleep(0.5)
        elif letter == " ":
            sleep(1)
            
def colorwheel():
    """ """
    init_hue("1")
    init_hue("2")
    change("1",DEMO_ON)
    change("2",DEMO_ON)
    sleep(60)
    change("1",OFF)
    change("2",OFF)

def increment():
    """ """
    change("1", OFF)
    change("2", OFF)
    change("1", DIM)
    change("1", {"hue": 40000, "sat": 254})
    for x in range(1,10):
        change("1", BRIGHTER)
        sleep(0.5)

def alert():
    """ """
    return change("3", LONG_ALERT)
