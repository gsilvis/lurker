import socket

class IrcError(Exception) :
    def __init__(self, value) :
        self.value = value

    def __str__(self) :
        return repr(self.value)

class IrcListener : # interface
    def onPrivMsg(message, sender) :
        pass

    def onChanMsg(message, sender, channel) :
        pass

class IrcConnection :
    
    def __init__(self, server, port, nick="lurker", realname="Helper P. Lurkington") :
        self.server = server
        self.port = port
        self.nick = nick
        self.realname = realname

        self.initialize_listeners()

    def connect(self) :
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try : 
            self.socket.connect((self.server, self.port))
        except Error as e :
            raise IrcError(e)
        self.start_recv_loop()

    def start_recv_loop(self) :

        
