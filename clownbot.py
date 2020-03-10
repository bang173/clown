import discord
from discord.utils import get
import youtube_dl
import random
import os
import json
from discord.ext import commands, tasks
from itertools import cycle
import typing
import asyncio

status = cycle(['Type ^help'])

client = commands.Bot(command_prefix = '^')
os.chdir(r'D:/dbot')

players = {}

client.remove_command('help')

@client.event
async def on_ready():
    change_status.start()
    print('Bot run')

@client.command()
async def help(ctx):
    embed = discord.Embed(
        title = 'Помощь',
        description = '*** - - - Команды - - - ***',
        colour = discord.Colour.red()
    )
    embed.add_field(name='`^hi`', value=' - **приветствие.**', inline=False)
    embed.add_field(name='`^8ball`', value=' - **задать вопрос шару.**', inline=False)
    embed.add_field(name='`^clear {кол-во}`', value=' - **очистить любое количество сообщений в текущем канале.**', inline=False)
    embed.add_field(name='`^kick @user`', value=' - **выгнать пользователя.**', inline=False)
    embed.add_field(name='`^ban @user`', value=' - **забанить пользователя.**', inline=False)
    embed.add_field(name='`^embed`', value=' - **сложная в использовании команда, позволяет в текущем канале создать красивое сообщение. Использование: ^embed "заголовок" "содержание" "дополнение" "автор"\n Если хотите что либо оставить нетронутым, просто оставьте нужную скобку пустой.**', inline=False)
    embed.add_field(name='`^profile @user`', value=' - **просмотреть профиль пользователя(если хотите свой, отметьте себя)**', inline=False)
    embed.set_footer(text='ждите обновлений ;)')
    await ctx.send(embed=embed)

@client.command(aliases=['p', 'prof'])
async def profile(ctx, *, member: discord.Member):
    fmt = 'Пользователь   ***{0.mention}***\n \n Ник на сервере - ***{0.nick}***\n \n  Присоединился к серверу -  `{0.joined_at}`\n \n Бустит с   `{0.premium_since}`\n \n Мобильный статус(надо что бы был статус "онлайн") - `{0.mobile_status}`\n \n Статус - `{0.status}`\n \n Бот? - ***{0.bot}***\n \n ID = `{0.id}`\n {0.avatar_url}'
    await ctx.send(fmt.format(member))

@profile.error
async def p_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send('Неизвестный аргумент, вероятно вы не отметили пользователя.')

@profile.error
async def p1_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Вы не отметили пользователя.')

@client.event
async def on_member_join(ctx, member: discord.Member):
    print('member joined.')
    await ctx.send('Пользователь {0} присоединился к серверу'.format(member))

@client.event
async def on_member_remove(ctx, member: discord.Member):
    print('member left.')
    await ctx.send('Пользователь {0} покинул сервер'.format(member))

@client.command()
async def hi(ctx):
    await ctx.send('Привет!')

class Slapper(commands.Converter):
    async def convert(self, ctx, argument):
        to_slap = random.choice(ctx.guild.members)
        return '**{0.author}** дал подщёчину **{1}** потому, что ***{2}***'.format(ctx, to_slap, argument)

@client.command()
async def slap(ctx, *, reason: Slapper):
    await ctx.send(reason)

@client.command()
async def tst(ctx, member: discord.Member):
    await ctx.send(f'{member.mention}'.format(member))

@client.command()
async def massban(ctx, members: commands.Greedy[discord.Member], delete_days: typing.Optional[int] = 0, *, reason: str):
    for member in members:
        await member.ban(delete_message_days=delete_days, reason=reason)

@client.command()
async def testembed(ctx):
    embed = discord.Embed(

        title = 'Test',
        description = 'test description',
        colour = discord.Colour.blue()
    )
    embed.set_footer(text='Test footer')
    embed.set_author(name='test author')
    embed.add_field(name='test field', value='test field value', inline=False)
    await ctx.send(embed=embed)

@client.command(aliases=['8ball'])
async def _8ball(ctx, *, question):
    responses = ['Что бы ответить...',
                'Возможно...',
                'Да', 'Нет']
    await ctx.send(f'Вопрос: {question}\nОтвет: {random.choice(responses)}')

@_8ball.error
async def ball_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Задайте вопрос.')

@_8ball.error
async def ball2_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send('Я не понимаю вашего вопроса.')

@client.command()
async def embed(ctx, arg1, arg2, arg3, arg4):
    embed = discord.Embed(
        title = '{}'.format(arg1),
        description = '{}'.format(arg2),
        colour = discord.Colour.green()
    )
    embed.set_footer(text='{}'.format(arg3))
    embed.set_author(name='{}'.format(arg4))
    await ctx.send(embed=embed)

@embed.error
async def embed_error(ctx, error):
    if isinstance(error, commands.ExpectedClosingQuoteError):
        await ctx.send('Вы долны использовать ковычки')

@embed.error
async def embed1_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Использование: ^embed "заголовок" "содержание" "дополнение" "автор"(оставьте пустым то, что вам не нужно).')

@embed.error
async def embed2_error(ctx, error):
    if isinstance(error, commands.InvalidEndOfQuotedStringError):
        await ctx.send('Перед и после ковычек должен быть пробел.')

@embed.error
async def embed3_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send('Вы использовали неверные аргументы.')

@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount : int):
    await ctx.channel.purge(limit=amount)
    await ctx.send('Очистка сообщений...')

@clear.error 
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Выберите сколько сообщений надо стереть.')

@clear.error
async def clear1_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send('Указаны неверные аргументы.')

@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'Пользователь {member.mention} выгнан')

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Укажите пользователя.')

@kick.error
async def kick2_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send('Вы должны отметить пользователя.')

@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send('Пользователь {0.mention} забанен'.format(member))

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Укажите пользователя.')

@ban.error
async def ban2_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send('Вы должны отметить пользователя.')


def isitme(ctx):
    return ctx.author.id == 616691484057534465

@client.command()
@commands.check(isitme)
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    await ctx.send('Библиотека импортирована.')

@client.command()
@commands.check(isitme)
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    await ctx.send('Библиотека удалена.')

@client.command(pass_context=True, aliases=['j', 'joi'])
async def join(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

    await voice.disconnect()

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        print(f'The bot has connected to {channel}\n')

    await ctx.send(f'Подключено к {channel}')

@client.command(pass_context=True, aliases=['l', 'lea'])
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
        print(f'The bot has left {channel}')
        await ctx.send(f'Отключено от {channel}')
    else:
        print('Bot was told to leave voice channel, bot was not in one.')
        await ctx.send('Я не подключен ни к какому каналу.')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

@tasks.loop(seconds=8)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))


token = os.environ.get('BOT_TOKEN')

client.run(token)
