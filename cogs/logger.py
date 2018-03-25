import discord


class Logger:
    def __init__(self, bot):
        self.bot = bot
        self.edit_chan = bot.get_channel(413889551740960790)
        self.del_chan = bot.get_channel(427178643983433740)
        self.colors = {
            "edit": discord.Color.teal(),
            "delete": discord.Color.dark_red()
        }

    async def log_message(self, action, message, new_msg=None):
        f = None
        if message.author.bot:
            return
        embed = discord.Embed(title="Message " + action, description=f"", color=self.colors[action])
        embed.set_author(name=message.author.name, icon_url=message.author.avatar_url)
        embed.add_field(name="Channel", value=message.channel.mention)
        if message.content:
            embed.add_field(name="Content", value=message.content, inline=False)
        if action == "edit":
            embed.add_field(name="Edited Content", value=new_msg.content, inline=False)

        channel = self.edit_chan if action == "edit" else self.del_chan
        await channel.send("\n".join(a.url for a in message.attachments), embed=embed, file=f)  # we have to just output the attachments  # noqa

    async def on_message_delete(self, message):
        if message.author.bot:
            return
        if message.guild == self.edit_chan.guild:
            await self.log_message("delete", message)

    async def on_message_edit(self, old, new):
        if old.author.bot:
            return
        if old.content != new.content:
            if old.guild == self.del_chan.guild:
                await self.log_message("edit", old, new)


def setup(bot):
    bot.add_cog(Logger(bot))
