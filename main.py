import discord
from discord.ext import commands
import config
from discord.utils import get

client = commands.Bot(command_prefix=".")

@client.command()
async def make(ctx , role_ , member_ : discord.Member):
    guild = ctx.guild
    member = ctx.author
    category = get(guild.categories, 
    name=config.CATEGORY_NAME)
    admin_role = get(guild.roles, name=config.MODERATOR_ROLE_NAME)
    new = await guild.create_role(name=f"{role_}",colour=discord.Colour(0x1889C1))
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        member: discord.PermissionOverwrite(read_messages=True),
        admin_role: discord.PermissionOverwrite(read_messages=True),
        new : discord.PermissionOverwrite(read_messages=True)
    }
    await member_.add_roles(new)
    await guild.create_text_channel(f'{member_}-Event', overwrites=overwrites , category=category)

@client.command()
async def delete(ctx,delete_):
    role_object = discord.utils.get(ctx.message.guild.roles, name=delete_)
    await role_object.delete()

@client.command()
async def event_hunt(ctx):
    await ctx.send("he")













@client.event
async def on_ready():
    print("Bot is ready ! ! !")


client.run(config.TOKEN)    
