from channels.routing import route
from slides.consumers import ws_add, ws_disconnect, ws_receive

channel_routing = [
    #<token> regex that matches token ie all strings
    route("websocket.connect", ws_add, path=r'^/user/(?P<token>[0-9])/$'),
    route("websocket.disconnect", ws_disconnect),
    route("websocket.receive", ws_receive),
]
