# Mr.Pepito - A discord bot
import os
import discord
import time
import random
import datetime
from dotenv import load_dotenv

load_dotenv()

default_intents = discord.Intents.all()
bot = discord.Bot(intends=default_intents)

TOKEN = os.getenv('TOKEN')
OWNER = os.getenv('OWNER')


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
            if "Missing Permissions" in str(e):
                await r_msg.respond("*I don't have permission to timeout this user!*")
    else:
        r_embed.description = "**CLICK!** \nYou survived!"
        r_embed.colour = 0x00ff00
        r_embed.remove_image()
        r_embed.remove_footer()
        await r_msg.edit(embed=r_embed)


@bot.slash_command(name="blackjack", description="Play a hand of blackjack")
async def blackjack(ctx):
    deck = {"A♠️": 11, "2♠️": 2, "3♠️": 3, "4♠️": 4, "5♠️": 5, "6♠️": 6, "7♠️": 7, "8♠️": 8, "9♠️": 9, "10♠️": 10, "J♠️": 10, "Q♠️": 10, "K♠️": 10,
            "A♣️": 11, "2♣️": 2, "3♣️": 3, "4♣️": 4, "5♣️": 5, "6♣️": 6, "7♣️": 7, "8♣️": 8, "9♣️": 9, "10♣️": 10, "J♣️": 10, "Q♣️": 10, "K♣️": 10,
            "A♥️": 11, "2♥️": 2, "3♥️": 3, "4♥️": 4, "5♥️": 5, "6♥️": 6, "7♥️": 7, "8♥️": 8, "9♥️": 9, "10♥️": 10, "J♥️": 10, "Q♥️": 10, "K♥️": 10,
            "A♦️": 11, "2♦️": 2, "3♦️": 3, "4♦️": 4, "5♦️": 5, "6♦️": 6, "7♦️": 7, "8♦️": 8, "9♦️": 9, "10♦️": 10, "J♦️": 10, "Q♦️": 10, "K♦️": 10}
    player_hand = []
    dealer_hand = []
    player_score = 0
    dealer_score = 0
    for i in range(2):
        card = random.choice(list(deck.keys()))
        player_hand.append(card)
        player_score += deck[card]
        del deck[card]
    for i in range(2):
        card = random.choice(list(deck.keys()))
        dealer_hand.append(card)
        dealer_score += deck[card]
        del deck[card]
    b_embed = discord.Embed(title="Blackjack", description="You have been dealt two cards", color=0x0000ff)
    b_embed.add_field(name="Your hand", value=f"{player_hand[0]} and {player_hand[1]}", inline=False)
    b_embed.add_field(name="Your score", value=str(player_score), inline=False)
    b_embed.add_field(name="Dealer's hand", value=f"{dealer_hand[0]}", inline=False)
    b_embed.add_field(name="Dealer's score", value="?", inline=False)
    b_embed.set_footer(text="Type /hit or /stand")
    b_view = discord.ui.View()
    b_button_hit = discord.ui.Button(label="Hit", style=discord.ButtonStyle.success)
    b_button_stand = discord.ui.Button(label="Stand", style=discord.ButtonStyle.danger)
    b_view.add_item(b_button_hit)
    b_view.add_item(b_button_stand)
    b_msg = await ctx.respond(embed=b_embed, view=b_view)

    async def hit():
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
            b_embed.set_field_at(2, name="Dealer's hand", value=f"{', '.join(dealer_hand)}", inline=False)
            b_embed.set_field_at(3, name="Dealer's score", value=dealer_score, inline=False)
            b_embed.colour = 0xff0000
            b_embed.remove_footer()
            await b_msg.edit(embed=b_embed, view=None)
            return
        b_button_hit.callback = hit

    async def stand():
        nonlocal dealer_score
        nonlocal dealer_hand
        while dealer_score < 17:
            cards = random.choice(list(deck.keys()))
            dealer_hand.append(cards)
            dealer_score += deck[cards]
            del deck[cards]
        b_embed.set_field_at(2, name="Dealer's hand", value=f"{', '.join(dealer_hand)}", inline=False)
        b_embed.set_field_at(3, name="Dealer's score", value=dealer_score, inline=False)
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
            return

    b_button_hit.callback = hit
    b_button_stand.callback = stand


