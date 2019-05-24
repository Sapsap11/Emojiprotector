import discord
from discord.ext import commands


class EmojiGuardian(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def react(self, ctx: commands.Context, emoji: discord.Emoji):
        await ctx.message.add_reaction(emoji)

    @commands.command()
    async def fullreact(self, ctx: commands.context):
        for emoji in ctx.guild.emojis:
            await ctx.message.add_reaction(emoji)

def setup(bot):
    bot.add_cog(EmojiGuardian(bot))