import websockets
import asyncio
import json

async def listen():
  # 2222 is the port that the client will listen on
  url = 'ws://localhost:2222'
  # Behavior for connecting w Websocket
  async with websockets.connect(url) as ws:
    # Sends 'start' str to server
    await ws.send('start')

    while True:
      # Waits for response from Server
      startMsg = await ws.recv()
      print(startMsg)
      # Sends startN and endN to Server
      print('Welcome to the Fibonacci Sequence Generator!')
      startN = input('Starting index? ')
      await ws.send(startN)
      endN = input('How many rows? ')
      await ws.send(endN)
      # Waits for result from Server, decodes it and prints each number.
      data = await ws.recv()
      fiboArray = json.loads(data.decode())
      for x in fiboArray:
        print(x)
      # Sends 'start' to trigger the above await
      await ws.send('start')

# Runs listen()
asyncio.get_event_loop().run_until_complete(listen())
