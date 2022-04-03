import discord
from discord import File
from discord.ext import commands
import random
import json
import asyncio
from easy_pil import Editor, load_image_async, Font


##########################################
prefixes = "-","="
client = commands.Bot(command_prefix = prefixes)
client.remove_command("help")
TOKEN = "Tự thêm"


###########################################
@client.event
async def on_ready():
    print(f'Bot {client.user.name} đã hoạt động')
    await client.wait_until_ready()
    sta = ['Magi Natsuki', '-help[-h]',f'Với {len(client.guilds)} máy chủ']
    while not client.is_closed():
        a = random.choice(sta)
        await client.change_presence(activity=discord.Streaming(name=a, url='https://www.twitch.tv/your_channel_here'))
        await asyncio.sleep(5)

@client.event
async def on_member_join(member):
    with open('levels.json', 'r') as f:
        users = json.load(f)
    await update_data(users, member)
    with open('levels.json', 'w') as f:
        json.dump(users, f, indent=4)

@client.event
async def on_message(message):
    if message.author.bot == False:
        user = message.author
        with open('levels.json', 'r') as f:
            users = json.load(f)

        ex = random.randint(1, 2)

        await update_data(users, message.author)
        await add_experience(users, message.author, ex)
        await level_up(users, message.author, message)
        with open('levels.json', 'w') as f:
            json.dump(users, f, indent=4)

        users[str(user.id)]['exp_after'] = users[str(user.id)]['lvl'] ** 4
        with open('levels.json', 'w') as f:
            json.dump(users, f, indent=4)

        if users[str(user.id)]['exp'] >= users[str(user.id)]['exp_after']:
          users[str(user.id)]['lvl'] += 1
          with open('levels.json', 'w') as f:
            json.dump(users, f, indent=4)
        
          users[str(user.id)]['exp'] = 0
          with open('levels.json', 'w') as f:
            json.dump(users, f, indent=4)
          await message.author.send(f"{message.author.mention} đã lên level {users[str(user.id)]['lvl']}")


####################################
async def update_data(users, user):
    if not str(user.id) in users:
        users[str(user.id)] = {}
        users[str(user.id)]['exp'] = 0
        users[str(user.id)]['exp_after'] = 0
        users[str(user.id)]['lvl'] = 1

async def add_experience(users, user, exp):
    users[str(user.id)]['exp'] += exp
    with open('levels.json', 'w') as f:
        json.dump(users, f, indent=4)

async def level_up(users, user, message):
    with open('levels.json', 'r') as g:
        users = json.load(g)


###################################
@client.command()
async def rank(ctx, user: discord.Member = None):
  if user == None:
    user = ctx.author
  with open("levels.json", "r") as f:
    users = json.load(f)

  exp = users[str(user.id)]["exp"]
  exp_after = users[str(user.id)]["exp_after"]
  lvl = users[str(user.id)]["lvl"]

  xp_need = exp_after
  xp_have = users[str(user.id)]["exp"]

  percentage = int(((xp_have * 100)/ xp_need))

  if percentage < 1:
    percentage = 0
  
  background = Editor(f"E:\\lt\\bot\\eco\\img.png")
  profile = await load_image_async(str(user.avatar_url))
  profile = Editor(profile).resize((150, 150)).circle_image()

  poppins = Font.poppins(size=40)
  poppins_small = Font.poppins(size=30)

  ima = Editor("E:\\lt\\bot\\eco\\black.png")
  background.blend(image=ima, alpha=.5, on_top=False)
  background.paste(profile.image, (30, 30))

  background.rectangle((30, 220), width=650, height=40, fill="#fff", radius=20)
  background.bar(
      (30, 220),
      max_width=650,
      height=40,
      percentage=percentage,
      fill="#5b6ed6",
      radius=20,
  )

  background.text((200, 40), str(user.name), font=poppins, color="#c6cfff")
  background.rectangle((200, 100), width=350, height=2, fill="#bd87fa")
  background.text(
      (200, 130),
      f"Level : {lvl}   "
      + f" XP : {exp} / {exp_after}",
      font=poppins_small,
      color="#c6cfff",
  )
  card = File(fp=background.image_bytes, filename="card.png")
  await ctx.send(file=card)


#######################
client.run(TOKEN)