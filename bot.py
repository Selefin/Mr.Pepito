# Mr.Pepito - A discord bot
import asyncio
import datetime
import json
import os
import random
import re
import time
import urllib.request
import discord
from dotenv import load_dotenv
import yt_dlp as youtube_dl

load_dotenv()

default_intents = discord.Intents.all()
default_intents.members = True
bot = discord.Bot(intents=default_intents)

TOKEN = os.getenv('TOKEN')
OWNER = os.getenv('OWNER')

perm_missing = "Missing Permissions"
perm_kick_missing = "*I don't have permission to kick this user!*"


## Events
@bot.event
async def on_ready():
    print(f'{bot.user} is ready!')
    synced = await bot.get_desynced_commands()
    if synced:
        for guild in bot.guilds:
            try:
                await bot.sync_commands(guild_ids=[guild.id])
                print(f"Synced {len(synced)} commands in {guild.name} ({guild.id})")
            except Exception as e:
                print(f"Failed to sync commands: {e}")


@bot.event
async def on_connect():
    print("Bot connected to discord")


@bot.event
async def on_disconnect():
    print("Bot disconnected from discord")


@bot.listen()
async def on_ready():
    if not os.path.exists('./roles'):
        os.makedirs('./roles')
    for guild in bot.guilds:
        members = guild.fetch_members()
        if members is None:
            print(f"Failed to fetch members in {guild.name}")
            continue
        guild_roles = {}
        while True:
            try:
                member = await members.__anext__()
                member_roles = [role.id for role in member.roles if role.name != "@everyone"]
                guild_roles[member.id] = member_roles
            except StopAsyncIteration:
                break
        file_path = f'./roles/{guild.id}_roles.json'
        with open(file_path, 'w') as f:
            json.dump(guild_roles, f, indent=4)
        print(f"Roles for guild {guild.name} have been saved to {file_path}")


@bot.listen()
async def on_member_join(member):
    file_path = f'./roles/{member.guild.id}_roles.json'
    if not os.path.exists(file_path):
        return
    with open(file_path, 'r') as f:
        guild_roles = json.load(f)
    if str(member.id) not in guild_roles:
        return
    roles = [member.guild.get_role(role_id) for role_id in guild_roles[str(member.id)]]
    await member.add_roles(*roles)
    print(f"Roles have been added to {member.name} in {member.guild.name}")


## Commands
@bot.slash_command(name="commands", description="List all available commands")
async def commands(ctx):
    c_embed = discord.Embed(title="**Commands**", description="Here are all the commands available:", color=0xff00ff)
    command_list = bot.application_commands
    for command in command_list:
        c_embed.add_field(name=f"/{command.name}", value=command.description, inline=False)
    await ctx.respond(embed=c_embed)


@bot.slash_command(name="ping", description="Check the bot's latency")
async def ping(ctx):
    await ctx.respond(f"{int(bot.latency * 1000)}ms")


@bot.slash_command(name="disconnect", description="Disconnect the bot from discord")
async def disconnect(ctx):
    if ctx.author.id != int(OWNER):
        await ctx.respond("You do not have permission to use this command")
        return
    await ctx.respond("Disconnecting...")
    print("Disconnecting...")
    await bot.close()
    exit(0)


@bot.slash_command(name="roulette", description="Play a game of russian roulette")
async def roulette(ctx):
    r_embed = discord.Embed(title="Russian Roulette", description="You have a 1 in 6 chance of dying", color=0x0000ff)
    r_embed.set_image(url="https://media.tenor.com/fklGVnlUSFQAAAAd/russian-roulette.gif")
    r_embed.set_footer(text="Good luck!")
    r_msg = await ctx.respond(embed=r_embed)
    time.sleep(2.1)
    if random.randint(1, 6) == 6:
        r_embed.description = "**BANG!** \nYou're dead!"
        r_embed.colour = 0xff0000
        r_embed.remove_image()
        r_embed.set_footer(text="Better luck next time!")
        await r_msg.edit(embed=r_embed)
        try:
            r_duration = datetime.timedelta(minutes=1)
            await ctx.author.timeout_for(duration=r_duration, reason="You died in russian roulette")
        except Exception as e:
            print(f"Failed to timeout user: {e}")
            if perm_missing in str(e):
                await r_msg.respond("*I don't have permission to timeout this user!*")
    else:
        r_embed.description = "**CLICK!** \nYou survived!"
        r_embed.colour = 0x00ff00
        r_embed.remove_image()
        r_embed.remove_footer()
        await r_msg.edit(embed=r_embed)


