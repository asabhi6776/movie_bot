import discord
import requests
import os


TOKEN = os.environ['DISCORD_BOT_TOKEN']
# client = discord.Client()
intents = discord.Intents.all()
client = discord.Client(intents=intents)


# Set the base URLs for the 1337x and YTS APIs
BASE_URL_1337X = "https://1337x.to/api/v2/search"
BASE_URL_YTS = "https://yts.mx/api/v2/list_movies"

def search_1337x(query):
  # Set the parameters for the 1337x API
  params = {
    "query": query,
    "sort": "seeds",
    "limit": 10
  }

  # Send a request to the 1337x API
  response = requests.get(BASE_URL_1337X, params=params)

  # Check if the request was successful
  if response.status_code == 200:
    # Get the list of movies from the response
    movies = response.json()["torrents"]

    # Return a list of titles and magnet links for each movie
    results = []
    for movie in movies:
      results.append(f"Title: {movie['title']}\nMagnet Link: {movie['magnetLink']}\n")
    return results
  else:
    return ["An error occurred while searching 1337x."]

def search_yts(query):
  # Set the parameters for the YTS API
  params = {
    "query_term": query,
    "sort_by": "seeds",
    "limit": 10
  }

  # Send a request to the YTS API
  response = requests.get(BASE_URL_YTS, params=params)

  # Check if the request was successful
  if response.status_code == 200:
    # Get the list of movies from the response
    movies = response.json()["data"]["movies"]

    # Return a list of titles and magnet links for each movie
    results = []
    for movie in movies:
      results.append(f"Title: {movie['title_long']}\nMagnet Link: {movie['torrents'][0]['url']}\n")
    return results
  else:
    return ["An error occurred while searching YTS."]

@client.event
async def on_message(message):
  # Check if the message is a command
  if message.content.startswith("!search"):
    # Split the message into the command and the query
    command, query = message.content.split(" ", 1)

    # Search for movies on 1337x and YTS
    results_1337x = search_1337x(query)
    results_yts = search_yts(query)

    # Concatenate the results and send them back to the user
    results = "\n".join(results_1337x + results_yts)
    await message.channel.send(results)

client.run(TOKEN)