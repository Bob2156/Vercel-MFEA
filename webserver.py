import os
import sys
import asyncio
import aiohttp
import io

from quart import Quart

sys.path.insert(1, ".")

import quart.flask_patch
from flask_discord_interactions import DiscordInteractions, Message, Embed, embed, Autocomplete, Member


app = Quart(__name__)
discord = DiscordInteractions(app)
app.jeyybase_url = "https://api.jeyy.xyz/v2"
app.config["DISCORD_CLIENT_ID"] = os.environ["DISCORD_CLIENT_ID"]
app.config["DISCORD_PUBLIC_KEY"] = os.environ["DISCORD_PUBLIC_KEY"]
app.config["DISCORD_CLIENT_SECRET"] = os.environ["DISCORD_CLIENT_SECRET"]
app.imagetypes = []

app.jeyyheader = {"Authorization": f"Bearer {os.environ['JEYY_API']}"}

app.isgimg_started = False

@app.before_first_request
async def my_func():
  discord.update_commands()
  asyncio.create_task(getimagelist())


async def getimagelist():
    app.isgimg_started = True
    while True:
        print("Executed")
        async with aiohttp.ClientSession(headers=app.jeyyheader) as sus:
             async with sus.get(f"{app.jeyybase_url + '/general/endpoints'}") as resp:
                rawdat = await resp.json()
                app.imagetypes = [l[10:] for l in rawdat if "/v2/image" in l]

        print("Cached")
        await asyncio.sleep(5)

@discord.command(annotations={"imagefilter": "The Image Filter", "member": "Member profile pic"})
async def generateimage(ctx, imagefilter: Autocomplete(str), member: Member = None):
    "Generate Image using JeyyAPI"

    async def dofetchimage():
     if imagefilter in app.imagetypes:
            async with aiohttp.ClientSession(headers=app.jeyyheader) as sus:
              async with sus.get(f"{app.jeyybase_url + '/image/' + imagefilter}", params={'image_url': member.avatar_url if member else ctx.author.avatar_url}) as resp:
                print(await resp.read())
                theimg = io.BytesIO(await resp.read())
                print("Image has been saved?")
                return await ctx.edit(Message(file=("output.gif", theimg, "image/gif")))
     else:
                return ctx.edit("Not Found")

    asyncio.create_task(dofetchimage())
    return Message(deferred=True)

@generateimage.autocomplete()
def more_autocomplete_handler(ctx, imagefilter=None):
    if app.isgimg_started:
       pass
    else:
       print("task start")
       asyncio.create_task(getimagelist())
    if imagefilter.focused:
       return [i for i in app.imagetypes if imagefilter.value.lower() in i.lower()]
    else:
       return []


discord.set_route_async("/interactions")

if __name__ == '__main__':
   app.run(port=8080)