@bot.slash_command(name="blackjack", description="Play a hand of blackjack")
async def blackjack(ctx):
    deck = {"A♠️": 11, "2♠️": 2, "3♠️": 3, "4♠️": 4, "5♠️": 5, "6♠️": 6, "7♠️": 7, "8♠️": 8, "9♠️": 9, "10♠️": 10,
            "J♠️": 10, "Q♠️": 10, "K♠️": 10,
            "A♣️": 11, "2♣️": 2, "3♣️": 3, "4♣️": 4, "5♣️": 5, "6♣️": 6, "7♣️": 7, "8♣️": 8, "9♣️": 9, "10♣️": 10,
            "J♣️": 10, "Q♣️": 10, "K♣️": 10,
            "A♥️": 11, "2♥️": 2, "3♥️": 3, "4♥️": 4, "5♥️": 5, "6♥️": 6, "7♥️": 7, "8♥️": 8, "9♥️": 9, "10♥️": 10,
            "J♥️": 10, "Q♥️": 10, "K♥️": 10,
            "A♦️": 11, "2♦️": 2, "3♦️": 3, "4♦️": 4, "5♦️": 5, "6♦️": 6, "7♦️": 7, "8♦️": 8, "9♦️": 9, "10♦️": 10,
            "J♦️": 10, "Q♦️": 10, "K♦️": 10}
    player_hand = []
    dealer_hand = []
    player_score = 0
    dealer_score = 0
    for _ in range(2):
        card = random.choice(list(deck.keys()))
        player_hand.append(card)
        player_score += deck[card]
        del deck[card]
    for _ in range(2):
        card = random.choice(list(deck.keys()))
        dealer_hand.append(card)
        dealer_score += deck[card]
        del deck[card]
    d_hand = "Dealer's hand"
    d_score = "Dealer's score"
    b_embed = discord.Embed(title="Blackjack", description="You have been dealt two cards", color=0x0000ff)
    b_embed.add_field(name="Your hand", value=f"{player_hand[0]} and {player_hand[1]}", inline=False)
    b_embed.add_field(name="Your score", value=str(player_score), inline=False)
    b_embed.add_field(name=d_hand, value=f"{dealer_hand[0]}", inline=False)
    b_embed.add_field(name=d_score, value="?", inline=False)
    b_embed.set_footer(text="Type /hit or /stand")
    b_view = discord.ui.View()
    b_button_hit = discord.ui.Button(label="Hit", style=discord.ButtonStyle.success)
    b_button_stand = discord.ui.Button(label="Stand", style=discord.ButtonStyle.danger)
    b_view.add_item(b_button_hit)
    b_view.add_item(b_button_stand)
    b_msg = await ctx.respond(embed=b_embed, view=b_view)

    async def hit(interaction):
        nonlocal player_score
        nonlocal player_hand
        cards = random.choice(list(deck.keys()))
        player_hand.append(cards)
        player_score += deck[cards]
        del deck[cards]
        b_embed.set_field_at(0, name="Your hand", value=f"{', '.join(player_hand)}", inline=False)
        b_embed.set_field_at(1, name="Your score", value=player_score, inline=False)
        await b_msg.edit(embed=b_embed, view=b_view)
        if player_score > 21:
            b_embed.description = "You have gone bust!"
            b_embed.set_field_at(2, name=d_hand, value=f"{', '.join(dealer_hand)}", inline=False)
            b_embed.set_field_at(3, name=d_score, value=dealer_score, inline=False)
            b_embed.colour = 0xff0000
            b_embed.remove_footer()
            await b_msg.edit(embed=b_embed, view=None)
            return
        b_button_hit.callback = hit

    async def stand(interaction):
        nonlocal dealer_score
        nonlocal dealer_hand
        while dealer_score < 17:
            cards = random.choice(list(deck.keys()))
            dealer_hand.append(cards)
            dealer_score += deck[cards]
            del deck[cards]
        b_embed.set_field_at(2, name=d_hand, value=f"{', '.join(dealer_hand)}", inline=False)
        b_embed.set_field_at(3, name=d_score, value=dealer_score, inline=False)
        await b_msg.edit(embed=b_embed)
        if dealer_score > 21:
            b_embed.description = "The dealer has gone bust!"
            b_embed.colour = 0x00ff00
            b_embed.remove_footer()
            await b_msg.edit(embed=b_embed, view=None)
            return
        if dealer_score > player_score:
            b_embed.description = "The dealer wins!"
            b_embed.colour = 0xff0000
            b_embed.remove_footer()
            await b_msg.edit(embed=b_embed, view=None)
            return
        if dealer_score < player_score:
            b_embed.description = "You win!"
            b_embed.colour = 0x00ff00
            b_embed.remove_footer()
            await b_msg.edit(embed=b_embed, view=None)
            return
        if dealer_score == player_score:
            b_embed.description = "It's a draw!"
            b_embed.colour = 0xffff00
            b_embed.remove_footer()
            await b_msg.edit(embed=b_embed, view=None)

    b_button_hit.callback = hit
    b_button_stand.callback = stand


