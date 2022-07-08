import discord
import config
import json
import random
import math
from discord.utils import asyncio, get
from discord.ext import tasks , commands
from github import Github

intents = discord.Intents.default()
intents.members = True

bot = discord.Bot(intents=intents)
g = Github(config.GITHUB_TOKEN)           

@commands.has_any_role(*config.MODERATOR_ROLE_NAME)
@bot.slash_command(name="start",description="To start the competition, enter the number of rounds and the number of people who will win",guild_ids=[config.GUILD_ID])
async def start(ctx , numbers_of_raund:discord.Option(int,"Please select the number of rounds to be played"), final:discord.Option(int,"Please select the number of people who will win")):
    
    guild = ctx.guild 
    roles = guild.roles
    roles = [role.name for role in roles]  ## Roles loop 

    channel_list = guild.text_channels
    channel_list = [cha.name for cha in channel_list] ## channel list loop     

    category_list = guild.categories
    category_list = [catego.name for catego in category_list]  ## category loop

    if "Scavenger Hunt" in category_list :  ## if category Scavenger Hunt is available pass

        pass

    else :  ## if category x is don't available create ("Scavenger Hunt") category

        await guild.create_category("Scavenger Hunt")    ## create function

    if "🕵Scavenger-Hunt-Event".lower() in channel_list : ## if channel "🕵Scavenger-Hunt-Event" is available , pass

        channel = get(guild.channels, name="🕵scavenger-hunt-event")  ## get channel "🕵Scavenger-Hunt-Event" info

    else :  ## if channel "🕵Scavenger-Hunt-Event" is don't available , create text_channel = "🕵Scavenger-Hunt-Event" and write the id in the "config.py"

        category = get(guild.categories, name="Scavenger Hunt")
        event_channel_ = await guild.create_text_channel( f'🕵Scavenger-Hunt-Event', overwrites=None ,category=category) ## create text_channel
        channel = bot.get_channel(event_channel_.id)
        ekleme = channel.id
        acilmayacak = open("config.py","a+").write(f"\nEVENT_CHANNEL_ID = {ekleme}") ## write the id in the "config.py" // EVENT_CHANNEL_ID = 1234..

    for zr in range(1,numbers_of_raund+1) :

        if f"EventRound-{zr}" in roles : ## if channel "EventRound-2" in roles , pass

            pass

        else :  ## else , create "EventRound-2" role , the color is fixed for this role but random for other roles 

            guild = ctx.guild
            await guild.create_role(name=f"EventRound-{zr}",colour=discord.Colour(0x00FFFF))   

    await ctx.respond("Please wait .." , ephemeral=True)

    check_baslangic_ = open("discord_1.json","r").read()        ## read the "discord_1.json" file 
    data_baslangic = json.loads(check_baslangic_)               ## here the json read operation is performed
    rand_baslangic = data_baslangic['story']                    ## filtering is performed
    randP_baslangic = random.sample(list(rand_baslangic),k=numbers_of_raund)    

    sta_file = open("wl-address.json","r")
    json_sta = json.load(sta_file)
    sta_file.close()

    json_sta["status_and_numb"][0] = "true"
    json_sta["status_and_numb"][1] = f"{numbers_of_raund}"
    json_sta["status_and_numb"][2] = f"{final}"

    for element in json_sta["quests"] :

        json_sta["quests"].remove(element)
        sta_file = open("wl-address.json","w")
        json.dump(json_sta, sta_file ,indent=4)
        sta_file.close()        

    json_sta["quests"] = randP_baslangic
    sta_file = open("wl-address.json","w")
    json.dump(json_sta, sta_file ,indent=4)
    sta_file.close()

    sta_file = open("wl-address.json","r")
    json_sta = json.load(sta_file)
    sta_file.close()
    oku = json_sta["quests"][0]["question_info"]

    for guild in bot.guilds:

        for member in guild.members:

            role_event_1 = get(guild.roles,name="EventRound-1")
            await member.add_roles(role_event_1,atomic=True)  

    embed = discord.Embed(title="The competition has started !",description=f"A person who knows the correct answer goes to the next round and a total of {numbers_of_raund} rounds are played.",color=0x97ffff)
    embed.add_field(name="First question :",value=f"{oku}",inline=True)
    await ctx.send(embed=embed)

    myLoop.start()

