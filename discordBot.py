import discord
from sheetsBot import SheetsBot
import datetime


def main():
    TOKEN = 'PLACE DISCORD BOT TOKEN HERE'
    bot = discord.Client()

    current_time = datetime.datetime.now()
    day = current_time.day
    month = current_time.month
    monthWord = current_time.strftime("%B")
    year = current_time.year

    # Notifies the user that the bot is active and ready to receive commands

    @bot.event
    async def on_ready():
        print('We have logged in as {0.user}'.format(bot))

    @bot.event
    async def on_message(message):
        listOfIds = []
        if message.author == bot.user:
            return

        if message.content.startswith('$Update SunsetSeries!'):
            ubcGuild = bot.guilds[0]
            categoryChannels = ubcGuild.categories
            specificChannel = None
            for category in categoryChannels:
                # Change category.name to the game you want to update
                if category.name == "🎮 Valorant":
                    specificChannel = category
            textChannel = message.channel
            voiceChannels = filter(
                lambda x: x.type[0] == 'voice', specificChannel.channels)
            for c in voiceChannels:
                listOfMembers = c.members
                for m in listOfMembers:
                    name = m.name
                    uniqueCode = m.discriminator
                    originalString = name + "#" + uniqueCode
                    listOfIds.append(originalString)
        sheetBot = SheetsBot(listOfIds)
        sheetBot.updateGameTabCells("{} {}, {}".format(monthWord, day, year))
        sheetBot.updatePointSystem("0{}-{}-{}".format(month, day, year), 225)
        await textChannel.send('Done updating!')

    bot.run(TOKEN)


if __name__ == "__main__":
    main()
