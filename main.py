#Importing required dependencies
import discord
from discord.ext import commands

import json

client = commands.Bot(command_prefix='!', intents=discord.Intents.all())

#imports Bot Token
from apikeys import *


@client.event
async def on_ready():
    print("The bot is now ready for use!")
    print("-----------------------------")


@client.command()
async def whoami(ctx):
    await ctx.send(ctx.author)


@client.command()
async def add(ctx, task):

    user = str(ctx.author)

    with open("data.json", "r") as file:
        b = json.load(file)

    print(b)

    try:
        if user in b:
            b[user].append(str(task))

            with open("data.json", "w") as file:
                json.dump(b, file)

    except KeyError:
        tasks = [str(task)]
        b[user] = tasks

    response = f"Hi {ctx.author}, I've added '{task}' to your list of tasks."
    await ctx.send(response)


@add.error
async def add_error(ctx, error):
    await ctx.send("You must enter a task after *add* command...")


@client.command()
async def show(ctx):
    user = str(ctx.author)
    response = ""

    with open("data.json", "r") as file:
        b = json.load(file)

    try:
        if b[user]:
            list_of_tasks = b[user]

            i = 0
            while i < len(list_of_tasks):
                response += f"{i + 1}. {list_of_tasks[i]}\n"
                i += 1

    except KeyError:
        response = f"You have not added any tasks yet {ctx.author}"
    await ctx.send(response)


@show.error
async def show_error(ctx, error):
    print({error})
    await ctx.send(f"You dont seem to have a task list {ctx.author}.")


@client.command()
async def done(ctx, arg):
    user = str(ctx.author)
    task_number = int(arg)
    response = ""

    with open("data.json", "r") as file:
        b = json.load(file)

    task_list = b[user]

    index = task_number - 1

    i = 0
    while i < len(task_list):
        if i != index:
            response += f"{i + 1}. {task_list[i]}\n"
            i += 1

        else:
            response += f"~~{i + 1}. {task_list[i]}~~"
            i += 1

    task_list.pop(index)

    with open("data.json", "w") as file:
        json.dump(b, file)

    await ctx.send(response)


@done.error
async def done_error(ctx, error):
    await ctx.send("You must enter a number after the *done* command...")


@client.command()
async def hello(ctx):
    await ctx.send(f"*Hello , I am the bot*")


@client.command()
async def bye(ctx):
    await ctx.send("Goodbye!")

client.run(BOTTOKEN)