@bot.slash_command(name="bomb", description="Plant a bot for a user to defuse")
async def bombe(ctx, user: discord.Member = None):
    if user is None:
        user = ctx.author
    b_embed = discord.Embed(title="A bomb has been planted",
                            description=f"A bomb is planted on {user.mention}. You have 5 minutes to defuse the bomb!\nIf you chose the wrong cable you may explode.",
                            color=0x0000ff)
    b_embed.set_footer(text="click the button to defuse the bomb")
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

    async def explode_by_timeout():
        b_embed.description = "Times up! The bomb has exploded!"
        b_embed.colour = 0xff0000
        b_embed.remove_footer()
        await b_msg.edit(embed=b_embed, view=None)
        try:
            await user.create_dm()
            await user.dm_channel.send(
                f"The blast expelled you from the server.\nHere's a link to join it: {invite.url}")
            await user.kick(reason="The bomb exploded")
        except Exception as e:
            print(f"Failed to kick user: {e}")
            if "Missing Permissions" in str(e):
                await b_msg.respond("*I don't have permission to kick this user!*")
        return

    b_view.on_timeout = explode_by_timeout

    wrong_cable = random.choice(["red", "blue", "green"])

    async def defuse_red():
        if wrong_cable == "red":
            b_embed.description = "You chose the wrong cable! The bomb has exploded!"
            b_embed.colour = 0xff0000
            b_embed.remove_footer()
            await b_msg.edit(embed=b_embed, view=None)
            try:
                await user.create_dm()
                await user.dm_channel.send(
                    f"The blast expelled you from the server.\nHere's a link to join it: {invite.url}")
                await user.kick(reason="The bomb exploded")
            except Exception as e:
                print(f"Failed to kick user: {e}")
                if "Missing Permissions" in str(e):
                    await b_msg.respond("*I don't have permission to kick this user!*")
            return
        b_embed.description = f"You defused the bomb! The wrong cable was {wrong_cable}."
        b_embed.colour = 0x00ff00
        b_embed.remove_footer()
        await b_msg.edit(embed=b_embed, view=None)
        return

    async def defuse_blue():
        if wrong_cable == "blue":
            b_embed.description = "You chose the wrong cable! The bomb has exploded!"
            b_embed.colour = 0xff0000
            b_embed.remove_footer()
            await b_msg.edit(embed=b_embed, view=None)
            try:
                await user.create_dm()
                await user.dm_channel.send(
                    f"The blast expelled you from the server.\nHere's a link to join it: {invite.url}")
                await user.kick(reason="The bomb exploded")
            except Exception as e:
                print(f"Failed to kick user: {e}")
                if "Missing Permissions" in str(e):
                    await b_msg.respond("*I don't have permission to kick this user!*")
            return
        b_embed.description = f"You defused the bomb! The wrong cable was {wrong_cable}."
        b_embed.colour = 0x00ff00
        b_embed.remove_footer()
        await b_msg.edit(embed=b_embed, view=None)
        return

    async def defuse_green():
        if wrong_cable == "green":
            b_embed.description = "You chose the wrong cable! The bomb has exploded!"
            b_embed.colour = 0xff0000
            b_embed.remove_footer()
            await b_msg.edit(embed=b_embed, view=None)
            try:
                await user.create_dm()
                await user.dm_channel.send(
                    f"The blast expelled you from the server.\nHere's a link to join it: {invite.url}")
                await user.kick(reason="The bomb exploded")
            except Exception as e:
                print(f"Failed to kick user: {e}")
                if "Missing Permissions" in str(e):
                    await b_msg.respond("*I don't have permission to kick this user!*")
            return
        b_embed.description = f"You defused the bomb! The wrong cable was {wrong_cable}."
        b_embed.colour = 0x00ff00
        b_embed.remove_footer()
        await b_msg.edit(embed=b_embed, view=None)
        return

    b_button_red.callback = defuse_red
    b_button_blue.callback = defuse_blue
    b_button_green.callback = defuse_green


@bot.slash_command(name="clear", description="Clear a specified number of messages")
async def clear(ctx, amount: int = None):
    if ctx.author.guild_permissions.manage_messages:
        if amount is None:
            try:
                print(
                    f"Clearing all messages in {ctx.guild.name} ({ctx.guild.id}) in channel {ctx.channel.name} ({ctx.channel.id})")
                msg = await ctx.respond("Clearing all messages...", ephemeral=True)
                await ctx.channel.purge()
                await msg.edit(content="Cleared all messages", ephemeral=True)
                await msg.delete(delay=5)
                print("Cleared all messages")
            except Exception as e:
                print(f"Failed to clear messages: {e}")
                await ctx.respond("Failed to clear messages", ephemeral=True)
        else:
            print(
                f"Clearing {amount} messages in {ctx.guild.name} ({ctx.guild.id}) in channel {ctx.channel.name} ({ctx.channel.id})")
            msg = await ctx.respond(f"Clearing {amount} messages...", ephemeral=True)
            await ctx.channel.purge(limit=amount)
            await msg.respond(f"Cleared {amount} messages", ephemeral=True)
            print(f"Cleared {amount} messages")
    else:
        await ctx.respond("You do not have permission to use this command")


bot.run(TOKEN)
