import os
import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

from bs4 import BeautifulSoup
from selenium import webdriver


#getting track name and artist information
def get_all_tracks_from_playlist(playlist_id):
    tracks_response = session.playlist_tracks(playlist_id)
    tracks = tracks_response["items"]
    while tracks_response["next"]:
        tracks_response = session.next(tracks_response)
        tracks.extend(tracks_response["items"])

    return tracks
#creating working youtube search links
def search_url(s1,s2):
    words= (s1+" "+s2).split()
    result = "https://www.youtube.com/results?search_query="
    for i in words:
        for j in i:
            if j.isalnum() or j == " ":
                result += j
        if i!=words[-1]:  
            result += "+"
    return result


#spotify authentication
load_dotenv()
id = os.getenv("CLIENT_ID","")
secret = os.getenv("CLIENT_SECRET","")
client_credentials_manager = SpotifyClientCredentials(client_id=id, client_secret=secret)

# playlist_link = input("Enter the playlist link:")
playlist_link = "https://open.spotify.com/playlist/3eI93PhkrtkQyiHHybYyUU?si=956239b02a9b4741"

# getting the playlist uri
#eg: https://open.spotify.com/playlist/3eI93PhkrtkQyiHHybYyUU?si=956239b02a9b4741

#     between / and ?                  <--------------------> is the uri part                             
ques_index =0
index=0
for i in playlist_link:
    if i == "?":
        ques_index = index
    index+=1
playlist_uri = playlist_link[34:ques_index]

#opening a spotify session to access our playlist data
session = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

name =[]
singer=[]
yt_search_urls = []
for track in get_all_tracks_from_playlist(playlist_uri):
    song = track["track"]["name"]
    artists = " ".join([artist["name"] for artist in track["track"]["artists"]])
    name.append(track["track"]["name"])
    singer.append(artists)
    url = search_url(song,artists)
    yt_search_urls.append(url)

playlist_info = {'title': name, "artist": singer}
df = pd.DataFrame(playlist_info)

#inputting to csv file
df.to_csv("playlist.csv",encoding='utf-7', index=False)

print("\ncsv file created succesfully\n")

#--------------------------------------------------------------------


options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)
for i in yt_search_urls:
    try:
        driver.get(i)
        soup = BeautifulSoup(driver.page_source,'html.parser')
        links = soup.find_all("a", attrs={'id':'video-title'})
        link = "https://www.youtube.com"+links[0].get('href')
    except:
        continue
driver.quit()