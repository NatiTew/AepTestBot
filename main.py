import requests
import json
import discord
import os
import pymongo
import pymongo.errors
from os import system
from keepAlive import keep_alive
from datetime import datetime
from time import sleep
from discord.ext import commands
from pymongo import MongoClient
from discord.ext.commands import has_permissions, MissingPermissions

def list_Huu(wallet:str):
  url = "https://api-v2-mainnet.paras.id/token/"

  querystring = {"collection_id":"peoplehuuyaowknow-by-huuyaownear","__limit":"100","owner_id":wallet}
  
  payload = ""
  response = requests.request("GET", url, data=payload, params=querystring)
  arr = response.json()
  
  # jtest = json.dumps(arr, indent=4)
  
  loopCount = arr["data"]["results"]

  text = ""
  for i in loopCount:
    text = text + i["metadata"]["title"] + "\n" 
  
  # arr1 = arr["data"]["results"][0]["metadata"]["title"]
  # arr2 = arr["data"]["count"]
  # arr2 = arr1["results"]
  
  # print(arr2[0]["metadata"]["title"])
  return text

def list_douby(wallet:str):
  url = "https://api-v2-mainnet.paras.id/token/"

  querystring = {"collection_id":"doubutzu-style-by-feraniznear","__limit":"100","owner_id":wallet}
  
  payload = ""
  response = requests.request("GET", url, data=payload, params=querystring)
  arr = response.json()
  
  # jtest = json.dumps(arr, indent=4)
  
  loopCount = arr["data"]["results"]

  text = ""
  for i in loopCount:
    text = text + i["metadata"]["title"] + "\n" 
  
  # arr1 = arr["data"]["results"][0]["metadata"]["title"]
  # arr2 = arr["data"]["count"]
  # arr2 = arr1["results"]
  
  # print(arr2[0]["metadata"]["title"])
  return text

def updateLog(text:str):
  now = datetime.now()
  date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
  f = open("Log.txt", "a")
  f.write(date_time + " | " + text + "\n")
  f.close()


server_ids = [952942108589834282]
token = os.environ['token']

id = 0

bot = discord.Bot()

password = os.environ["MongoDB password"]
mongodb = os.environ['mongodb']

client = pymongo.MongoClient(f"mongodb+srv://{mongodb}:{password}@aepmong0.uc53nzo.mongodb.net/?retryWrites=true&w=majority")
# db = client.test


# client = pymongo.MongoClient(f"mongodb+srv://Test:{password}@cluster0.hbuueev.mongodb.net/?retryWrites=true&w=majority")
db = client.warns
coll = db.serverwarns

@bot.event
async def on_ready():
  updateLog('System Starting...')
  print(f'Successfully logged in as {bot.user}')
  print("I am online")

@bot.slash_command(guild_ids = server_ids, name="check_paras", description = "Check Your NFT Paras.")
async def check_paras(ctx, wallet:discord.Option(str, description="Your Near Wallet ")):
  listname = list_Huu(wallet)
  embed = discord.Embed(
   title= f"Your NFT in {wallet} :",
   description= f"{listname}",
   color = discord.Color.random()
   )
  await ctx.respond(embed=embed)

@bot.slash_command(guild_ids = server_ids, name="check_douby", description = "Check Your NFT Paras.")
async def check_douby(ctx, wallet:discord.Option(str, description="Your Near Wallet ")):
  listname = list_douby(wallet)
  embed = discord.Embed(
   title= f"Your NFT in {wallet} :",
   description= f"{listname}",
   color = discord.Color.random()
   )
  await ctx.respond(embed=embed)

@bot.slash_command(guild_ids = server_ids, name="warn", description = "Warn a user.")
async def warn(ctx, user:discord.Option(discord.Member, description="What user do you want to warn?"), reason:discord.Option(str)):
  if ctx.author.guild_permissions.manage_guild:
    embed = discord.Embed(
     title= "You were warned",
     description= f"{ctx.author.mention} warned {user.mention} \n Reason: {reason}",
      color = discord.Color.random()
      )
    try:
      coll.insert_one({"_id":{"guild":user.guild.id, "user_id":user.id}, "count":1})
    except pymongo.errors.DuplicateKeyError:
      coll.update_one({"_id":{"guild":user.guild.id, "user_id":user.id}}, {"$inc":{"count":1}})
    await ctx.respond(embed=embed)
    
  else:
    await ctx.respond("You don't have permission to do that!", ephemeral = True)
    
@bot.slash_command(guild_ids = server_ids, name="warns", description="See all warns")
async def warns(ctx):
  users = coll.find({})
  end_str = ""
  for user in users:
    print(ctx.guild.id, user["_id"]["guild"])
    print(ctx.guild.id, user["_id"]["user_id"])
    if user["_id"]["guild"] == ctx.guild.id:
      end_str += f"Member: <@{user['_id']['user_id']}> has {user['count']} warn(s)\n"
  embed = discord.Embed(
    title = "Server warns",
    description = end_str,
    color = discord.Color.random()
  )
  if not end_str:
    embed = discord.Embed(
      title = "This server doesn't have any warns.",
      color = discord.Color.random()
    )
  
  await ctx.respond(embed = embed)

@bot.slash_command(guild_ids = server_ids, name="removewarns", description = "Remove a user's warns")
async def removewarns(ctx, user:discord.Option(discord.Member), amount:int):
  if ctx.author.guild_permissions.manage_guild:
    if amount < 1:
      await ctx.respond("You can't do that. Amount must be greater or equal to one.",  ephemeral = True)
      return 0
    coll.update_one({"_id":{"guild":user.guild.id, "user_id":user.id}}, {"$inc":{"count":-amount}})
    if coll.find_one({"_id":{"guild":user.guild.id, "user_id":user.id}})["count"] <= 0:
      coll.delete_one({"_id":{"guild":user.guild.id, "user_id":user.id}})
    embed = discord.Embed(
      title = "Removed warn",
      description = f"Removed warn(s) for {user.mention} \n Removed {amount} warn(s)"
    )
    
    await ctx.respond(embed = embed)
  else:
    await ctx.respond("You don't have permission to do that!", ephemeral = True)
    

@bot.slash_command(guild_ids = server_ids, name = "test", description = "Amazing Command")
async def test(ctx):
  await ctx.respond("The command works.")



keep_alive()
try:
  bot.run(token)
except discord.errors.HTTPException:
  print("\n\n\nBLOCKED BY RATE LIMITS\nRESTARTING NOW\n\n\n")
  log = 'BLOCKED BY RATE LIMITS'
  updateLog(log)
  system("python restarter.py")