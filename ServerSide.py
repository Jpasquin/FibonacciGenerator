import websockets
import asyncio
import json

# Define port location
PORT = 2222
numbers = []

print('Started server and listening on port ' + str(PORT))

async def fibo(websocket, path):
  print('Client connected')
  try:
    # clientRequest is response sent from the client
    async for clientRequest in websocket:
      # When the response is 'start', send back ready for input str
      if str(clientRequest) == 'start':
        print('Recieved request from client: ' + clientRequest)
        await websocket.send('OK, ready for user input')

      # When response is not 'start', assume values for calculaiton are being recieved
      else:
        print('Recieved request from client: ' + clientRequest)
        # Adds recieved value to numbers Array
        numbers.append(clientRequest)
        # When 2 slots are filled AKA array length is 2, then calculate and send back result
        if len(numbers) == 2:
          # First fib() calculation is to find A & B
          fiboToAB = list(fib(0, 1, int(numbers[0])+1))
          newA = fiboToAB[int(numbers[0])-1]
          newB = fiboToAB[int(numbers[0])]
          # Second fib() is proper A & B and rows requested by user.
          result = list(fib(int(newA), int(newB), int(numbers[1])))
          print(result)
          del numbers[1]
          del numbers[0]
          # Converts to JSON obj and encodes so it can be sent to client.
          data = json.dumps(result)
          await websocket.send(data.encode())

  # Prints websocket exceptions
  except websockets.exceptions.ConnectionClosed as e:
    print('Client disconnected: ' + str(e))
# Fibonacci calc method
def fib(a, b, n):
    for _ in range(n):
        yield a
        a, b = b, a + b

start_server = websockets.serve(fibo, 'localhost', PORT)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()