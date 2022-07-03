from os import close
import discord
from discord.ext import commands
import config
from discord.utils import asyncio, get
import random
import json
import math
from github import Github

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix=".", intents = intents)
g = Github(config.GITHUB_TOKEN)

@client.command()
async def add_question(ctx):

    def read_json(filename):  ## read file function
        with open(filename, 'r') as f:
            return json.load(f)

    def write_json(filename, data): ## write file function
        with open(filename, 'w') as f:
            json.dump(data, f ,indent=4) ## 

    file1 = open("discord_1.json").read() ## read file
    conv = json.loads(file1)
    convert = str(conv["story"][-1]["id"])  

    def kon(kon1):

        return(kon1.content.lower().startswith("question:"))              
        
    def kon2(kon3):

        return(kon3.content.lower().startswith("answer:"))
        
    try :
        await ctx.send(f"Please enter the question (type 'question:' before writing the question)")
        que = await client.wait_for("message" , check=kon , timeout=150)
        await ctx.send(f"Please enter the answer to question {que.content} (type 'answer:' before writing the answer)")
        an = await client.wait_for("message", check=kon2 , timeout=150)
        await ctx.send(f"{an.content}")

        data = read_json('discord_1.json')
        saye = an.content.replace("answer:","")
        data['story'].append({"id":f"{int(convert)+1}","question_info":f"{que.content}","answer_":f"{saye}"})

        write_json('discord_1.json', data)
        
    except asyncio.TimeoutError :

        await ctx.send("the command is canceled . reason = timeout ")   

@client.command()
async def github(ctx): ## update github file
    repo = g.get_user().get_repo("calisma") ## get repo
    all_files = [config.FILE_PATH]
    content = open("discord_1.json").read()  ## read "discord_1.json" file
    contents = repo.get_contents("discord1.json") ## get Github "discord1.json" json file
    repo.update_file(contents.path, "committing files", content, contents.sha, branch="main") ## update 
    await ctx.send(' UPDATED') ## send update message

@client.command()
async def question_id(ctx,name:int): ## show question x
    
    file1 = open("discord_1.json").read()  ## read "discord_1.json" file
    conv = json.loads(file1)  ## convert json to json (delete spaces)
    convert = str(conv["story"][name-1]) ## convert json to string
    hel = convert.replace("{","").replace("}","").replace("'","")  ## delete characters
    ## await ctx.send(convert.replace("{","").replace("}","").replace("'",""))
    embed=discord.Embed(title=f"Question : {name}", url="https://github.com/BalyozMuzo/calisma/blob/main/discord1.json", description=f"{hel}", color=0xFF5733)
    await ctx.send(embed=embed)

