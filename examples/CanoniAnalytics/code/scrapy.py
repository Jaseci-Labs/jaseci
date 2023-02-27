from bs4 import BeautifulSoup
import requests
import re
import json

from fastapi import HTTPException
from jaseci.actions.live_actions import jaseci_action
from jaseci.actions.remote_actions import launch_server


url_link = "https://imsdb.com/all-scripts.html"
_whitespace_re = re.compile(r"\s+")


def get_script(film_url):
    """
    Scrape the script from the given url.

    Parameters:
    ------------
    film_url :  Sring, a url to the script from https://imsdb.com/

    Return:
    -------------
    html_content : bs4.element.ResultSet. The bs4 resultset object, This contains the uncleaned moview script with html tags.
    """
    html_doc = requests.get(film_url).text
    soup = BeautifulSoup(html_doc, "html.parser")
    html_content = soup.find_all("pre")
    return html_content


def get_scenes(movie_script):
    """
    Extract movie scenes from the movie script.

    Parameters:
    ------------
    movie_script : bs4.element.ResultSet. The bs4 resultset object, This contains the uncleaned moview script with html tags.

    Return:
    ------------
    scenes : list. movie scenes as a list.
    """
    scenes = []

    for item in movie_script[0].find_all("b"):
        tag = item.get_text()
        tag = re.sub(_whitespace_re, " ", tag).strip()
        if tag.__contains__("EXT.") or tag.__contains__("INT."):
            scenes.append(tag)

    return scenes


def find_between(text, first, last):
    """
    Get the substring between two substrings.

    Parameters:
    ------------
    text : String. The main input string, where need to be chuncked.
    first : String. The first substring.


    Return:
    ------------
    substring: String.

    """
    start = text.index(first) + len(first)
    end = text.index(last, start)
    substring = text[start:end]

    return substring


def actors_content(scene):
    """ """
    scene_items = scene.replace("\r", "").split("\n")
    actors = []
    actor_line = []
    actors_dict = {}

    for i in range(0, len(scene_items)):
        leading_space = len(scene_items[i]) - len(scene_items[i].lstrip())
        if leading_space == 25 and len(scene_items[i].strip()) != 0:
            actor = scene_items[i].strip()
            if actor.isalpha():
                actors.append(actor)
                actor_line.append(i)
    if len(actors) != 0:
        scene_desc = " ".join(scene_items[: actor_line[0]])
        scene_desc = re.sub(_whitespace_re, " ", scene_desc).strip()
        for i in range(0, len(actors)):
            try:
                actor_content = " ".join(
                    scene_items[actor_line[i] + 1 : actor_line[i + 1]]
                )
                actor_content = re.sub(_whitespace_re, " ", actor_content).strip()
            except IndexError as e:
                actor_content = " ".join(scene_items[actor_line[i] + 1 :])
                actor_content = re.sub(_whitespace_re, " ", actor_content).strip()
            if not (actors[i] in actors_dict.keys()):
                actors_dict[actors[i]] = [actor_content]
            else:
                get_prev = actors_dict[actors[i]]
                actors_dict[actors[i]] = get_prev + [actor_content]
        return scene_desc, actors_dict
    else:
        scene_desc = re.sub(_whitespace_re, " ", scene).strip()
        return scene_desc


@jaseci_action(act_group=["scrappy"], allow_remote=True)
def scrape_content(url: str):

    try:
        movie_script = get_script(url)
        movie_scenes = {}
        full_script = movie_script[0].get_text()
        scenes = get_scenes(movie_script)
        for i in range(0, len(scenes)):
            try:
                scene_content = find_between(full_script, scenes[i], scenes[i + 1])
            except IndexError as e:
                scene_content = full_script.split(scenes[i])[1]
            movie_scenes[scenes[i]] = actors_content(scene_content)

        with open("movie_data.json", "w") as outfile:
            json.dump(movie_scenes, outfile)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
