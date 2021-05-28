import asyncio
import websockets
import time
import ssl

#https://github.com/binance/binance-spot-api-docs/blob/master/web-socket-streams.md#general-wss-information
binanceWSS = "wss://stream.binance.com:9443/ws"

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)

async def wsClient():
    async with websockets.connect(
        binanceWSS, ssl=ssl_context
    ) as websocket:
        time.sleep(1)
        
        
        
        msg = await websocket.recv()
        print(f"< {msg}")        
    
asyncio.get_event_loop().run_until_complete(wsClient())