@client.command()
async def start(ctx, round : int , howppl : int , _final_ : int):  ## round = number of rounds , howppl = number of people to be selected in the first round , _final_ = the number of people who will win the whitelist

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
        channel = client.get_channel(event_channel_.id)
        ekleme = channel.id
        acilmayacak = open("config.py","a+").write(f"\nEVENT_CHANNEL_ID = {ekleme}") ## write the id in the "config.py" // EVENT_CHANNEL_ID = 1234..

    if "EventRound-2" in roles : ## if channel "EventRound-2" in roles , pass

        pass

    else :  ## else , create "EventRound-2" role , the color is fixed for this role but random for other roles 

        guild = ctx.guild
        await guild.create_role(name=f"EventRound-2",colour=discord.Colour(0x00FFFF))   

    guild = ctx.guild
    engelle= get(guild.roles, name="EventRound-2")  ## get "EventRound-2" role info

    await channel.set_permissions(engelle, send_messages=False)  ## here, the role "EventRound-2" is prevented from sending messages to the channel
                                                                 
    check_baslangic_ = open("discord_1.json","r").read()        ## read the "discord_1.json" file 
    data_baslangic = json.loads(check_baslangic_)               ## here the json read operation is performed
    rand_baslangic = data_baslangic['story']                    ## filtering is performed
    randP_baslangic = random.choice(list(rand_baslangic))       ## a random question is selected from a json file
    
    await channel.send(randP_baslangic["question_info"])  ## send the question to the channel
    
    for a in range(howppl) : ## howppl = number of people to be selected in the first round

        def check_baslangic(ch1_rnd_1): ## check funtion
        
            if ch1_rnd_1.channel.id == config.EVENT_CHANNEL_ID : ## only messages sent to the event channel are considered

                return(
                
                    ch1_rnd_1.content.lower() == randP_baslangic["answer_"] ## if the answer to the question is correct, proceed to the other process

                )

            else :  ## else , pass

                pass          

        round_role_1 = get(guild.roles, name="@everyone")  ## all anyone can send a message
        await ctx.channel.set_permissions(round_role_1, send_messages=True) ## "True"
        round_role_1 = get(guild.roles, name="EventRound-2") ## the "EventRound-2" role cannot send messages to this channel
        await ctx.channel.set_permissions(round_role_1, send_messages=False) ## "False"

        try : ## the reason I use the "try" function is that if the user does not send a message  at time, it switches to the other function

            mesaj_for_1 = await client.wait_for("message" , check=check_baslangic , timeout=100) ## wait for "def chechk_baslangic" or 100 second
            await mesaj_for_1.delete()  ## delete true message
            guild_for_1 = ctx.guild
            content_for_1 = mesaj_for_1.author
            round_for_1 = get(guild_for_1.roles,name ="EventRound-2")  

            if round_for_1 in [y.name for y in content_for_1.roles] : ## if the user has the role "EventRound-2", pass

                pass

            else : ## else , give him a role and congratulate him

                await channel.send(f"Congratulations, you have passed first round {content_for_1.mention}")
                role = get(guild.roles, name="EventRound-2")
                await content_for_1.add_roles(role , atomic=True)                        

        except asyncio.TimeoutError: ## if the message does not arrive on time, kill the for loop

            break
   
    await channel.send("Please wait for next question !\n")     ## send message channel
    
    for r in ctx.guild.roles:  ## prevent all roles from sending messages 

        guild = ctx.guild
        rol = get(guild.roles, name=str(r.name))
        await channel.set_permissions(rol,send_messages=False)

    guild = ctx.guild
    admin_role = get(guild.roles, name=config.MODERATOR_ROLE_NAME) ## allow moderators to send messages
    await channel.set_permissions(admin_role, send_messages=True)

    liste_tut = []  ## create list
    liste_tut.append(randP_baslangic) ## add the question used to the list . In order not to encounter the same question

    for b in range(2,round+1): ## start from the second round and continue until the last round
        
        if b == round : ## final round !

            check_final_round = open("discord_1.json","r").read()      ## read the "discord_1.json" file 
            data_final_round = json.loads(check_final_round)           ## here the json read operation is performed
            rand_final_round = data_final_round['story']               ## filtering is performed
            randP_final_round = random.choice(list(rand_final_round))  ## a random question is selected from a json file

            if randP_final_round in liste_tut :  ## if the question is in the list, change it

                randP_final_round = random.choice(list(rand_final_round))
                  
            else :  ## else , pass

                pass

            if f"EventRound-{b}" in roles :  ## if the roles have "EventRound-(Rlound number)" in them, pass

                pass
            
            else : ## else , create "EventRound-(Round number)" role 

                guild = ctx.guild
                await guild.create_role(name=f"EventRound-{b}",colour=discord.Colour(random.randint(0, 16777215))) ## color = random color

            if f"Whitelist !" in roles :  ## if the roles have "Whitelist !" in them, pass

                pass
            
            else : ## else , create "Whitelist !" role

                guild = ctx.guild
                await guild.create_role(name=f"Whitelist !",colour=discord.Colour(random.randint(0, 16777215)))                  

            guild = ctx.guild
            roles = guild.roles
            roles = [role.name for role in roles]  ## roles loop 
            round_arti_bir_1 = get(guild.roles , name=f"EventRound-{b-1}") ## get "EventRound-(current round-1)" role info
            await channel.set_permissions(round_arti_bir_1, send_messages=False) ## prevent role "EventRound-(current round-1)" from sending messages
            round_role_final_ = get(guild.roles, name=f"EventRound-{b}") ## 
            await channel.set_permissions(round_role_final_, send_messages=True) ## enable users who have passed the round to send messages
            wl_role = get(guild.roles ,name="Whitelist !")
            await channel.set_permissions(wl_role, send_messages=False) ## prevent winning people from sending messages
            await channel.send(f"Welcome Final round , a total of {_final_} people will pass this round ") ## 
            ques = randP_final_round["question_info"]
            await channel.send(f"{ques}") ## question send channel

            def check_final(ch1_rnd_1): ##check function
            
                if ch1_rnd_1.channel.id == config.EVENT_CHANNEL_ID : ## only messages sent to the event channel are considered

                    return(
                    
                        ch1_rnd_1.content.lower() == randP_aradaki["answer_"] ## if the answer to the question is correct, proceed to the other process

                    )
                else : ## else , pass
                    pass  
           
            for c in range(_final_) : ## loop for wl

                try :

                    mesaj_for_3 = await client.wait_for("message" , check=check_final , timeout=100) ## wait for message or 100 second
                    guild_for_3 = ctx.guild
                    content_for_3 = mesaj_for_3.author
                    await mesaj_for_3.delete() ## delete true message
                    role_wl = get(guild_for_3.roles, name="Whitelist !")
                    await content_for_3.add_roles(role_wl , atomic=True)  ## answer the correct answers correctly
                    remove_role = get(guild_for_3.roles , name=f"EventRound-{b}")
                    await content_for_3.remove_roles(remove_role , atomic=True)  ## remove the role of "EventRound-{b}" from those who answered correctly            

                except asyncio.TimeoutError: ## if the message does not arrive on time, kill the for loop

                    break 

            guild = ctx.guild
            roles = guild.roles
            for role in roles : ## 
                engelle= get(ctx.guild.roles, name=f"{role}")
                channel = get(ctx.guild.channels, name="🕵scavenger-hunt-event")
                await channel.set_permissions(engelle, overwrite=None) ## remove all permissions from the channel (default setting)

        else :
            
            check_aradaki_ = open("discord_1.json","r").read() ## read the "discord_1.json" file 
            data_aradaki = json.loads(check_aradaki_)          ## here the json read operation is performed
            rand_aradaki = data_aradaki['story']               ## filtering is performed
            randP_aradaki = random.choice(list(rand_aradaki))  ## a random question is selected from a json file

            if randP_aradaki in liste_tut :  ## if the question is in the list, change it

                randP_aradaki = random.choice(list(rand_aradaki))
                
            else : ## else , pass

                pass        

            liste_tut.append(randP_aradaki)  ## again add element int list
            
            guild = ctx.guild
            roles = guild.roles
            roles = [role.name for role in roles] ## roles loop 

            if f"EventRound-{b}" in roles : ## if the roles have "EventRound-{b}" in them, pass

                pass
            
            else : ## else , create "EventRound-{b}" role , random color

                guild = ctx.guild
                await guild.create_role(name=f"EventRound-{b}",colour=discord.Colour(random.randint(0, 16777215))) 

            if f"EventRound-{b+1}" in roles : ## if the roles have "EventRound-{b+1}" in them, pass

                pass
            
            else : ## else , create "EventRound-{b+1}" role , random color

                guild = ctx.guild
                await guild.create_role(name=f"EventRound-{b+1}",colour=discord.Colour(random.randint(0, 16777215)))                            

            round_role = get(guild.roles, name=f"EventRound-{b}")
            await channel.set_permissions(round_role, send_messages=True)  ## allows send message permission
            round_arti_bir = get(guild.roles , name=f"EventRound-{b+1}")
            await channel.set_permissions(round_arti_bir, send_messages=False) ## blocks permission to send messages
            await channel.send(f"Welcome Round-{b} 🥳🥳 ")  ## welcome message send channel
            ques_1 = randP_aradaki["question_info"]
            await channel.send(f"{ques_1}")  ## send question

            def check_aradaki(ch1_rnd_1):
            
                if ch1_rnd_1.channel.id == config.EVENT_CHANNEL_ID :

                    return(
                    
                        ch1_rnd_1.content.lower() == randP_aradaki["answer_"]

                    )
                else :
                    pass  

            role_rnd_ara = get(guild.roles, name=f"EventRound-{b}")
            user_with_role = [m for m in guild.members if role_rnd_ara in m.roles]
            no = len(user_with_role)

            for a in range(math.ceil(no-((no-_final_)/(round-b+1)))) : ## Formula 

                try :

                    mesaj_for_2 = await client.wait_for("message" , check=check_aradaki , timeout=100)
                    guild_for_2 = ctx.guild
                    content_for_2 = mesaj_for_2.author
                    await mesaj_for_2.delete()
                    round_role_ust = get(guild_for_2.roles , name =f"EventRound-{b+1}")

                    if round_role_ust in [y.name for y in content_for_2.roles]:

                        pass

                    else :

                        await channel.send(content_for_2)
                        role_ara_ = get(guild.roles , name=f"EventRound-{b+1}")
                        await content_for_2.add_roles(role_ara_ , atomic=True)
                        role_remove = get(guild.roles , name=f"EventRound-{b}")
                        await content_for_2.remove_roles(role_remove , atomic=True)

                except asyncio.TimeoutError:

                    break         
        
def check(ch1_rnd_1):

    if ch1_rnd_1.channel.id == config.EVENT_CHANNEL_ID :
        
        return(

            ch1_rnd_1.content.lower() == "true"

        )
    else :
        pass  

def check_ara(ch1_rnd_ara):

    if ch1_rnd_ara.channel.id == config.EVENT_CHANNEL_ID :

        return(

            ch1_rnd_ara.content == "trueara"

        )
    else :

        pass    

@client.event
async def on_ready():
    print("Bot is ready ! ! !")

client.run(config.TOKEN)
