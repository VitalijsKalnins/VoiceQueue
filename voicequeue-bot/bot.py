## Discord Imports
import discord
from discord.ext import commands

## Environment Imports
import os
from dotenv import load_dotenv

## Async Request Library
import aiohttp
import asyncio


## Load environment
load_dotenv("./dev.env")


## Fetch API URLS from environment
GET_PROFILE_REQ = os.getenv("GET_PROFILE")
SET_PROFILE_REQ = os.getenv("SET_PROFILE")
GET_MATCHMAKING_REQ = os.getenv("GET_MATCHMAKING")


## Fetch VoiceQueue Discord Server Id
VOICEQUEUE_SERVER_ID = int(os.getenv("VOICEQUEUE_SERVER_ID"))

## Fetch Maximum Queue Size
MAXIMUM_QUEUE_SIZE = int(os.getenv("MAXIMUM_QUEUE_SIZE"))


## Define Bot Intents
intents = discord.Intents.default()
intents.message_content = True

## Initialize and define Bot
BOT_PREFIX = "!"
bot = commands.Bot(command_prefix="!", intents=intents)


## Define Bot Events
@bot.event
async def on_connect():
    bot.session = aiohttp.ClientSession()

@bot.event
async def on_disconnect():
    await bot.session.close()

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    ## Notify user to directly message the Bot instead of using commands in channels
    if message.guild is not None and message.content.startswith(BOT_PREFIX):
        await message.author.send("Please DM me if you're attempting to use VoiceQueue commands. Use: **!bothelp** for a list of commands.")
        return
    else:
        ## Try processing message as command
        try:
            await bot.process_commands(message)
        except:
            pass

@bot.event
async def on_voice_state_update(user, before, after):
    channel = None
    if before.channel is not None and (after.channel is None or before.channel != after.channel):
        channel = before.channel

    ## Delete channel if both users have left
    if channel and "VoiceQueue" in channel.name and len(channel.members) == 0:
        await channel.delete(reason="Voice channel deleted due to inactivity.")


## Define Bot Commands
@bot.command()
async def bothelp(ctx):
    await ctx.author.send(f"""
    Available commands and usage:\n
    **!getprofile** : gets your current profile, alongside interest(s) / disinterest(s) data.\n
    **!setprofile** <new_profile> : sets a new profile from free-form text, and processes interest(s) / disinterest(s).\n
    **!joinqueue** : joins you into the matchmaking queue.\n
    **!leavequeue** : removes you from the matchmaking queue.""")


@bot.command()
async def getprofile(ctx):
    ## Fetch profile from voicequeue-api
    async with bot.session.get(f"{GET_PROFILE_REQ}/{ctx.author.id}") as resp:
        if resp.status == 200:
            data = await resp.json()
            print(data)
            
            ## Format INTERESTS / DISINTERESTS for output
            interests = ""
            disinterests = ""
            note = f":warning: **NOTE**: INTEREST / DISINTEREST strength ranges from **0 - 1**!"
            for e in data["entities"]:
                if e["type"] == 1:
                    interests+=f"**PHRASE**: '*{e['text']}*'\n**SUBJECT**: '*{e['subject']}*'\n**INTEREST STRENGTH**: {round(e['sentiment'], 2)}\n\n"
                else:
                    disinterests+=f"**PHRASE**: '*{e['text']}*'\n**SUBJECT**: '*{e['subject']}*'\n**DISINTEREST STRENGTH**: {round(abs(e['sentiment']), 2)}\n\n"
            if interests == "":
                interests+= "**NONE**\n\n"
            if disinterests == "":
                disinterests+= "**NONE**\n\n"
            ## Format output
            formatted = f":speech_balloon: **PROFILE INPUT**\n'*{data['text']}*'\n\n\n:thumbsup: **PROFILE INTERESTS**\n\n{interests}\n:thumbsdown: **PROFILE DISINTERESTS**\n\n{disinterests}\n{note}"

            ## Display profile to user
            await ctx.author.send(formatted)


@bot.command()
async def setprofile(ctx, *, new_profile: str):
    ## Notify user profile set operation
    await ctx.author.send(f"Setting profile... this can take **1 - 3** seconds!")

    ## Set profile from voicequeue-api
    async with bot.session.post(f"{SET_PROFILE_REQ}", json={"id": ctx.author.id, "text": new_profile}) as resp:
        if resp.status == 200:
            await ctx.author.send(f"Profile set successfully, you can view it with: **!getprofile**. :partying_face:")
        else:
            await ctx.author.send(f"Profile was not set, failed to extract any interests / disinterests... :confused:")



