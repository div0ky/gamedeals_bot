import praw
from app.models import Deal
import config
import asyncio
import re


class BotHelper:

    def __init__(self, config=config):
        self.reddit = praw.Reddit(client_id=config.REDDIT_CLIENT_ID,
                                  client_secret=config.REDDIT_CLIENT_SECRET,
                                  password=config.REDDIT_PASSWORD,
                                  user_agent=config.REDDIT_USER_AGENT,
                                  username=config.REDDIT_USERNAME)
        self.reddit.read_only = True

    async def get_new_posts(self, num_of_deals: int = config.REDDIT_NUMBER_OF_DEALS, sub_name: str = 'GameDeals') -> list:
        sub_reddit = self.reddit.subreddit(sub_name).new(limit=num_of_deals)
        game_deals = [x for x in sub_reddit]
        return game_deals

    async def update_database(self) -> None:
        game_deals = await self.get_new_posts()
        for deal in game_deals:
            match_free = re.search(r'\bfree\b', deal.title, re.IGNORECASE)
            match_100 = re.search('100 *%', deal.title)

            if match_100 or match_free:
                deal_exists = Deal.get_or_none(Deal.ident == deal.id)
                if deal_exists is None:
                    Deal.create(ident=deal.id, title=deal.title, url=deal.url, created=deal.created_utc, posted=False)

    @staticmethod
    def get_unannounced_deals() -> list:
        to_announce = Deal.select().where(Deal.posted == False)
        return [x for x in to_announce]

    async def main(self) -> None:
        asyncio.create_task(self.update_database())
    
    def refresh(self) -> None:
        asyncio.run(self.main())

if __name__ == "__main__":
    helper = BotHelper()
