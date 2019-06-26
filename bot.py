import discord
import time
import asyncio

messages = 0
joined = 0

def read_token():
        with open("token.txt", "r") as f:
                lines = f.readlines()
                return lines[0].strip()

def read_server_id():
        with open("server_id.txt", "r") as f:
                lines = f.readlines()
                return lines[0].strip()

token = read_token()
serverID = read_server_id()

client = discord.Client()

async def update_stats():
        await client.wait_until_ready()
        global messages, joined

        while not client.is_closed():
                try:
                        with open("stats.txt", "a") as f:
                                f.write(f"Time: {int(time.time())}, Messages: {messages}, Members Joined: {joined} \n")
                        
                        messages = 0 
                        joined = 0

                        await asyncio.sleep(5)

                except Exception as e:
                        print(e)
                        await asyncio.sleep(5)

@client.event
async def on_member_join(member):
        global joined 
        joined +=1 
        for channel in member.server.channels:
                if str(channel) == "general":
                        await client.send_message(f"""Welcome to the server {member.mention}""")

@client.event
async def on_message(message):
        global messages 
        messages +=1
        id = client.get_guild(serverID)
        channels = ["commands"]

        if str(message.channel) in channels:
                if message.content.find("!hello") != -1:
                        await message.channel.send("Hi")
                elif message.content == "!users":
                        await message.channel.send(f"""# of Members {id.member_count}""")

client.loop.create_task(update_stats)

client.run(token)
