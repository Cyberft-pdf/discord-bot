import discord
from discord.ext import commands
import requests
import datetime
import asyncio


intents = discord.Intents.default()
intents.members = True # Enable the privileged Gateway Intents
intents.messages = True
intents.guilds = True
intents.message_content = True
client = discord.Client(intents=intents)
client = commands.Bot(command_prefix='!', intents=intents)
rocket_launch_api_url = 'https://api.spacexdata.com/v3/launches/upcoming'


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
print("test2")

#code made by cyberft-pdf on github

async def check_launch():
    while True:
        url = 'https://api.spacexdata.com/v4/launches/next'
        response = requests.get(url)
        if response.status_code == 200:
            launch = response.json()
            launch_date = datetime.datetime.strptime(launch['date_utc'], '%Y-%m-%dT%H:%M:%S.%fZ')
            now = datetime.datetime.utcnow()
            countdown = launch_date - now
            if countdown < datetime.timedelta(minutes=5):
                message = f"Start mise {launch['name']} začne za {countdown.total_seconds()} sekund!"
                await client.get_channel(1107756591572336782).send(message)
        await asyncio.sleep(60)



@client.command()
async def ping(ctx):
    await ctx.send("Pong!")

@client.event
async def on_message(message):
    if message.content.startswith('!launch'):
        launches = get_upcoming_launches()
        if launches:
            await send_launches(launches, message.channel)
        else:
            await message.channel.send('Žádný start nebyl nalezen.')
#code made by cyberft-pdf on github:)

def get_upcoming_launches():
    response = requests.get(rocket_launch_api_url)
    if response.status_code == 200:
        launches = response.json()
        return launches
    else:
        return None


async def send_launches(launches, channel):
    for launch in launches:
        await channel.send(f'Start rakety je naplánován na {launch["launch_date_utc"]} - {launch["mission_name"]}')


client.run("")
