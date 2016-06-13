from channels import Group
from .models import Token, PDF, Current

#connected to websocket.connect channel
def ws_add(message, token):
    user = Token.objects.get(token = token).user
    groupname = str(Current.objects.get(owner=user, active=1).pdf)
    print(user.username + " added to group " + groupname)
    Group(groupname).add(message.reply_channel)

#connected tp websocket.disconnect channel
def ws_disconnect(message):
    print(message.reply_channel)
    Group("all").discard(message.reply_channel)

def ws_receive(message):
    print(message)
