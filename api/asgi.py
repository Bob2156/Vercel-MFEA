from hypercorn.asyncio import serve
import asyncio
from mangum import Mangum
from webserver import app
from hypercorn.config import Config
from a2wsgi import ASGIMiddleware

config = Config()
config.bind = ["localhost:8080"]

# vercel only supports wsgi so a2wsgi is needed here
# handler = Mangum(app)
handler = ASGIMiddleware(app)

if __name__ == __main__:
   asyncio.run(serve(app, config))
