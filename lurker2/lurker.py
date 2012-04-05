#!/usr/bin/env python

# Copyright (C) 2012 Robbie Harwood
# Based on code from the python irclib python-irclib.sourceforge.net (GPL)

    # This file is part of lurker.

    # lurker is free software: you can redistribute it and/or modify
    # it under the terms of the GNU General Public License as published by
    # the Free Software Foundation, either version 3 of the License, or
    # (at your option) any later version.

    # lurker is distributed in the hope that it will be useful,
    # but WITHOUT ANY WARRANTY; without even the implied warranty of
    # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    # GNU General Public License for more details.

    # You should have received a copy of the GNU General Public License
    # along with lurker.  If not, see <http://www.gnu.org/licenses/>.

import do
import time
from ircbot import SingleServerIRCBot
from irclib import nm_to_n, nm_to_h, irc_lower, ip_numstr_to_quad, ip_quad_to_numstr

class TestBot(SingleServerIRCBot):    
    def __init__(self, channel, nickname, server, port=6667):
        SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
        self.channel = channel

    def on_nicknameinuse(self, c, e):
        c.nick(c.get_nickname() + "_")

    def on_join(self, c, e):
        outref = ".../lurker2/rsrc/alerts.db"
        alpha = open(outref, 'r')
        beta = ""
        nick = nm_to_n(e.source())
        for line in alpha:
            try:
                linebeta = line.split(" ", 2)
                if linebeta[1] == nick:
                    c.privmsg(nick, linebeta[0] + " told me to tell you " + linebeta[2])
                else:
                    beta = beta + line
            except:
                beta = beta
        alpha.close()
        alpha = open(outref, "w")
        alpha.write(beta)
        alpha.close()
        channel = e._target
        if channel == "#zathrassrv":
            c.privmsg(channel, nick + " joined the irc side.")
        return

    def on_welcome(self, c, e):
        c.privmsg("NickServ", "IDENTIFY ********")
        c.join(self.channel)
        return

    def on_privmsg(self, c, e):
        commandchar = "!"
        a = e.arguments()[0]
        a = a.strip()
        outref = ".../lurker2/rsrc/alerts.db"
        alpha = open(outref, 'r')
        beta = ""
        nick = nm_to_n(e.source())
        for line in alpha:
            try:
                linebeta = line.split(" ", 2)
                if linebeta[1] == nick:
                    c.privmsg(nick, linebeta[0] + " told me to tell you " + linebeta[2])
                else:
                    beta = beta + line
            except:
                beta = beta
        alpha.close()
        alpha = open(outref, "w")
        alpha.write(beta)
        alpha.close()
        
        if a == "sup" or a == "sup." or a == "sup?":
            c.privmsg(e.target(), "notmuch")

        if a[:1] == commandchar:
            a = a.lstrip(commandchar)
            if nm_to_n(e.source()) is "frozencemetery" and a is "reload":
                reload(do)
                pass
            else:
                self.do_command(e, a)
                pass
            pass
        return

    def on_kick(self, c, e):
        return
    
    def on_nick(self, c, e):
        return

    def on_part(self, c, e):
        return

    def on_topic(self, c, e):
        return

    def on_mode(self, c, e):
        return

    def on_quit(self, c, e):
        return

    def on_action(self, c, e):
        return

    def on_pubmsg(self, c, e):
        commandchar = "!"
        a = e.arguments()[0]
        a = a.strip()

        outref = ".../lurker2/rsrc/alerts.db"
        alpha = open(outref, 'r')
        beta = ""
        nick = nm_to_n(e.source())
        for line in alpha:
            try:
                linebeta = line.split(" ", 2)
                if linebeta[1] == nick:
                    c.privmsg(nick, linebeta[0] + " told me to tell you " + linebeta[2])
                else:
                    beta = beta + line
            except:
                beta = beta
        alpha.close()

        if a == "sup" or a == "sup." or a == "sup?":
            c.privmsg(e.target(), "notmuch")

        alpha = open(outref, "w")
        alpha.write(beta)
        alpha.close()

        if a[:1] == commandchar:
            a = a.lstrip(commandchar)
            self.do_command(e, a)
        return

    def do_command(self, e, cmd):
        nick = nm_to_n(e.source())
        c = self.connection
        channel = e.target()
        if channel[:1] != "#" and channel[:1] != "&" and channel[:1] != "+" and channel[:1] != "!":
            channel = "(prvt)"
        print time.strftime("[%Y-%m-%d %H:%M:%S]") + " (" + channel + ") <" + nick + "> " + cmd
        if cmd[:6] == "reload" and nick == "frozencemetery":
            z = cmd.split(" ", 1)
            if len(z) == 2:
                do.reset(z[1])
            else:
                reload(do)
        else:
            try:
                do.command(self, e, cmd, c, nick)
            except:
                pass

def main():
    import sys
    if len(sys.argv) != 4 and len(sys.argv) != 5:
        print "Syntax is: \"python lurker.py <server[:port]> <nick> <chan> [<pass>]\""
        sys.exit(1)

    s = sys.argv[1].split(":", 1)
    server = s[0]
    if len(s) == 2:
        try:
            port = int(s[1])
        except ValueError:
            print "PORT IS TOO WEIRD!"
            sys.exit(1)
    else:
        port = 6667

    nickname = sys.argv[2]
    
    channel = sys.argv[3]
    
    try:
        channel = channel + " " + sys.argv[4]
    except:
        pass
    
    
    bot = TestBot(channel, nickname, server, port)
    bot.start()

if __name__ == "__main__":
    main()
