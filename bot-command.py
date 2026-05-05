from discord.ext import commands
from discord import ui
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
hint_num = 0
empty_hints = []

class DifficultySelectView(ui.View):
    def __init__(self):
        super().__init__(timeout=120)

    @ui.select(
        placeholder="Choose a difficulty...",
        options=[
            discord.SelectOption(label="Easy", value="easy"),
            discord.SelectOption(label="Medium", value="medium"),
            discord.SelectOption(label="Hard", value="hard"),
        ]
    )
    async def select_difficulty(self, interaction: discord.Interaction, select: ui.Select):
        global last_slug, empty_hints, hint_num
        await interaction.response.defer()
        randomQuestion = randomProblem(select.values[0])
        last_slug = randomQuestion["titleSlug"]
        question_id, title, diff, clean_question, _, empty_hints_result = leetProblem(randomQuestion["titleSlug"])
        if question_id is None:
            randomQuestion = randomProblem(select.values[0])
            last_slug = randomQuestion["titleSlug"]
            question_id, title, diff, clean_question, _, empty_hints_result = leetProblem(randomQuestion["titleSlug"])
        empty_hints = empty_hints_result
        hint_num = 0
        embed = discord.Embed(
            title=f"#{question_id} - {title} - ({diff})"[:256],
            description=f"```\n{clean_question}\n```",
            color=0xFFA500
        )
        await interaction.followup.send(embed=embed)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged on as {bot.user}")

@bot.hybrid_command(name="problem", description="Fetch a specific problem based on its name (e.g. two-sum)")
async def problem(ctx, problem_name: str):
    global last_slug, empty_hints, hint_num
    await ctx.defer()
    last_slug = problem_name
    question_id, title, difficulty, clean_question, _, empty_hints_result = leetProblem(problem_name)
    if question_id is None:
        await ctx.send("⚠️ Could not fetch that problem. Check the slug is correct or the API may be waking up — try again in a few seconds.")
        return
    empty_hints = empty_hints_result
    hint_num = 0
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
    global hint_num
    await ctx.defer()
    if last_slug is None:
        await ctx.send("No problem has been fetched")
        return
    if not empty_hints:
        await ctx.send("No hints available for this problem")
        return
    if hint_num >= len(empty_hints):
        await ctx.send("No more hints available")
        return
    hint = empty_hints[hint_num]
    hint_num += 1
    embed = discord.Embed(
        title=f"Hint {hint_num}/{len(empty_hints)}:",
        description=f"{hint}",
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
    global last_slug, empty_hints, hint_num
    await ctx.defer()
    result = dailyProblem()
    if result[0] is None:
        await ctx.send("⚠️ Could not fetch the daily problem. The API may be waking up — try again in a few seconds.")
        return
    title, dailyDate, question_id, difficulty, clean_question, slug = result
    last_slug = slug
    _, _, _, _, _, empty_hints_result = leetProblem(slug)
    empty_hints = empty_hints_result
    hint_num = 0
    embed = discord.Embed(
        title=f"{dailyDate} - #{question_id} - {title} - ({difficulty})"[:256],
        description=f"```\n{clean_question}\n```",
        color=0xFFA500
    )
    await ctx.send(embed=embed)

@bot.hybrid_command(name="random", description="Fetch a random problem. Includes a difficulty filter")
async def random_problem(ctx):
    view = DifficultySelectView()
    await ctx.send("**Select a difficulty:**", view=view, ephemeral=True)

@bot.event
async def on_command_error(ctx, error):
    await ctx.send(f"Error: {error}")

bot.run(api_key)