import discord
import urllib.request, json
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

        with urllib.request.urlopen('https://api.wynncraft.com/public_api.php?action=guildStats&command=Spectral%20Cabbage') as url:
            data = json.loads(url.read().decode())
            embed = discord.Embed(title=f'**SPC** Members', description=f'*Play time tracker*',color=3903947)
            if members := data.get('members'):
                for member in members:
                    nick = member.get('name')
                    embed.add_field(name=f'{nick}', value=f'{nick}')
            else: 
                await ctx.send('tg')
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(MembersCog(bot))
