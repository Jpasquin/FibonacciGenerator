import websockets
import asyncio
import json

async def listen():
  url = 'ws://localhost:2222'

  async with websockets.connect(url) as ws:

    await ws.send('start')

    while True:
      startMsg = await ws.recv()
      print(startMsg)
      print('Welcome to the Fibonacci Sequence Generator!')
      startN = input('Starting index? ')
      await ws.send(startN)
      endN = input('How many rows? ')
      await ws.send(endN)

      data = await ws.recv()
      fiboArray = json.loads(data.decode())
      for x in fiboArray:
        print(x)

      await ws.send('start')

        
asyncio.get_event_loop().run_until_complete(listen())