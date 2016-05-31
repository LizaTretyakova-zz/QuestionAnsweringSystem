import asyncio

import websockets

from src import run


@asyncio.coroutine
def query_handler(websocket, path):
    query = yield from websocket.recv()
    print("query:", query)

    answer = run(query)
#    answer = query
    yield from websocket.send(answer)
    print("send:", answer)

start_server = websockets.serve(query_handler, 'localhost', 9999)

asyncio.get_event_loop().run_until_complete(start_server)
try:
    asyncio.get_event_loop().run_forever()
except:
    pass