@bot.slash_command(guild_ids=[config.GUILD_ID])
async def answer(ctx,answer:str):

    a = open("wl-address.json","r").read()
    aa = json.loads(a)

    if aa['status_and_numb'][0] == "true" :

        guild = ctx.guild 
        cont = ctx.author

        for z in range(1,(int(aa['status_and_numb'][1])+1)):

                if answer.lower() == aa["quests"][z-1]["answer_"] and f"EventRound-{z}" in [y.name for y in cont.roles] : 

                    if z+1 == int(aa['status_and_numb'][1]) :

                        role_1 = get(guild.roles,name="Whitelist !")
                        memb = ctx.author
                        role_2 = get(guild.roles, name=f"EventRound-{z}")
                        await memb.add_roles(role_1 , atomic=True)
                        await memb.remove_roles(role_2 , atomic=True)

                        a_file = open("wl-address.json", "r")
                        json_object = json.load(a_file)
                        a_file.close()

                        json_object["Whitelist_members"].append(f"{memb}")

                        a_file = open("wl-address.json", "w")
                        json.dump(json_object, a_file,indent=4)
                        a_file.close()
                        await ctx.respond("Congratulations ! Now you have the role of `Whitelist !`" , ephemeral=True)
                        await ctx.channel.send(f"Congratulations {ctx.author.mention} !")

                    else :

                        nexta = aa["quests"][z]["question_info"]

                        role_1_1 = get(guild.roles, name=f"EventRound-{z+1}")
                        memb = ctx.author
                        await memb.add_roles(role_1_1 , atomic=True)

                        role_2_2 = get(guild.roles, name=f"EventRound-{z}")
                        await memb.remove_roles(role_2_2 , atomic=True)
                        await ctx.respond(f"Next question : {nexta}" ,ephemeral=True)

                    break

                elif answer.lower() != aa["quests"][z-1]["answer_"] and f"EventRound-{z}" in [y.name for y in cont.roles] :

                        await ctx.respond("Wrong answer !" , ephemeral=True)

                        break

                else :pass

    else :

        await ctx.respond("The competition has not started yet" , ephemeral=True)

@tasks.loop(seconds = 1)
async def myLoop():

    tek = open("wl-address.json","r")
    ope = json.load(tek)
    tek.close()

    if int(ope["status_and_numb"][2]) == len(ope["Whitelist_members"]) :

        for elements in ope["Whitelist_members"] :

            ope["Whitelist_members"].remove(elements)
            tek = open("wl-address.json","w")
            json.dump(ope , tek , indent=4)
    
        tek.close()

        for guild in bot.guilds:

            for member in guild.members:

                role_event_1 = get(guild.roles,name="EventRound-1")
                await member.remove_roles(role_event_1,atomic=True)
        
        loop_file = open("wl-address.json","r")
        json_loop = json.load(loop_file)
        loop_file.close()

        json_loop["status_and_numb"][0] = "false"

        loop_file_ = open("wl-address.json","w")
        json.dump(json_loop,loop_file_ ,indent=4)
        loop_file_.close()

        myLoop.stop()

    else :

        pass    

@commands.has_any_role(*config.MODERATOR_ROLE_NAME)
@bot.slash_command(name="add_question",description="To add a question; add a question and an answer",guild_ids=[config.GUILD_ID])
async def add_question(ctx, question:discord.Option(str,"Please enter the question") , answer:discord.Option(str,"Please enter the answer")):

    def read_json(filename):  ## read file function
        with open(filename, 'r') as f:
            return json.load(f)

    def write_json(filename, data): ## write file function
        with open(filename, 'w') as f:
            json.dump(data, f ,indent=4) ## 

    file1 = open("discord_1.json").read() ## read file
    conv = json.loads(file1)
    convert = str(conv["story"][-1]["id"])  
    data = read_json('discord_1.json')
    data['story'].append({"id":f"{int(convert)+1}","question_info":f"{question}","answer_":f"{answer}"})
    write_json('discord_1.json', data)
    await ctx.respond("Checkk ✅",ephemeral=True)

    repo = g.get_user().get_repo("calisma") ## get repo
    content = open("discord_1.json").read()  ## read "discord_1.json" file
    contents = repo.get_contents("discord1.json") ## get Github "discord1.json" json file
    repo.update_file(contents.path, "committing files", content, contents.sha, branch="main") ## update 

@bot.event
async def on_ready():
    print("Bot is ready ! ! !")
    
bot.run(config.TOKEN)
