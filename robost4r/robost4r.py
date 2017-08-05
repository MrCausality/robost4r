import globals
import IRC


#print(globals.channel)

IrcClient = IRC.IRC("irc.chat.twitch.tv",
                    6667,
                    "#" + globals.channel.user_name,
                    globals.channel.user_name,
                    "robost4r",
                    'oauth:' + globals.channel.secret)

IrcClient.main()
