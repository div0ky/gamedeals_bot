import asyncio
import logging
import traceback

import discord

import config
from app.bot_helper import BotHelper

logging.basicConfig(level=logging.INFO)

class GameDealsClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = BotHelper()
        self.channel = self.get_channel(config.DISCORD_CHANNEL_ID)
        self.post_things = None

    async def on_ready(self) -> None:
        """
        Print to console when we've logged in and are ready.
        Start up the task to check for deals every 15min.
        :return: Nothing
        """
        print(f"Logged in as {self.user}.")
        self.post_things = self.loop.create_task(self.post_new_deals())

    async def on_message(self, message: discord.message) -> None:
        """
        Instead of using the commands extension, just monitor for messages and respond accordingly.
        :param message: <str> Message from a user
        :return: Nothing
        """
        # If a user sends a message with the defined prefix + 'info'
        if message.content == config.DISCORD_PREFIX + "info":
            description = "DivDeals is a Reddit scraping bot that alerts you of FREE game deals."
            embed = discord.Embed(title=f'{config.DISCORD_BOT_NAME} Info', description=description, color=0x2df228) \
                .add_field(name='Developed by', value='[div0ky](https://github.com/div0ky)') \
                # .add_field(name='Source', value='[Github](https://github.com/div0ky)')
            await message.channel.send(embed=embed)
            await message.delete()
        # If a user sends a message with the defined prefix + 'help'
        elif message.content == config.DISCORD_PREFIX + "help":
            embed = discord.Embed(title='DivDeals Commands', colour=0x2df228) \
                .add_field(name='d.info', value='Display bot information.', inline=False) \
                .add_field(name='d.help', value='Display the commands menu.', inline=False) \
                .add_field(name='d.refresh', value='Force a manual refresh of deals.')
            await message.channel.send(embed=embed)
            await message.delete()
        # If a user sends a message with the defined prefix + 'refresh'
        # Kill the gamedeals method and reload it. Then DM the user that requested it letting them know we heard them.
        elif message.content == config.DISCORD_PREFIX + "refresh":
            self.post_things.cancel()
            self.post_things = self.loop.create_task(self.post_new_deals())
            await message.author.send("Manual Refresh Initiated.")
            await message.delete()

    # async def on_error(event, *args, **kwargs):
    #     message = args[0]
    #     logging.warning(traceback.format_exc())

    async def post_new_deals(self):

        while not self.is_closed():
            await self.wait_until_ready()
            # Triggers a fresh scrape which will update the database with any new deals
            await self.helper.update_database()
            # Obtain a list of all deals from the database that are not tagged as 'posted'
            new_deals = self.helper.get_unannounced_deals()
            # If we have new deals, let's generate an embed and post them
            if new_deals:
                for n in new_deals:
                    print(n.title)
                embed = discord.Embed(title='PSA: FREE Stuff', description='I found some new FREE stuff on [/r/GameDeals](https://www.reddit.com/r/GameDeals/)', color=0x2df228)
                for deal in new_deals:
                    embed.add_field(name=deal.title, value=deal.url, inline=False)
                    deal.posted = True
                    deal.save()

                # Required the channel id from Discord that you want the notifications posted to
                channel = self.get_channel(704524926027300874)
                await channel.send(embed=embed)

            # Sleep for 15min and check again
            await asyncio.sleep(900)

def main():
    client = GameDealsClient()
    client.run(config.DISCORD_TOKEN)

if __name__ == "__main__":
    main()