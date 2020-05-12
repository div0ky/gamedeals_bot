import asyncio
import re

import jellyfish
import praw

import config
from app.models import Deal


class BotHelper:

    def __init__(self, config=config):
        self.reddit = praw.Reddit(client_id=config.REDDIT_CLIENT_ID,
                                  client_secret=config.REDDIT_CLIENT_SECRET,
                                  password=config.REDDIT_PASSWORD,
                                  user_agent=config.REDDIT_USER_AGENT,
                                  username=config.REDDIT_USERNAME)
        self.reddit.read_only = True

    async def get_new_posts(self, num_of_deals: int = config.REDDIT_NUMBER_OF_DEALS,
                            sub_name: str = 'GameDeals') -> list:
        sub_reddit = self.reddit.subreddit(sub_name).new(limit=num_of_deals)
        game_deals = [x for x in sub_reddit]
        return game_deals

    @staticmethod
    async def deal_is_duplicate(deal):
        all_deals = Deal.select()
        for d in all_deals:
            diff = jellyfish.jaro_winkler(deal.title, d.title)
            if diff > 0.867:
                print(f"Match Found: {d.title, d.ident} with an {round(diff*100,2)}% match.")
                return True
        return False

    async def update_database(self) -> None:
        game_deals = await self.get_new_posts()
        for deal in game_deals:
            match_free = re.search(r'\bfree\b', deal.title, re.IGNORECASE)
            match_100 = re.search('100 *%', deal.title)
            if match_free or match_100:
                deal_exists = Deal.get_or_none(Deal.ident == deal.id)
                if deal_exists is None:
                    duplicate = await self.deal_is_duplicate(deal)
                    if not duplicate:
                        Deal.create(ident=deal.id, title=deal.title, url=deal.url, created=deal.created_utc, posted=False)
                        print(f"Deal {deal.title} has been added to the database.")
                else:
                    print(f"Deal <{deal.title}> is already in the database.")

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
