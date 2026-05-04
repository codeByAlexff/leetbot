from discord.ext import commands
import discord
from leetcode import leetProblem
from leetcode import leetUser
from leetcode import randomProblem
from leetcode import dailyProblem
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("API_KEY")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="leetcode ", intents=intents, help_command=None)

last_slug = None

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged on as {bot.user}")

@bot.hybrid_command(name="problem", description="Fetch a specific problem based on its name (e.g. two-sum)")
async def problem(ctx, problem_name: str):
    await ctx.defer()
    global last_slug
    last_slug = problem_name
    question_id, title, difficulty, clean_question, _ = leetProblem(problem_name)
    embed = discord.Embed(
        title=f"#{question_id} - {title} - ({difficulty})"[:256],
        description=f"```\n{clean_question}\n```",
        color=0xFFA500
    )
    await ctx.send(embed=embed)

@bot.hybrid_command(name="link", description="Get the leetcode link for the last fetched problem")
async def link(ctx):
    await ctx.defer()
    if last_slug is None:
        await ctx.send("No problem has been fetched")
        return
    await ctx.send(f"https://leetcode.com/problems/{last_slug}")

@bot.hybrid_command(name="hint", description="Get hints for the last fetched problem")
async def hint(ctx):
    await ctx.defer()
    if last_slug is None:
        await ctx.send("No problem has been fetched")
        return
    _, _, _, _, hints = leetProblem(last_slug)
    embed = discord.Embed(
        title=f"Hint:",
        description=f"{hints}",
        color=0xFFA500
    )
    await ctx.send(embed=embed)

@bot.hybrid_command(name="help", description="List all commands")
async def help_command(ctx):
    await ctx.defer()
    embed = discord.Embed(
        title=f"LeetBot Commands:",
        color=0xFFA500
        )
    embed.add_field(name="/problem problem-name", value="Get a specific problem", inline=False)
    embed.add_field(name="/random", value="Get a random problem", inline=False)
    embed.add_field(name="/random difficulty", value="Get a random problem by difficulty (easy, medium, hard)", inline=False)
    embed.add_field(name="/daily", value="Get today's daily problem", inline=False)
    embed.add_field(name="/user username", value="Get a user's profile", inline=False)
    embed.add_field(name="/link", value="Get the link of last fetched problem", inline=False)
    embed.add_field(name="/hint", value="Get a hint for the last fetched problem", inline=False)
    await ctx.send(embed=embed)

@bot.hybrid_command(name="user", description="Lookup a user's Leetcode information")
async def user(ctx, name: str):
    await ctx.defer()
    username, avatar, ranking, github, about = leetUser(name)
    embed = discord.Embed(
                    title=f"{username} - ({ranking})"[:256],
                    description=f"{github}\b{about}",
                    color=0xFFA500
                )
    embed.set_thumbnail(url=avatar)
    await ctx.send(embed=embed)

@bot.hybrid_command(name="daily", description="Fetch the daily problem")
async def daily(ctx):
    await ctx.defer()
    global last_slug
    title, dailyDate, question_id, difficulty, clean_question, slug = dailyProblem()
    last_slug = slug
    embed = discord.Embed(
                    title=f"{dailyDate} - #{question_id} - {title} - ({difficulty})"[:256],
                    description=f"```\n{clean_question}\n```",
                    color=0xFFA500
                )
    await ctx.send(embed=embed)

@bot.hybrid_command(name="random", description="Fetch a random problem. Includes a difficulty filter")
async def random_problem(ctx, difficulty: str = None):
    await ctx.defer()
    global last_slug
    randomQuestion = randomProblem(difficulty)
    last_slug = randomQuestion["titleSlug"]
    question_id, title, diff, clean_question, _ = leetProblem(randomQuestion["titleSlug"])
    if question_id is None:
        randomQuestion = randomProblem(difficulty)
        last_slug = randomQuestion["titleSlug"]
        question_id, title, diff, clean_question, _ = leetProblem(randomQuestion["titleSlug"])
    embed = discord.Embed(
        title=f"#{question_id} - {title} - ({diff})"[:256],
        description=f"```\n{clean_question}\n```",
        color=0xFFA500
    )
    await ctx.send(embed=embed)

@bot.event
async def on_command_error(ctx, error):
    await ctx.send(f"Error: {error}")
    #if isinstance(error, commands.CommandNotFound):
        #await ctx.send("Command not found. Type `leetcode help` or `/help` for a list of commands.")

bot.run(api_key)