@bot.slash_command(name="bomb", description="Plant a bot for a target to defuse")
async def bomb(ctx, user: discord.Member = None):
    if user is None:
        user = ctx.author

    def create_bomb_embed(target):
        embed = discord.Embed(
            title="A bomb has been planted",
            description=f"A bomb is planted on {target.mention}. You have 5 minutes to defuse the bomb!\nIf you choose the wrong cable, you may explode.",
            color=0x0000ff
        )
        embed.set_footer(text="Click the button to defuse the bomb")
        return embed

    b_embed = create_bomb_embed(user)
    b_view = discord.ui.View()
    b_button_red = discord.ui.Button(label="red", style=discord.ButtonStyle.danger)
    b_button_blue = discord.ui.Button(label="blue", style=discord.ButtonStyle.primary)
    b_button_green = discord.ui.Button(label="green", style=discord.ButtonStyle.success)
    b_view.add_item(b_button_red)
    b_view.add_item(b_button_blue)
    b_view.add_item(b_button_green)
    b_view.timeout = 300
    b_msg = await ctx.respond(embed=b_embed, view=b_view)
    invite = await ctx.channel.create_invite()

    bomb_exploded = "The bomb has exploded!"
    bomb_defused = "The bomb has been defused!"
    cable_boom = "You chose the wrong cable! The bomb has exploded!"

    async def kick_user(target, reason, invite_url):
        try:
            await target.create_dm()
            await target.dm_channel.send(
                f"The blast expelled you from the server.\nHere's a link to join it: {invite_url}")
            await target.kick(reason=reason)
        except Exception as e:
            print(f"Failed to kick target: {e}")
            if perm_missing in str(e).lower():
                await b_msg.respond("I don't have permission to kick users.")

    async def explode_by_timeout():
        b_embed.title = bomb_exploded
        b_embed.description = "Time's up! The bomb has exploded!"
        b_embed.colour = 0xff0000
        b_embed.remove_footer()
        await b_msg.edit(embed=b_embed, view=None)
        await kick_user(user, bomb_exploded, invite.url)

    b_view.on_timeout = explode_by_timeout
    wrong_cable = random.choice(["red", "blue", "green"])

    async def defuse_bomb(color):
        if wrong_cable == color:
            b_embed.title = bomb_exploded
            b_embed.description = cable_boom
            b_embed.colour = 0xff0000
            b_embed.remove_footer()
            await b_msg.edit(embed=b_embed, view=None)
            await kick_user(user, bomb_exploded, invite.url)
        else:
            b_embed.title = bomb_defused
            b_embed.description = f"You defused the bomb! The wrong cable was {wrong_cable}."
            b_embed.colour = 0x00ff00
            b_embed.remove_footer()
            await b_msg.edit(embed=b_embed, view=None)

    b_button_red.callback = lambda interaction: defuse_bomb("red")
    b_button_blue.callback = lambda interaction: defuse_bomb("blue")
    b_button_green.callback = lambda interaction: defuse_bomb("green")


