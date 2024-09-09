# Creating custom action to scrap movie data

This is a Python script that scrapes movie scripts from https://imsdb.com/ and extracts information about scenes and actors. It also stores the extracted information in a JSON file called `movie_data.json`.

## Creating the custom Jaseci action

The script uses the following Python libraries:

```
from bs4 import BeautifulSoup
import requests
import re
import json

from fastapi import HTTPException
from jaseci.jsorc.live_actions import jaseci_action
from jaseci.jsorc.remote_actions import launch_server
```

`BeautifulSoup` from the bs4 library to parse and extract data from HTML.
`requests` to make HTTP requests to retrieve the HTML content of a given URL.
`re` to work with regular expressions.
`json` to store the extracted data in a JSON file.

Make sure you have installed them in your current Python working environment.

Next, we are initializing the url_link and the regular expressions for white spaces.

```python
url_link = "https://imsdb.com/all-scripts.html"
_whitespace_re = re.compile(r"\s+")
```

We are using four supplementary Python functions in this script. Here's a brief overview of the functions defined in this script:

```python
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

```

This function takes a URL to a movie script on `https://imsdb.com/` and returns a `bs4.element.ResultSet` object containing the uncleaned movie script with HTML tags.

```python
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
```
This function takes a `bs4.element.ResultSet` object containing the uncleaned movie script with HTML tags and returns a list of scenes.

```python

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
```
This function takes a string, a starting substring, and an ending substring, and returns the substring between the two given substrings.

```python

def actors_content(scene):
    """
    Extract information about scenes.

    Parameters:
    ------------
    scene : String

    Return:
    ------------
    scene_dict: Dictionary
    actors_dict: Dictionary


    """
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
```

This function takes a scene as input and extracts information about the actors and their content. It returns a tuple containing the scene description and a dictionary of actors and their content.

```python

@jaseci_action(act_group=["scrapy"], allow_remote=True)
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
        return movie_scenes

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

`scrape_content(url)` is the main function that takes a URL to a movie script on https://imsdb.com/ and returns a JSON object containing the extracted information about the scenes and actors.

This function first retrieves the HTML content of the given URL using the `requests.get()` method and parses it using **BeautifulSoup**. It then calls `get_scenes()` to get a list of scenes and `actors_content()` to extract information about actors and their content for each scene. The extracted data is stored in a Python dictionary called `movie_scenes`. Finally, the `json.dump()` method is used to write the dictionary to a JSON file called `movie_data.json`.

This script is also decorated with a `jaseci_action()` decorator which makes it an executable action for the Jaseci eco system. The decorator adds metadata to the function that allows it to be executed remotely by a Jaseci server.

Now save all this code in a python file, and let's see how it's executed inside Jaseci.

## Executing the custom Jaseci action

Start the Jaseci shell session and load the local action with the following command. Here, the `scrapy.py` is the file name that I was given for the Python script that we created.

```
actions load local scrapy.py
```

After successful execution you will see the following output.

```
{
  "success": true
}
```

Execute `action list` command in `jsctl` shell to see if the custom action is loaded successfully. If the action is loaded successfully, you may see `"scrapy.scrape_content"` at the end of the loaded actions list.

Following is an example walker to execute the above Jaseci action.

```jac
walker init{
    can scrapy.scrape_content;

    report scrapy.scrape_content("https://imsdb.com/scripts/Thor.html");
}
```
run this jac code and observe the `movie_data.json` file generated in the current working directory.


> **Note**
> This data scraping algorithm is tailored to extract information from the given link's **Thore** movie.
> You can try scraping the script from another movie if that piques your interest by customizing the scrapping script.