## Initialize Matchmaking Queue
matchmaking_queue = set()

async def channel_cleanup_check(channel, users, timeout):
    await asyncio.sleep(timeout)

    if not channel:
        return
    if len(channel.members) == 2:
        return
    elif len(channel.members) == 1:
        ## Fetch user to kick
        user_to_kick = channel.members[0]
        other_user = users[0] if users[0].id != user_to_kick.id else users[1]

        ## Inform the user who joined that their match did not join on time
        await user_to_kick.move_to(None)
        await user_to_kick.send("Unfortunately your match did not join on time... :confused:\nPlease try matchmaking again!")

        ## Inform the user who did not join that they did not join on time
        await other_user.send("You did not join the voice channel on time... match aborted :warning:")
    else:
        for user in users:
            await user.send("Both parties did not join the voice channel on time... match aborted :warning:")

    ## Finally delete voice channel
    try:
        await channel.delete(reason="Match cancelled due to inactivity.")
    except discord.errors.NotFound:
        pass


async def attempt_matchmaking(ctx):
    guild = bot.get_guild(VOICEQUEUE_SERVER_ID)

    ## Check queue capacity
    if len(matchmaking_queue) != MAXIMUM_QUEUE_SIZE:
        return

    ## Fetch matchmaking from voicequeue-api
    async with bot.session.get(GET_MATCHMAKING_REQ, json={"ids": list(matchmaking_queue)}) as resp:
        if resp.status != 200:
            return
        pairs = await resp.json()

    for user1_id, user2_id in pairs["matches"].items():
        ## Fetch members
        user1 = await bot.fetch_user(int(user1_id))
        user2 = await bot.fetch_user(int(user2_id))
        
        if not user1 or not user2:
            continue
        
        ## Permission overwrites for new channel
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False, connect=False),
            user1: discord.PermissionOverwrite(view_channel=True, connect=True, speak=True),
            user2: discord.PermissionOverwrite(view_channel=True, connect=True, speak=True),
            guild.me: discord.PermissionOverwrite(view_channel=True, connect=True)
        }

        ## Fetch number of matchaking channels
        num_channels = 0
        for channel in guild.channels:
            if "VoiceQueue" in channel.name:
                num_channels += 1

        ## Define the new channel name
        channel_name = f"VoiceQueue - {num_channels + 1}"

        ## Create new channel
        channel = await guild.create_voice_channel(channel_name, overwrites=overwrites, user_limit=2)
        ## Create new invites to voice channel
        invite = await channel.create_invite()
        ## Define a notification to send to the user of invite
        notification = f"You have been matched! :partying_face:\nJoin via invite: {invite.url}\nYou have 2 minutes to join."

        ## Send notification invite
        await user1.send(notification)
        await user2.send(notification)

        ## Remove users from matchmaking queue
        matchmaking_queue.discard(int(user1_id))
        matchmaking_queue.discard(int(user2_id))

        ## Schedule task to remove voice channel if both parties do not join
        bot.loop.create_task(channel_cleanup_check(channel, [user1, user2], 120))


@bot.command()
async def joinqueue(ctx):
    user_id = ctx.author.id

    if user_id in matchmaking_queue:
        await ctx.author.send(f"You are already in queue. :thinking:")
    else:
        matchmaking_queue.add(user_id)
        await ctx.author.send(f"You have joined the queue! Waiting for a match... :head_shaking_horizontally:\nTotal Users in queue: **{len(matchmaking_queue)}**")
        await attempt_matchmaking(ctx)

@bot.command()
async def leavequeue(ctx):
    user_id = ctx.author.id

    if not user_id in matchmaking_queue:
        await ctx.author.send(f"You are not in the queue. :thinking:")
    else:
        matchmaking_queue.remove(user_id)
        await ctx.author.send(f"You have left the queue. :saluting_face:")



if __name__ == "__main__":
    ## Fetch Discord Token from environment
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

    if not DISCORD_TOKEN:
        raise ValueError("No DISCORD_TOKEN found in environment.")
    
    ## Run Bot using DISCORD_TOKEN
    bot.run(DISCORD_TOKEN)