@bot.slash_command(name="clear", description="Clear a specified number of messages")
async def clear(ctx, amount: int = None):
    if ctx.author.guild_permissions.manage_messages:
        if amount is None:
            try:
                print(
                    f"Clearing all messages in {ctx.guild.name} ({ctx.guild.id}) in channel {ctx.channel.name} ({ctx.channel.id})")
                msg = await ctx.respond("Clearing all messages...", ephemeral=True)
                await ctx.channel.purge()
                await msg.edit(content="Cleared all messages")
                print("Cleared all messages")
            except Exception as e:
                print(f"Failed to clear messages: {e}")
                await ctx.respond("Failed to clear messages", ephemeral=True)
        else:
            print(
                f"Clearing {amount} messages in {ctx.guild.name} ({ctx.guild.id}) in channel {ctx.channel.name} ({ctx.channel.id})")
            msg = await ctx.respond(f"Clearing {amount} messages...", ephemeral=True)
            await ctx.channel.purge(limit=amount)
            await msg.respond(f"Cleared {amount} messages")
            print(f"Cleared {amount} messages")
    else:
        await ctx.respond("You do not have permission to use this command")


@bot.slash_command(name="play", description="Play a song from youtube")
async def play(ctx, request: str):
    if ctx.author.voice is None:
        await ctx.respond("You are not in a voice channel")
        return

    voice_channel = ctx.author.voice.channel

    if bot.voice_clients:
        for vc in bot.voice_clients:
            if vc.channel != voice_channel:
                await vc.disconnect(force=False)
            else:
                break
    await voice_channel.connect()

    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    if " " in request:
        request = request.replace(" ", "+")
    request = request.encode('ascii', 'ignore').decode('ascii')
    query_url = f"https://www.youtube.com/results?search_query={request}"
    html = urllib.request.urlopen(query_url)
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())

    if not video_ids:
        await ctx.response.send_message("No video found.")
        return

    await ctx.defer()

    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': False,
        'verbose': True,
    }

    video_url = f"https://www.youtube.com/watch?v={video_ids[0]}"
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=False)
        formats = info.get('formats', None)

        if not formats:
            await ctx.followup.send("No valid audio stream found.")
            return

        audio_format = next((f for f in formats if f.get('acodec') != 'none'), None)
        if not audio_format:
            await ctx.followup.send("No valid audio stream found.")
            return

        url = audio_format['url']
        title = info['title']

    ffmpeg_options = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn',
    }

    if voice_client.is_playing():
        voice_client.stop()

    try:
        voice_client.play(discord.FFmpegPCMAudio(url, **ffmpeg_options))
    except Exception as e:
        print(f"Error playing audio: {e}")
        await ctx.followup.send(f"Error playing audio: {e}")
        return

    await ctx.followup.send(f"Playing {title}\n {video_url}")

    while voice_client.is_playing():
        await asyncio.sleep(1)
    await voice_client.disconnect(force=True)


@bot.slash_command(name="stop", description="Stop the current song")
async def stop(ctx):
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice_client is None:
        await ctx.respond("I am not in a voice channel")
        return

    if voice_client.is_playing():
        voice_client.stop()
        await voice_client.disconnect(force=True)
        await ctx.respond("Stopped the current song")
    else:
        await ctx.respond("No song is currently playing")
        if voice_client.is_connected():
            await voice_client.disconnect(force=True)


bot.run(TOKEN)
