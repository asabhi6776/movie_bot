import discord
import requests

# client = discord.Client()
intents = discord.Intents.all()
client = discord.Client(intents=intents)

# Define the YTS search function
def search_yts(query):
  # Send an HTTP GET request to the YTS API with the specified query
  response = requests.get(f'https://yts.mx/api/v2/list_movies.json?query_term={query}')
  
  # Extract the JSON data from the response
  data = response.json()
  
  # Extract the list of movies from the data
  movies = data['data']['movies']
  
  # Build a list of movie titles and download links
  results = []
  for movie in movies:
    title = movie['title']
    for torrent in movie['torrents']:
      url = torrent['url']
      results.append(f'{title}: {url}')
  
  # Join the results into a single string and return them
  results_str = '\n'.join(results)
  return results_str

# Define the 1337x search function
def search_1337x(query):
  # Send an HTTP GET request to the 1337x search page with the specified query
  response = requests.get(f'https://1337x.to/search/{query}/1/')
  
  # Extract the HTML from the response
  html = response.text
  
  # Use a regular expression to find all the torrent download links in the HTML
  # import re
  # links = re.findall(r'href="/torrent/\d+/[^"]+"', html)

  # Use a regular expression to find all the torrent download links in the HTML
# Use a regular expression to find all the torrent download links in the HTML
  import re
  links = re.findall(r'href="/torrent/\d+/[^"]+" class="download"', html)


  
  # Build a list of download links
  results = []
  for link in links:
    url = f'https://1337x.to{link[6:-1]}'
    results.append(url)
  
  # Join the results into a single string and return them
  results_str = '\n'.join(results)
  return results_str

# Define the on_message event
@client.event
async def on_message(message, search_engine="yts"):
  # If the message is a "!torrent" command
  if message.content.startswith("!torrent"):
    # Extract the query from the command
    query = message.content[9:]
    
    # Determine which search function to use based on the search_engine parameter
    if search_engine == "yts":
      search_func = search_yts
    elif search_engine == "1337x":
      search_func = search_1337x
    else:
      await message.channel.send("Invalid search engine specified.")
      return
    
    # Search for torrents and send the results to the user
    results_str = search_func(query)
    await message.channel.send(results_str)

client.run("Token here")
