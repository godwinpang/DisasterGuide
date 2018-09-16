import asyncio
import websockets

async def get_disaster(websocket, path):
    while(True):
        disaster = await websocket.recv()
        print(disaster)

server = websockets.serve(get_disaster, 'localhost', 8085)

asyncio.get_event_loop().run_until_complete(server)
asyncio.get_event_loop().run_forever()
