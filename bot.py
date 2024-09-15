import discord
from discord.ext import commands
import aiohttp

TOKEN = "your_token_here"
CLIENT_ID = "your_client_id_here"
GUILD_ID = "your_guild_id_here"
BOT_STATUS = "Fluxus Bypass Bot | Ibypass Made This"
EMBED_COLOR = 0x000000
FOOTER_TEXT = "footer text here"

intents = discord.Intents.default()
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"\x1b[36mSuccessfully Logged In As {bot.user.name}\x1b[0m")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=BOT_STATUS))
    
    try:
        print('\x1b[33mUpdating Commands..\x1b[0m')
        guild = discord.Object(id=GUILD_ID)

        @bot.tree.command(name="fluxus", description="Gets Fluxus Key")
        @discord.app_commands.describe(link="Fluxus Link")
        async def fluxus_command(interaction: discord.Interaction, link: str):
            if link.startswith("https://flux.li/android/external/start.php?HWID="):
                try:
                    async with aiohttp.ClientSession() as session:
                        async with session.get(f"https://api.ibypass.lol/api/fluxus?url={link}") as response:
                            json = await response.json()
                            if json['status'] == "success":
                                embed = discord.Embed(
                                    title="Fluxus Key",
                                    description=f"Key:\n```{json['key']}```\nTime Taken:\n```{json['time_taken']}```",
                                    color=EMBED_COLOR
                                )
                                embed.set_footer(text=FOOTER_TEXT)
                                await interaction.response.send_message(embed=embed)
                            elif json['status'] == "message" and json['key'] == "Invalid HWID/Invalid Fluxus Link":
                                embed = discord.Embed(
                                    title="Invalid Fluxus Link",
                                    description="The Fluxus Link You Entered Is Invalid.",
                                    color=EMBED_COLOR
                                )
                                embed.set_footer(text=FOOTER_TEXT)
                                await interaction.response.send_message(embed=embed)
                            else:
                                embed = discord.Embed(
                                    title="Error",
                                    description="Most Likely An Error With API",
                                    color=EMBED_COLOR
                                )
                                embed.set_footer(text=FOOTER_TEXT)
                                await interaction.response.send_message(embed=embed)
                except Exception as e:
                    print(e)
                    embed = discord.Embed(
                        title="Error",
                        description="Failed To Process Your Request. Try Again Later",
                        color=EMBED_COLOR
                    )
                    embed.set_footer(text=FOOTER_TEXT)
                    await interaction.response.send_message(embed=embed)
            else:
                embed = discord.Embed(
                    title="Invalid Fluxus Link",
                    description="The Link You Entered Is Not A Fluxus Link. Try Again With A Valid Fluxus Link.",
                    color=EMBED_COLOR
                )
                embed.set_footer(text=FOOTER_TEXT)
                await interaction.response.send_message(embed=embed)

        await bot.tree.sync(guild=guild)
        print(f"\x1b[32mSuccessfully Updated Commands For {guild}\x1b[0m")
    except Exception as e:
        print(f'\x1b[31m{e}\x1b[0m')

bot.run(TOKEN)
