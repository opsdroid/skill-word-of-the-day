import logging
import random

import aiohttp
import feedparser

from opsdroid.matchers import match_regex, match_crontab


_LOGGER = logging.getLogger(__name__)
_OED_WOD_BASE_URL = "http://www.oed.com/rss/wordoftheday"


async def get_feed():
    async with aiohttp.ClientSession() as session:
        async with session.get(_OED_WOD_BASE_URL) as resp:
            feed = feedparser.parse(await resp.text())
            return feed


@match_regex(r'.*word of the day.*')
@match_crontab('30 09 * * *')
async def word_of_the_day(opsdroid, config, message):
    intro = random.choice([
        "Here's today's word of the day",
        "Here's the OED word of the day",
        "Why not try and use this word today",
        "Today's goal, say this word to a stranger"
    ])
    feed = await get_feed()
    word = feed["entries"][0]["title"]
    link = feed["entries"][0]["link"]
    definition = ".".join(feed["entries"][0]["summary"].split(".")[1:]).strip()
    response = "{}\n> {}\n> {}\n> {}".format(intro, word, definition, link)
    await message.respond(response)
