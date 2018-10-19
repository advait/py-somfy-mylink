import asyncio
import json
import logging

class SomfyMyLink:
    """Wraps access to a Somfy MyLink Hub via the Somfy Synergy API."""

    def __init__(self, system_id, host, port=44100):
        self.system_id = system_id
        self.host = host
        self.port = port
        self._id = 0
        self._writer = self._reader = None

    async def _connect(self):
        if self._writer and not self._writer.transport.is_closing():
            return
        self._reader, self._writer = await asyncio.open_connection(self.host, self.port)

    async def _send(self, method, target_id):
        """Send the given method/command to the given target_id."""
        await self._connect()
        reader, writer = (self._reader, self._writer)
        self._id += 1
        req = {
            "id": self._id,
            "method": method,
            "params": {
                "auth": self.system_id,
                "targetID": target_id,
            },
        }
        reqs = json.dumps(req)
        logging.debug('Sending request: %s' % reqs)
        writer.write(reqs.encode())
        await writer.drain()
        resps = await reader.readuntil(b'}')
        logging.debug('Received response: %s' % resps)
        try:
            resp = json.loads(resps)
        except json.decoder.JSONDecodeError as e:
            logging.error('Could not understand response: %s' % resps, exc_info=e)
            raise e
        return resp

    async def _up(self, target_id):
        return await self._send('mylink.move.up', target_id)

    async def _down(self, target_id):
        return await self._send('mylink.move.down', target_id)

    async def _stop(self, target_id):
        return await self._send('mylink.move.stop', target_id)

    def target(self, target_id):
        """Returns a target that can be used to issue commands."""
        return SomfyMyLinkTarget(self, target_id)


class SomfyMyLinkTarget:
    """Represents a single Somfy MyLink device/target."""
    def __init__(self, somfy, target_id):
        self._somfy = somfy
        self._target_id = target_id

    async def up(self):
        """Open the shade."""
        return await self._somfy._up(self._target_id)

    async def down(self):
        """Close the shade."""
        return await self._somfy._down(self._target_id)

    async def stop(self):
        """Stop the shade."""
        return await self._somfy._stop(self._target_id)
