import os
import aiohttp
import discord
from EmojiGuardian import EmojiGuardian
from discord.ext import commands

token = os.environ["token"]
if not token:
    raise OSError("No token enviroment variable")

bot = commands.Bot(command_prefix='>')


@bot.event
async def on_ready():
    info = await bot.application_info()
    bot.owner_id = info.owner.id
    permissions = discord.permissions.Permissions.general()

    bot.summon_link = discord.utils.oauth_url(client_id=bot.user.id, permissions=permissions)
    print(f"logged in as {info.name}")
    print(f"owner_id is {bot.owner_id}")
    bot.session = aiohttp.ClientSession()

    for cog in bot.cogs:
        bot.add_cog(bot.get_cog(cog))


@bot.event
async def on_command_error(ctx: commands.Context, error: commands.CommandError):
    print("\n[Command Error]")
    print(ctx.message.author)
    print(ctx.message.content)


@bot.command()
async def load_cog(ctx: commands.context, cog: str):
    if cog in bot.cogs:
        bot.add_cog(bot.get_cog(cog))
        await ctx.send(f"{cog} loaded")
    else:
        await ctx.send(f"failed to load {cog}, are you sure it's a real cog?")


@bot.command()
async def reload_cog(ctx: commands.context, cog: str):
    if cog in bot.cogs:
        bot.remove_cog(bot.get_cog(cog))
        bot.add_cog(bot.get_cog(cog))
        await ctx.send(f"reloaded {cog}")
    else:
        await ctx.send(f"failed to reload {cog}, are you sure it's a real cog?")


@bot.command()
async def echo(ctx, message: str = "hello"):
    await ctx.send(message)


@bot.command()
async def show(ctx, url: str):
    picture = await bot.session.get(url)

    await ctx.send("thing", embed=picture)


@bot.command()
async def logout(ctx):
    await bot.session.close()
    await ctx.send("logging out")
    await bot.logout()


bot.run(token)
