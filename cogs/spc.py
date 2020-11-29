import discord
import urllib, json
import DiscordUtils
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
        

        await ctx.send(embed=embed)

    @commands.command()
    async def paginate(self, ctx):
        embed1 = discord.Embed(color=ctx.author.color).add_field(name="Example", value="Page 1")
        embed2 = discord.Embed(color=ctx.author.color).add_field(name="Example", value="Page 2")
        embed3 = discord.Embed(color=ctx.author.color).add_field(name="Example", value="Page 3")
        paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx, remove_reactions=True)
        paginator.add_reaction('◀️', "back")
        paginator.add_reaction('▶️', "next")
        embeds = [embed1, embed2, embed3]
        await paginator.run(embeds)

def embed_creator(embed_name, embed_num, username, play_output, number):
    embed_name.add_field(name=username, 
                        value=play_output, 
                        inline=False)
    embed_name.set_footer(icon_url="https://cdn.discordapp.com/icons/513160124219523086/a_3dc65aae06b2cf7bddcb3c33d7a5ecef.gif?size=128",
                    text=f"{embed_num} / {number}")

def fecth_data(num):
    with open("/home/nepmia/Myazu/db/db.json") as api:
            data = json.load(api)
            default = data.get("_default")
            count = 0
            embed = discord.Embed(title=f'**SPC** Last week online time',
                                  color=3903947)
            for number in default:
                count += 1
                track = default.get(number)
                username = track.get("username")
                ur2 = f"https://api.wynncraft.com/v2/player/{username}/stats"
                u2 = urllib.request.urlopen(ur2)
                api_2 = json.loads(u2.read().decode())
                data2 = api_2.get("data")
                for item in data2:
                            meta = item.get("meta")
                            playtime = meta.get("playtime")
                            play_in = track.get("playtime")
                            play_minus = playtime - play_in
                            play_mult = (play_minus * 4.7) // 60
                            play_output = f"played {float(play_mult):g} hours"
                            if count > num:
                                embed_creator(embed_name=embed, embed_num=num, username=username, play_output=play_output, number=number)

def setup(bot):
    bot.add_cog(MembersCog(bot))
