somfy-mylink
============

TCP API bindings for the [Somfy MyLink Synergy API](https://www.somfysystems.com/somfy-synergy-api).

## Usage

```python
from somfy_mylink import SomfyMyLink

somfy = SomfyMyLink('yoursystemid', '192.168.86.31')
cover = somfy.target('CC104FA2.1')

# Async open the shade
await cover.up()

# Async close the shade
await cover.down()

# Async stop the shade motion
await cover.stop()
```

