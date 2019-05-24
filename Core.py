import os
import sys
import aiohttp
import discord
from EmojiGuardian import EmojiGuardian
from discord.ext import commands

try:
    with open("token.txt", "r") as f:
        token = f.read()
except:
    print("Unable to open token.txt, did you place it in this directory?")
    sys.exit(0)
        

bot = commands.Bot(command_prefix='>')

# list of extensions to be loaded on startup
cog_list = ["EmojiGuardian"]

@bot.event
async def on_ready():
    info = await bot.application_info()
    bot.owner_id = info.owner.id
    permissions = discord.permissions.Permissions.general()

    bot.summon_link = discord.utils.oauth_url(client_id=bot.user.id, permissions=permissions)
    print(f"logged in as {info.name}")
    print(f"owner_id is {bot.owner_id}")
    for cog in cog_list:
        bot.load_extension(cog)


@bot.event
async def on_command_error(ctx: commands.Context, error: commands.CommandError):
    print("\n[Command Error]")
    print(ctx.message.author)
    print(error.args)
    print(ctx.message.content)


@bot.command()
async def load_cog(ctx: commands.context, cog: str):
    try:
        bot.load_extension(cog)
        #bot.add_cog(bot.get_cog(cog))
        await ctx.send(f"{cog} loaded")
    except:
        await ctx.send(f"failed to load {cog}, are you sure it's a real cog?")


@bot.command()
async def reload_cog(ctx: commands.context, cog: str):
    try:
        bot.reload_extension(cog)
        #bot.remove_cog(bot.get_cog(cog))
        #bot.add_cog(bot.get_cog(cog))
        await ctx.send(f"reloaded {cog}")
    except:
        await ctx.send(f"failed to reload {cog}, are you sure it's a real cog?")


@bot.command()
async def echo(ctx, message: str = "hello"):
    await ctx.send(message)


@bot.command()
async def show(ctx, url: str):
    embed = discord.Embed()
    embed.add_field("Title", ctx.message.author.name)
    embed.set_image(url)
    await ctx.send(embed=embed)


@bot.command()
async def logout(ctx):
    await ctx.send("logging out")
    await bot.logout()


bot.run(token)
