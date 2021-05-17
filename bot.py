import discord
from discord.ext import commands
from cogs import praw
import youtube_dl
import json
import random
from discord.utils import get
from discord.ext.commands import has_permissions, MissingPermissions
import asyncio

TOKEN = 'YourTokenHere'

PREFIX = 'i!'

bot = commands.Bot(command_prefix=PREFIX)

bot.load_extension("cogs.memes")

bot.remove_command("help")

@bot.event
async def on_ready():
    print('YourBot is Ready!')

@bot.command()
async def help(ctx):
 
        em = discord.Embed(title = "Help", description ="", color = 0x00a8ff)
        em.add_field(name="`i!clear <amount>`", value="Deletes a certain ammount of messages")
        em.add_field(name="`i!kick <user>`", value="kicks a user")
        em.add_field(name="`i!ban <user>`", value="bans a user")
        em.add_field(name="`i!say <text>`", value="bot dictates what you say")
        em.add_field(name="`i!meme`", value="Funny")
        em.add_field(name="`i!kiss <user>`", value="Kiss someone") 
        em.add_field(name="`i!punch<user>`", value="Punch someone")
        em.add_field(name="`i!slap<user>`", value="Slap somone")
        em.add_field(name="`i!join`", value="The bot joins the music channel")
        em.add_field(name="`i!play`", value="Play some music")
        em.add_field(name="`i!next`", value="skip the song")
        em.add_field(name="`i!queue`", value="Queue a song")
        em.add_field(name="`i!eightball`", value="The magic eightball")
        em.add_field(name="`i!new`", value="Create a new ticket")
        em.add_field(name="`i!close`", value="Close a ticket")
        em.add_field(name="`i!mute <user>`", value="Mute a user")
        em.add_field(name="`i!unmute <user>`", value="Unmute a user")
        em.add_field(name="`i!addaccess <user>`", value="Give someone access to tickets")
    
        em.set_footer(text="Help")

        await ctx.send(embed=em)

@bot.command()
async def slap(ctx, *,member : discord.Member):
    slapb = discord.Embed(title = "Ouch, that mustve hurt!",description = str(ctx.author) + ' slapped ' + str(member), color=discord.Color(0x00a8ff))
    slapb.set_image(url='https://cdn.weeb.sh/images/r1lxO_QIf.gif')
    await ctx.send (embed=slapb)
    
@bot.command()
async def say(ctx, *,arg):
    await ctx.send(arg)
    
@bot.command()
async def punch(ctx, *,member : discord.Member):
    punch = discord.Embed(title = " He deserved that!",description = str(ctx.author) + ' punched ' + str(member), color=discord.Color(0x00a8ff))
    punch.set_image(url='https://cdn.weeb.sh/images/SJAfH5TOz.gif')
    await ctx.send (embed=punch) 
    
@bot.command()
async def kiss(ctx, *, member : discord.Member):
    kiss = discord.Embed(title="How cute!", description=str(ctx.author) + ' kissed ' + str(member), color=discord.Color(0x00a8ff))
    kiss.set_image(url='https://cdn.weeb.sh/images/Bkk_hpdv-.gif')
    await ctx.send(embed=kiss)
    
@bot.command(aliases=['8ball', '8Sock', 'eightball'])
async def _8ball(ctx, *, question):
    responses = ['It is certain.',
                 'It is decidedly so.',
                 'Without a doubt.',
                 'Yes, Definitely.',
                 'You may rely on it',
                 'As I see it, Yes.',
                 'Most likely.',
                 'Outlook good.',
                 'Yes',
                 'Signs point to yes.',
                 'Reply hazy, try again',
                 'Ask again later.',
                 'I will not tell you this now.',
                 'I cannot predict this at the moment',
                 'Concentrate and ask me again',
                 "Don't count on it",
                 'My reply is no!',
                 'My sources are pointing to no.',
                 'The outlook is not so good.',
                 'It is very doubtful.']
    await ctx.send(f'Question: {question} \nAnswer: {random.choice(responses)}')
    
@bot.command()
@commands.has_permissions(kick_members=True)
async def mute(ctx, member : discord.Member):
    muted_role = ctx.guild.get_role(754709622379774023)
    
    await member.add_roles(muted_role)

    await ctx.send(member.mention + " has been muted")
    
