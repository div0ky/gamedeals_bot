# GameDeals Bot
> Scrape FREE deals from r/gamedeals and post in Discord.

![GitHub tag (latest SemVer pre-release)](https://img.shields.io/github/v/tag/div0ky/gamedeals_bot?color=blue&include_prereleases&label=latest&logo=github&sort=semver)
![GitHub last commit (branch)](https://img.shields.io/github/last-commit/div0ky/gamedeals_bot/master?logo=github)
![Maintenance](https://img.shields.io/maintenance/yes/2020)
![Requires.io](https://img.shields.io/requires/github/div0ky/gamedeals_bot)
![GitHub issues](https://img.shields.io/github/issues/div0ky/gamedeals_bot)

This bot scrapes r/GameDeals on Reddit every 15min to see if any *FREE* things have been posted. It checks the title using RegEx for the words `FREE` or `100%`. If it finds those words it consders it a deal worth posting. It then checks the database (SQLite) to see if we've already saved this deal and, if not, saves it to the database.

The Discord Bot portion then queries the database for a list of all items that have not been posted, creates an embed, and posts all unannounced deals into the designated channel.

![gamedeals_bot embed](https://i.imgur.com/VIukGIJ.png)

## Setup

Clone the repo

```python
git clone https://github.com/div0ky/gamedeals_bot.git
``` 

Create a `config.py` file in the root folder with the following variables defined. Filling in your info where needed.

```python
REDDIT_CLIENT_ID = ""
REDDIT_CLIENT_SECRET = ""
REDDIT_PASSWORD = ""
REDDIT_USER_AGENT = "gamedeals_bot v0.2"
REDDIT_USERNAME = ""
DISCORD_TOKEN = ""
DISCORD_CHANNEL_ID = ""
DISCORD_PREFIX = 'd.'
REDDIT_NUMBER_OF_DEALS = 100
DISCORD_BOT_NAME = 'GameDeals'
```

## Get Started

### Docker

Navigate to the folder in `CMD` or `Terminal` and run `docker-compose up -d --build`. 

### Local

1. Navigate to the root folder.
2. Run `pip install -r requirements.txt`
3. Run `python gamedeals_bot.py`.

## Release History

Keep a [Changelog](https://github.com/div0ky/gamedeals_bot/blob/master/CHANGELOG.md)

## Meta

div0ky - https://div0ky.com - me@div0ky.com

Distributed under the GNU GPLv3 License. See `LICENSE` for more information.

[https://github.com/div0ky](https://github.com/div0ky)

## Contributing

1. Fork it ( https://github.com/div0ky/gamedeals_bot/fork )
2. Create your feature branch ( `git checkout -b feature/foobar` )
3. Commit your changes ( `git commit -Am 'Add some fooBar` )
4. Push to the branch ( `git push origin feature/foobar` )
5. Create a new Pull Request