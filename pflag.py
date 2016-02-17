#!/usr/bin/env python

import urllib2, time, json, ConfigParser
from decimal import *

FLAG_COLOUR_NONE = 0,           # Not used for actual flags, only for some query functions
FLAG_COLOUR_GREEN = 1,          # End of danger zone, or race started
FLAG_COLOUR_BLUE = 2,           # Faster car wants to overtake the participant
FLAG_COLOUR_WHITE = 3,          # Approaching a slow car
FLAG_COLOUR_YELLOW = 4,         # Danger on the racing surface itself
FLAG_COLOUR_DOUBLE_YELLOW = 5,  # Danger that wholly or partly blocks the racing surface
FLAG_COLOUR_BLACK = 6,          # Participant disqualified
FLAG_COLOUR_CHEQUERED = 7,      # Chequered flag


#
# Parses the configuration file
#
def loadConfig():
        print("Reading configuration...")
        configini = ConfigParser.ConfigParser()
        configini.read('./apiconfig.ini')

        config = {}
        for section in configini.sections():
            for option in configini.options(section):
                config[section.lower()+':'+option.lower()] = configini.get(section, option)
        
        config['logging:verbose'] = config['logging:verbose'].lower() in ('yes', 'y', 'true', 't', '1')

        if(config['logging:verbose']):
                print("Loaded configuration:")
                for option in config:
                        print("%s = %s") % (option,config[option])

                
        return config

#
# Gets the current flag from the API
#
def getFlag():
        global config, crest_api_url

        flags_url=crest_api_url+"?flags=true"

        if (config['logging:verbose']):
                print("Requesting "+flags_url)
                
        response = urllib2.urlopen(flags_url)
        flag_json_raw = response.read()
        flag_json = json.loads(flag_json_raw)

        if (config['logging:verbose']):
                print flag_json

        return flag_json['flags']['mHighestFlagColour']


# Load the config
config = loadConfig()

# Assemble the URL
crest_api_url = "%s://%s:%s%s" % (config['api:proto'], config['api:host'], config['api:port'], config['api:path'])

# Convert miliseconds to seconds
config['general:delay'] = float(config['general:delay'])/1000

while True:
        flag = getFlag()

        if   flag == 0:
                print "No Flag"
        elif flag == 1:
                print "End of danger zone, or race started"
        elif flag == 2:
                print "Faster car wants to overtake the participant"
        elif flag == 3:
                print "Approaching a slow car"
        elif flag == 4:
                print "Danger on the racing surface itself"
        elif flag == 5:
                print "Danger that wholly or partly blocks the racing surface"
        else:
                print "Participant disqualified"

        time.sleep(config['general:delay'])
