import discord
import urllib, json
import DiscordUtils
from math import ceil
from discord.ext import commands


class MembersCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    async def joined(self, ctx, *, member: discord.Member):
        created_at = member.created_at.strftime('%b %d, %Y')
        embed = discord.Embed(title=f'{member.display_name}', description=f'Joined **{created_at}**',color=3903947)
        await ctx.send(embed=embed)
    
    @commands.command()
    @commands.guild_only()
    async def onlinetime(self, ctx):
        processing = discord.Embed(title=f'**Processing...**',
                                   description="Please wait, I'm getting all the data you need.",
                                   color=3903947)
        processing.set_thumbnail(url="https://cdn.discordapp.com/emojis/407266065660510218.gif?v=1")
        await ctx.send(embed=processing, delete_after=2)
        paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx, remove_reactions=True)
        paginator.add_reaction('⏪', "first")
        paginator.add_reaction('◀️', "back")
        paginator.add_reaction('▶️', "next")
        paginator.add_reaction('⏩', "last")
        await paginator.run(fetch_data())

def fetch_data():
    with open("/home/nepmia/Myazu/db/db.json") as api:
        data = json.load(api)
    db = data.get("_default")
    embeds = []
    for i, elt in enumerate(db):
        user_data = db.get(elt)
        username = user_data.get("username")
        ur2 = f"https://api.wynncraft.com/v2/player/{username}/stats"
        u2 = urllib.request.urlopen(ur2)
        api_2 = json.loads(u2.read().decode())
        data2 = api_2.get("data")
        for item in data2:
            meta = item.get("meta")
            playtime = meta.get("playtime")
            play_in = user_data.get("playtime")
            play_minus = playtime - play_in
            play_mult = (play_minus * 4.7) / 60
            play_output = f"played {round(play_mult, 1)} hours"
            embeds.append(
                {
                    "username": username, 
                    "play_output": play_output, 
                })
    return embed_creator(embeds)
    
            
def chunker(seq, size):
    for i in range(0, len(seq), size):
        yield seq[i:i+size]

def embed_creator(embeds):
    pages = []
    current_page = None
    for i, chunk in enumerate(chunker(embeds, 10)):
        current_page = discord.Embed(title=f'**SPC** Last week online time',color=3903947)
        for elt in chunk:
            current_page.add_field(name=elt.get("username"), value=elt.get("play_output"), inline=False)
        current_page.set_footer(
            icon_url="https://cdn.discordapp.com/icons/513160124219523086/a_3dc65aae06b2cf7bddcb3c33d7a5ecef.gif?size=128", 
            text=f"{i + 1} / {ceil(len(embeds) / 10)}"
            )
        pages.append(current_page)
        current_page = None
    return pages


def setup(bot):
    bot.add_cog(MembersCog(bot))