@bot.command()
async def unmute(ctx, member : discord.Member):
    emuted_role = ctx.guild.get_role(754709622379774023)
    await member.remove_roles(emuted_role)
    await ctx.send(member.mention + " has been unmuted")
    
@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send("User has been kicked")
    
@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send("User has been banned")
    
@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount : int):
    await ctx.channel.purge(limit=amount)

@bot.command(pass_context=True, aliases=['j', 'joi'])
async def join(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

    await voice.disconnect()

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        print(f"The bot has connected to {channel}\n")

        embed = discord.Embed(title = f"Joined {channel}", color = discord.Color.red())
        await ctx.send(embed=embed)

@bot.command(pass_context=True, aliases=['l', 'lea'])
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
        print(f"The bot has left {channel}")
        embed = discord.Embed(title = f"Left {channel}", color = discord.Color.red())
        await ctx.send(embed=embed)
    else:
        print("Bot was told to leave voice channel, but was not in one")
        embed = discord.Embed(title = "Don't think I am in a voice channel", color = discord.Color.red())
        await ctx.send(embed=embed)

@bot.command(pass_context=True, aliases=['p', 'pla'])
async def play(ctx, url: str):

    def check_queue():
        Queue_infile = os.path.isdir("./Queue")
        if Queue_infile is True:
            DIR = os.path.abspath(os.path.realpath("Queue"))
            length = len(os.listdir(DIR))
            still_q = length - 1
            try:
                first_file = os.listdir(DIR)[0]
            except:
                print("No more queued song(s)\n")
                queues.clear()
                return
            main_location = os.path.dirname(os.path.realpath(__file__))
            song_path = os.path.abspath(os.path.realpath("Queue") + "\\" + first_file)
            if length != 0:
                print("Song done, playing next queued\n")
                print(f"Songs still in queue: {still_q}")
                song_there = os.path.isfile("song.mp3")
                if song_there:
                    os.remove("song.mp3")
                shutil.move(song_path, main_location)
                for file in os.listdir("./"):
                    if file.endswith(".mp3"):
                        os.rename(file, 'song.mp3')

                voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
                voice.source = discord.PCMVolumeTransformer(voice.source)
                voice.source.volume = 0.07

            else:
                queues.clear()
                return

        else:
            queues.clear()
            print("No songs were queued before the ending of the last song\n")



    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
            queues.clear()
            print("Removed old song file")
    except PermissionError:
        print("Trying to delete song file, but it's being played")
        embed = discord.Embed(title = "ERROR: Music playing", color = discord.Color.red())
        await ctx.send(embed=embed)
        return


    Queue_infile = os.path.isdir("./Queue")
    try:
        Queue_folder = "./Queue"
        if Queue_infile is True:
            print("Removed old Queue Folder")
            shutil.rmtree(Queue_folder)
    except:
        print("No old Queue folder")

    embed = discord.Embed(title = "Getting everything ready now", color = discord.Color.red())
    await ctx.send(embed=embed)

    voice = get(bot.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print("Downloading audio now\n")
            ydl.download([url])
    except:
        print("FALLBACK: youtube-dl does not support this URL, using Spotify (This is normal if Spotify URL)")
        c_path = os.path.dirname(os.path.realpath(__file__))
        system("spotdl -f " + '"' + c_path + '"' + " -s " + url)

    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name = file
            print(f"Renamed File: {file}\n")
            os.rename(file, "song.mp3")

    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.07

    nname = name.rsplit("-", 2)
    embed = discord.Embed(title = f"Playing: {nname[0]}", color = discord.Color.red())
    await ctx.send(embed=embed)
    print("playing\n")


@bot.command(pass_context=True, aliases=['pa', 'pau'])
async def pause(ctx):

    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        print("Music paused")
        voice.pause()
        await ctx.send("Music paused")
    else:
        print("Music not playing failed pause")
        embed = discord.Embed(title = "Music not playing failed pause", color = discord.Color.red())
        await ctx.send(embed=embed)
 
 
@bot.command(pass_context=True, aliases=['r', 'res'])
async def resume(ctx):

    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_paused():
        print("Resumed music")
        voice.resume()
        embed = discord.Embed(title = "Resumed music", color = discord.Color.red())
        await ctx.send(embed=embed)
    else:
        print("Music is not paused")
        embed = discord.Embed(title = "Music is not paused", color = discord.Color.red())
        await ctx.send(embed=embed)


@bot.command(pass_context=True, aliases=['s', 'sto'])
async def stop(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)

    queues.clear()

    queue_infile = os.path.isdir("./Queue")
    if queue_infile is True:
        shutil.rmtree("./Queue")

    if voice and voice.is_playing():
        print("Music stopped")
        voice.stop()
        embed = discord.Embed(title = "Music stopped", color = discord.Color.red())
        await ctx.send(embed=embed)
    else:
        print("No music playing failed to stop")
        embed = discord.Embed(title = "No music playing failed to stop", color = discord.Color.red())
        await ctx.send(embed=embed)


queues = {}

@bot.command(pass_context=True, aliases=['q', 'que'])
async def queue(ctx, url: str):
    Queue_infile = os.path.isdir("./Queue")
    if Queue_infile is False:
        os.mkdir("Queue")
    DIR = os.path.abspath(os.path.realpath("Queue"))
    q_num = len(os.listdir(DIR))
    q_num += 1
    add_queue = True
    while add_queue:
        if q_num in queues:
            q_num += 1
        else:
            add_queue = False
            queues[q_num] = q_num

    queue_path = os.path.abspath(os.path.realpath("Queue") + f"\song{q_num}.%(ext)s")

    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'outtmpl': queue_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print("Downloading audio now\n")
            ydl.download([url])
    except:
        print("FALLBACK: youtube-dl does not support this URL, using Spotify (This is normal if Spotify URL)")
        q_path = os.path.abspath(os.path.realpath("Queue"))
        system(f"spotdl -ff song{q_num} -f " + '"' + q_path + '"' + " -s " + url)


    embed = discord.Embed(title = "Adding song " + str(q_num) + " to the queue", color = discord.Color.red())
    await ctx.send(embed=embed)

    print("Song added to queue\n")


@bot.command(pass_context=True, aliases=['n', 'nex'])
async def next(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        print("Playing Next Song")
        voice.stop()
        embed = discord.Embed(title = "Next Song")
        await ctx.send(embed=embed)
    else:
        print("No music playing")
        embed = discord.Embed(title = "No music playing failed", color = discord.Color.red())
        await ctx.send(embed=embed)
        
    
@bot.command()
async def new(ctx, *, args = None):

    await bot.wait_until_ready()

    if args == None:
        message_content = "Please wait, we will be with you shortly!"
    
    else:
        message_content = "".join(args)

    with open("data.json") as f:
        data = json.load(f)

    ticket_number = int(data["ticket-counter"])
    ticket_number += 1

    ticket_channel = await ctx.guild.create_text_channel("ticket-{}".format(ticket_number))
    await ticket_channel.set_permissions(ctx.guild.get_role(ctx.guild.id), send_messages=False, read_messages=False)

    for role_id in data["valid-roles"]:
        role = ctx.guild.get_role(role_id)

        await ticket_channel.set_permissions(role, send_messages=True, read_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True)
    
    await ticket_channel.set_permissions(ctx.author, send_messages=True, read_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True)

    em = discord.Embed(title="New ticket from {}#{}".format(ctx.author.name, ctx.author.discriminator), description= "{}".format(message_content), color=0x00a8ff)

    await ticket_channel.send(embed=em)

    pinged_msg_content = ""
    non_mentionable_roles = []

    if data["pinged-roles"] != []:

        for role_id in data["pinged-roles"]:
            role = ctx.guild.get_role(role_id)

            pinged_msg_content += role.mention
            pinged_msg_content += " "

            if role.mentionable:
                pass
            else:
                await role.edit(mentionable=True)
                non_mentionable_roles.append(role)
        
        await ticket_channel.send(pinged_msg_content)

        for role in non_mentionable_roles:
            await role.edit(mentionable=False)
    
    data["ticket-channel-ids"].append(ticket_channel.id)

    data["ticket-counter"] = int(ticket_number)
    with open("data.json", 'w') as f:
        json.dump(data, f)
    
    created_em = discord.Embed(title="Tickets", description="Your ticket has been created at {}".format(ticket_channel.mention), color=0x00a8ff)
    
    await ctx.send(embed=created_em)

@bot.command()
async def close(ctx):
    with open('data.json') as f:
        data = json.load(f)

    if ctx.channel.id in data["ticket-channel-ids"]:

        channel_id = ctx.channel.id

        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel and message.content.lower() == "close"

        try:

            em = discord.Embed(title="Tickets", description="Are you sure you want to close this ticket? Reply with `close` if you are sure.", color=0x00a8ff)
        
            await ctx.send(embed=em)
            await bot.wait_for('message', check=check, timeout=60)
            await ctx.channel.delete()

            index = data["ticket-channel-ids"].index(channel_id)
            del data["ticket-channel-ids"][index]

            with open('data.json', 'w') as f:
                json.dump(data, f)
        
        except asyncio.TimeoutError:
            em = discord.Embed(title="Tickets", description="You have run out of time to close this ticket. Please run the command again.", color=0x00a8ff)
            await ctx.send(embed=em)

        

@bot.command()
async def addaccess(ctx, role_id=None):

    with open('data.json') as f:
        data = json.load(f)
    
    valid_user = False

    for role_id in data["verified-roles"]:
        try:
            if ctx.guild.get_role(role_id) in ctx.author.roles:
                valid_user = True
        except:
            pass
    
    if valid_user or ctx.author.guild_permissions.administrator:
        role_id = int(role_id)

        if role_id not in data["valid-roles"]:

            try:
                role = ctx.guild.get_role(role_id)

                with open("data.json") as f:
                    data = json.load(f)

                data["valid-roles"].append(role_id)

                with open('data.json', 'w') as f:
                    json.dump(data, f)
                
                em = discord.Embed(title="Tickets", description="You have successfully added `{}` to the list of roles with access to tickets.".format(role.name), color=0x00a8ff)

                await ctx.send(embed=em)

            except:
                em = discord.Embed(title="Tickets", description="That isn't a valid role ID. Please try again with a valid role ID.")
                await ctx.send(embed=em)
        
        else:
            em = discord.Embed(title="Tickets", description="That role already has access to tickets!", color=0x00a8ff)
            await ctx.send(embed=em)
    
    else:
        em = discord.Embed(title="Tickets", description="Sorry, you don't have permission to run that command.", color=0x00a8ff)
        await ctx.send(embed=em)

@bot.command()
async def delaccess(ctx, role_id=None):
    with open('data.json') as f:
        data = json.load(f)
    
    valid_user = False

    for role_id in data["verified-roles"]:
        try:
            if ctx.guild.get_role(role_id) in ctx.author.roles:
                valid_user = True
        except:
            pass

    if valid_user or ctx.author.guild_permissions.administrator:

        try:
            role_id = int(role_id)
            role = ctx.guild.get_role(role_id)

            with open("data.json") as f:
                data = json.load(f)

            valid_roles = data["valid-roles"]

            if role_id in valid_roles:
                index = valid_roles.index(role_id)

                del valid_roles[index]

                data["valid-roles"] = valid_roles

                with open('data.json', 'w') as f:
                    json.dump(data, f)

                em = discord.Embed(title="Tickets", description="You have successfully removed `{}` from the list of roles with access to tickets.".format(role.name), color=0x00a8ff)

                await ctx.send(embed=em)
            
            else:
                
                em = discord.Embed(title="Tickets", description="That role already doesn't have access to tickets!", color=0x00a8ff)
                await ctx.send(embed=em)

        except:
            em = discord.Embed(title="Tickets", description="That isn't a valid role ID. Please try again with a valid role ID.")
            await ctx.send(embed=em)
    
    else:
        em = discord.Embed(title="Tickets", description="Sorry, you don't have permission to run that command.", color=0x00a8ff)
        await ctx.send(embed=em)

@bot.command()
async def addpingedrole(ctx, role_id=None):

    with open('data.json') as f:
        data = json.load(f)
    
    valid_user = False

    for role_id in data["verified-roles"]:
        try:
            if ctx.guild.get_role(role_id) in ctx.author.roles:
                valid_user = True
        except:
            pass
    
    if valid_user or ctx.author.guild_permissions.administrator:

        role_id = int(role_id)

        if role_id not in data["pinged-roles"]:

            try:
                role = ctx.guild.get_role(role_id)

                with open("data.json") as f:
                    data = json.load(f)

                data["pinged-roles"].append(role_id)

                with open('data.json', 'w') as f:
                    json.dump(data, f)

                em = discord.Embed(title="Tickets", description="You have successfully added `{}` to the list of roles that get pinged when new tickets are created!".format(role.name), color=0x00a8ff)

                await ctx.send(embed=em)

            except:
                em = discord.Embed(title="Tickets", description="That isn't a valid role ID. Please try again with a valid role ID.")
                await ctx.send(embed=em)
            
        else:
            em = discord.Embed(title="Tickets", description="That role already receives pings when tickets are created.", color=0x00a8ff)
            await ctx.send(embed=em)
    
    else:
        em = discord.Embed(title="Tickets", description="Sorry, you don't have permission to run that command.", color=0x00a8ff)
        await ctx.send(embed=em)

@bot.command()
async def delpingedrole(ctx, role_id=None):

    with open('data.json') as f:
        data = json.load(f)
    
    valid_user = False

    for role_id in data["verified-roles"]:
        try:
            if ctx.guild.get_role(role_id) in ctx.author.roles:
                valid_user = True
        except:
            pass
    
    if valid_user or ctx.author.guild_permissions.administrator:

        try:
            role_id = int(role_id)
            role = ctx.guild.get_role(role_id)

            with open("data.json") as f:
                data = json.load(f)

            pinged_roles = data["pinged-roles"]

            if role_id in pinged_roles:
                index = pinged_roles.index(role_id)

                del pinged_roles[index]

                data["pinged-roles"] = pinged_roles

                with open('data.json', 'w') as f:
                    json.dump(data, f)

                em = discord.Embed(title="Tickets", description="You have successfully removed `{}` from the list of roles that get pinged when new tickets are created.".format(role.name), color=0x00a8ff)
                await ctx.send(embed=em)
            
            else:
                em = discord.Embed(title="Tickets", description="That role already isn't getting pinged when new tickets are created!", color=0x00a8ff)
                await ctx.send(embed=em)

        except:
            em = discord.Embed(title="Tickets", description="That isn't a valid role ID. Please try again with a valid role ID.")
            await ctx.send(embed=em)
    
    else:
        em = discord.Embed(title="Tickets", description="Sorry, you don't have permission to run that command.", color=0x00a8ff)
        await ctx.send(embed=em)


@bot.command()
@has_permissions(administrator=True)
async def addadminrole(ctx, role_id=None):

    try:
        role_id = int(role_id)
        role = ctx.guild.get_role(role_id)

        with open("data.json") as f:
            data = json.load(f)

        data["verified-roles"].append(role_id)

        with open('data.json', 'w') as f:
            json.dump(data, f)
        
        em = discord.Embed(title="Tickets", description="You have successfully added `{}` to the list of roles that can run admin-level commands!".format(role.name), color=0x00a8ff)
        await ctx.send(embed=em)

    except:
        em = discord.Embed(title="Tickets", description="That isn't a valid role ID. Please try again with a valid role ID.")
        await ctx.send(embed=em)

@bot.command()
@has_permissions(administrator=True)
async def deladminrole(ctx, role_id=None):
    try:
        role_id = int(role_id)
        role = ctx.guild.get_role(role_id)

        with open("data.json") as f:
            data = json.load(f)

        admin_roles = data["verified-roles"]

        if role_id in admin_roles:
            index = admin_roles.index(role_id)

            del admin_roles[index]

            data["verified-roles"] = admin_roles

            with open('data.json', 'w') as f:
                json.dump(data, f)
            
            em = discord.Embed(title="Tickets", description="You have successfully removed `{}` from the list of roles that get pinged when new tickets are created.".format(role.name), color=0x00a8ff)

            await ctx.send(embed=em)
        
        else:
            em = discord.Embed(title="Tickets", description="That role isn't getting pinged when new tickets are created!", color=0x00a8ff)
            await ctx.send(embed=em)

    except:
        em = discord.Embed(title="Tickets", description="That isn't a valid role ID. Please try again with a valid role ID.")
        await ctx.send(embed=em)

bot.run(TOKEN)