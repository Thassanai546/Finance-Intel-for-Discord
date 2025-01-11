import os
import discord
import finance_data

# Set up Discord bot intents
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print('{0.user} is online.'.format(client))


@client.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == client.user:
        return

    if message.content.startswith('/help'):
        # Get the user's name
        user_name = message.author.name

        # Create the embed with the user's name in the title
        embed = discord.Embed(
            title=f"Hey {user_name}, here are the available commands:",
            description=
            "Top Trending Stocks in the US: https://finance.yahoo.com/markets/stocks/trending/",
            color=discord.Color.pink())

        embed.add_field(
            name="/pingfin",
            value=
            "Check if Finance Intelligence is online and get trending stocks.",
            inline=False)

        embed.add_field(
            name="/getinfo [ticker]",
            value=
            "Get company details for the given stock ticker (e.g., AAPL for Apple).",
            inline=False)

        embed.add_field(name="/getfin [ticker]",
                        value="Get financial data for the given stock ticker.",
                        inline=False)

        embed.add_field(
            name="/get52 [ticker]",
            value="Get 52-week high/low data for the given stock ticker.",
            inline=False)

        embed.add_field(
            name="/getrec [ticker]",
            value="Get stock recommendations for the given stock ticker.",
            inline=False)

        await message.channel.send(embed=embed)

    # Respond ping test
    if message.content.startswith('/pingfin'):
        await message.channel.send('Finance Intelligence bot is online :)')
        await message.channel.send(
            'Top Trending Stocks: https://finance.yahoo.com/markets/stocks/trending/'
        )

    if message.content.startswith('/getinfo'):
        try:
            ticker = message.content.split(' ')[1]
            ticker_result = finance_data.get_company_details(ticker)
            await message.channel.send(ticker_result)
        except Exception as e:
            await message.channel.send(
                "Enter the stock ticker of the company (e.g., AAPL for Apple)")

    if message.content.startswith('/getfin'):
        try:
            ticker = message.content.split(' ')[1]
            ticker_result = finance_data.get_financial_data(ticker)
            await message.channel.send(ticker_result)
        except Exception as e:
            await message.channel.send(
                "Enter the stock ticker of the company (e.g., AAPL for Apple)")

    if message.content.startswith('/get52'):
        try:
            ticker = message.content.split(' ')[1]
            ticker_result = finance_data.get_52_week_high_low(ticker)
            await message.channel.send(ticker_result)
        except Exception as e:
            await message.channel.send(
                "Enter the stock ticker of the company (e.g., AAPL for Apple)")

    if message.content.startswith('/getrec'):
        try:
            ticker = message.content.split(' ')[1]
            ticker_result = finance_data.get_stock_recommendations(ticker)
            await message.channel.send(ticker_result)
        except Exception as e:
            await message.channel.send(
                "Enter the stock ticker of the company (e.g., AAPL for Apple)")


try:
    token = os.environ['Bot_Token']
    if token == "":
        raise Exception("No Discord Token found.")
    client.run(token)
except discord.HTTPException as e:
    if e.status == 429:
        print(
            "The Discord servers denied the connection for making too many requests"
        )
        print(
            "Get help from https://stackoverflow.com/questions/66724687/in-discord-py-how-to-solve-the-error-for-toomanyrequests"
        )
    else:
        raise e
