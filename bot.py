import discord
from discord.ext import commands
from discord.ext.commands import Bot
Bot = commands.Bot(command_prefix= "!")
@Bot.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name="новичок")
    await bot.add_roles(member, role)
@Bot.event
async def on_ready():
    print("!Bot started")
@Bot.command()
async def clown(ctx):
    author = ctx.message.author
    await ctx.send(f"Привет, я тестовый дискорд-бот банги написанный на Python {author.mention}")
@Bot.command()
@commands.has_permissions(kick_members= True)
async def mute(ctx, member: discord.Member):
    mute_role = discord.utils.get(ctx.message.guild.roles, name= "Mute")
    await member.add_roles(mute_role)
Bot.run(open('token.txt', 'r').readline())