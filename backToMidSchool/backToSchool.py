#!/usr/bin/env python3

import socket
import sys
import re

try:
	from .config import (PASSWORD,
			    NICKNAME,
			    DOMAIN,
			    SERVER,
			    CHANNEL,
			    REAL_NAME,
			    QUITMSG,
			    PONG)
except:
	from config import (PASSWORD,
			    NICKNAME,
			    DOMAIN,
			    SERVER,
			    CHANNEL,
			    REAL_NAME,
			    QUITMSG,
			    PONG)

from math import sqrt

class IRCMessages:
	def __init__(self):
		self.PASS = PASSWORD
		self.NICK = NICKNAME
		self.USER = (self.NICK, DOMAIN, SERVER, REAL_NAME)
		self.SERVER = SERVER
		self.CHANNEL = CHANNEL
		self.QUIT = QUITMSG
		self.PONG = PONG
		self.MESSAGE = "!ep1"
		self.ANSWER = " -rep"
		self.CALC = float(0.0)

	@classmethod
	def connection(self):
		irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
		irc.connect((SERVER, 6667))
		irc.send(bytes("USER " + NICKNAME + " " + NICKNAME + " " + NICKNAME + " " + SERVER + "\n", "UTF-8"))
		irc.send(bytes("NICK " + NICKNAME + "\n", "UTF-8"))
		print("connecting to:" + SERVER)
		return irc

	def disconnection(self, irc):
		irc.shutdown(socket.SHUT_RDWR)
		irc.close()
		print("Disconnected from: " + SERVER)
		return

	def joinChannel(self, irc, CHANNEL):
		irc.send(bytes("JOIN " + CHANNEL + "\n", "UTF-8"))
		ircmsg = ""
		while (ircmsg.find("Narrqtor +x") == -1):
			ircmsg = irc.recv(2048).decode("UTF-8")
			ircmsg = ircmsg.strip('\n\r')
			print(ircmsg)

	def ping(self, irc):
		irc.send(bytes(PONG + " received ping\n", "UTF-8"))
		return

	def sendMsg(self, irc, CHANNEL):
		target = "candy" 
		irc.send(bytes("PRIVMSG " + target + " :" + self.MESSAGE + "\n", "UTF-8"))
		return
		
	def sendAnsw(self, irc, CHANNEL, CALC):
		target = "candy"
		irc.send(bytes("PRIVMSG " + target + " :" + self.MESSAGE + self.ANSWER + " " + CALC + "\n\r", "UTF-8"))
		print(self.MESSAGE + self.ANSWER + " "  + CALC)
		return

	def calculation(self, candysMessage):
		num1 = candysMessage.split('/',1)[0]
		num2 = candysMessage.split('/',1)[1][1:]
		res = sqrt(float(num1)) * int(num2)
		resstr = "{:.2f}".format(res)
		return str(resstr)

	def main(self):
		irc = IRCMessages().connection()
		IRCMessages().joinChannel(irc, CHANNEL)
		while(1):
			IRCMessages().sendMsg(irc, CHANNEL)
			ircmsg = irc.recv(2048).decode("UTF-8")
			ircmsg = ircmsg.strip('\n\r')
			print(ircmsg)
			if ircmsg.find("PRIVMSG") != -1:
				name = ircmsg.split('!',1)[0][1:]
				message = ircmsg.split('PRIVMSG',1)[1].split(':',1)[1]
				self.CALC = IRCMessages().calculation(message)
				IRCMessages().sendAnsw(irc, CHANNEL, self.CALC)
				ircmsg = irc.recv(2048).decode("UTF-8")
				ircmsg = ircmsg.strip('\n\r')
				print(ircmsg)
				IRCMessages().disconnection(irc)
				return

if __name__ == '__main__':
	IRCMessages().main()
