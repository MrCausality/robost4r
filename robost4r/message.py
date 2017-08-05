#!/usr/bin/python3
import os
import xml.etree.ElementTree as ET
import random
import SQL
import srcom
from twitch import Twitch
import globals
from dynamodb import DynamoDB

class Message:

    admin = None
    mods = None
    killCommand = False

    user = None
    text = None
    
    command = None
    parms = None
    
    output = None
    
    def __init__(self, ircMessage, admin, mods):
                  
        if ircMessage.find("PRIVMSG") != -1:

            self.admin = admin
            self.mods = mods
        
            self.user = ircMessage.split('!',1)[0][1:]          
            self.text = ircMessage.split('PRIVMSG',1)[1].split(':',1)[1]
            
            print(self.user + ": " + self.text)

        else:
            
            self.text = ircMessage
    
    def isPing(self):
        if self.text.find("PING :") != -1:
            return True
       
    def isCommand(self):
    
        if self.text.startswith('!') != -1:
        
            commandArray = self.text.split()
            
            self.command = commandArray[0][1:]
            self.parms = commandArray[1:]
            
            return True
        
        else:
        
            return False
    
    def procCommand(self):
    
        if self.command == 'getlb':
            msrcom = srcom.srcom()
            self.output = msrcom.get_lb(' '.join(map(str,self.parms)))
            return True

        elif self.command == 'title':

            global channel

            mtwitch = Twitch()
            mtwitch.title(' '.join(map(str, self.parms)))
            return True

        elif self.command == 'game':

            global channel

            mtwitch = Twitch()
            mtwitch.game(' '.join(map(str, self.parms)))
            return True

        elif self.command == 'hi':
            self.output = 'Hello ' + self.user + '!'
            return True

        elif self.command == 'bye':
            self.killCommand = True
            self.output = 'Bye, love you!'
            return True

        elif self.command == 'fact':
            mSql = SQL.SQL()

            if not self.parms:
                fact = mSql.selectAsArray("SELECT * FROM facts ORDER BY RAND()LIMIT 0,1;", None)
                self.output = fact

            elif self.parms[0] == "add":
                ddb = DynamoDB(globals.channel.user_id)

                # TODO fact text is storing with quotes, need to strip them off
                ddb.put_fact(self.parms[1], self.parms[2])

                self.command = 'fact'
                self.parms = {self.parms[1]}
                self.procCommand()

            else:
                ddb = DynamoDB(globals.channel.user_id)

                fact = ddb.get_fact(self.parms[0])
                
                if not fact:
                    self.output = "Sorry buddy, fact not found. :("

                else:
                    self.output = fact
                    
            return True
        
        else:
            return True
