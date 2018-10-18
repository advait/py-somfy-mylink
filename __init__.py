import asyncio
import json

class SomfyMylink:
    def __init__(self, systemID, host, port=44100):
        self.systemID = systemID
        self.host = host
        self.port = port
        self._id = 0

    async def _send(self, method, targetID):
        """Send the given method/command to the given targetID."""
        reader, writer = await asyncio.open_connection(self.host, self.port)
        self._id += 1
        req = {
            "id": self._id,
            "method": method,
            "params": {
                "auth": self.systemID,
                "targetID": targetID,
            },
        }
        print('Writing')
        writer.write(json.dumps(req).encode())
        print('Draining')
        await writer.drain()
        print('Reading')
        ret = await reader.readuntil(b'}')
        print(ret)
        resp = json.loads(ret)
        print(resp)

    async def up(self, targetID):
        return await self._send('mylink.move.up', targetID)

    async def down(self, targetID):
        return await self._send('mylink.move.down', targetID)

    async def stop(self, targetID):
        return await self._send('mylink.move.stop', targetID)
