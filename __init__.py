import asyncio
import json

class SomfyMylink:
    def __init__(self, systemID, host, port=44100):
        self.systemID = systemID
        self.host = host
        self.port = port
        self._id = 0
        self._writer = self._reader = None

    async def _connect(self):
        if self._writer and not self._writer.is_closing():
            return
        self._reader, self._writer = await asyncio.open_connection(self.host, self.port)

    async def _send(self, method, targetID):
        """Send the given method/command to the given targetID."""
        await self._connect()
        reader, writer = (self._reader, self._writer)
        self._id += 1
        req = {
            "id": self._id,
            "method": method,
            "params": {
                "auth": self.systemID,
                "targetID": targetID,
            },
        }
        print('Writing %s', json.dumps(req))
        writer.write(json.dumps(req).encode())
        await writer.drain()
        ret = await reader.readuntil(b'}')
        resp = json.loads(ret)
        print(resp)
        return resp

    async def _up(self, targetID):
        return await self._send('mylink.move.up', targetID)

    async def _down(self, targetID):
        return await self._send('mylink.move.down', targetID)

    async def _stop(self, targetID):
        return await self._send('mylink.move.stop', targetID)

    def target(self, targetID):
        return SomfyMylinkTarget(self, targetID)


class SomfyMylinkTarget:
    def __init__(self, somfy, targetID):
        self._somfy = somfy
        self._targetID = targetID

    async def up(self):
        return await self._somfy._up(self._targetID)

    async def down(self):
        return await self._somfy._down(self._targetID)

    async def stop(self):
        return await self._somfy._stop(self._targetID)
