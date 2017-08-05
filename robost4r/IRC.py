import socket
from message import Message

class IRC:

    def __init__(self, server, port, channel, admin, botNickname, botPassword):
    
        self.admin = admin
        self.channel = channel
    
        self.ircSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.ircSocket.connect((server, port))

        self.ircSocket.send(bytes("USER " + botNickname + " " + botNickname + " " + botNickname + " " + botNickname + "\n", "UTF-8"))
        self.ircSocket.send(bytes("PASS " + botPassword + "\n", "UTF-8"))
        self.ircSocket.send(bytes("NICK " + botNickname + "\n", "UTF-8"))
        self.ircSocket.send(bytes("JOIN " + self.channel + "\n", "UTF-8"))
        
        irc_message = ""
        
        while irc_message.find("End of /NAMES list") == -1:
            irc_message = self.ircSocket.recv(2048).decode("UTF-8")
            irc_message = irc_message.strip('\n\r')
            print(irc_message)
            
        self.ircSocket.send(bytes("CAP REQ :twitch.tv/commands" + "\n", "UTF-8"))
        
        while irc_message.find("ACK :twitch.tv/commands") == -1:
            irc_message = self.ircSocket.recv(2048).decode("UTF-8")
            irc_message = irc_message.strip('\n\r')
            print(irc_message)
            
        self.ircSocket.send(bytes("PRIVMSG {} :{}\r\n".format(self.channel, ".mods").encode()))
        
        while irc_message.find("moderators of this room are:") == -1:
            irc_message = self.ircSocket.recv(2048).decode("UTF-8")
            irc_message = irc_message.strip('\n\r')
            print(irc_message)
            
            self.mods = irc_message.split(": ")[1].split(", ")
        
        self.mods.append("st4rsurfer")
            
    def ping(self): # respond to server Pings.
        self.ircSocket.send(bytes("PONG :pingis\n", "UTF-8"))

    def send_msg(self, msg): # sends messages to the target.
        self.ircSocket.send(bytes("PRIVMSG {} :{}\r\n".format(self.channel, msg).encode()))

    def main(self):

        while 1:
            
            msg = Message(self.ircSocket.recv(2048).decode("UTF-8").strip('\n\r'), self.admin, self.mods)
            
            if msg.text is not None:

                if msg.isPing():
                    self.ping()
                    
                if msg.isCommand():
                    if msg.procCommand():
                        if msg.output is not None:
                            self.send_msg(msg.output)
                        if msg.killCommand:
                            print(":shutting down")
                            self.ircSocket.send(bytes("QUIT \n", "UTF-8"))
                            return
                    else:
                        print(":command failed")
                        self.ircSocket.send(bytes("QUIT \n", "UTF-8"))
                        return