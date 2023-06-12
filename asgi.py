from hypercorn.asyncio import serve
import asyncio
from mangum import Mangum
from webserver import app
from hypercorn.config import Config


config = Config()
config.bind = ["localhost:8080"]

handler = Mangum(app)

if __name__ == __main__:
   asyncio.run(serve(app, config))
