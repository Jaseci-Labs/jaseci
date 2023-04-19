# Preparation

### **1. Installing Jaseci**
Before getting started you have to install Jaseci latest version. Jaseci requeres python 3.10 or later version. We prefer you to create a fresh python environment using conda or any other virtual environment packaging to try out codes in this codelab. A complete Jaseci installation guide is
[here](../../../docs/docs/getting-started/installation.md)

After successfull installation of Jaseci run the help command,

```
jsctl --help
```

`jsctl` stands for the Jaseci Command Line Interface.
If the command above displays the help menu for `jsctl`, then you have successfully installed jaseci.

### **1. Installing Jaseci Server**

Install Jaseci Server Using following commands.

```
pip install jaseci-serv
```

Before getting start to use jaseci server, a few commands are required to set up the database.
```
jsserv makemigrations base
jsserv makemigrations
jsserv migrate
```
The above commands essentially initializes the database schemas. We will also need an admin user so we can log into the jaseci server. To create an admin user, run

```
jsserv createsuperuser
```

And follow the command line prompts to create a super user. For the purpose of this demostration, we are going to use the following credentials:

```
Email: admin@jaseci.org
Password: JaseciAdmin
```
Then launch the jaseci server with

```
jsserv runserver
```

You should see an output that looks like the following if everything is fine.

```
$ jsserv runserver
Watching for file changes with StatReloader
Performing system checks...
System check identified no issues (0 silenced).
October 24, 2022 - 18:27:14
Django version 3.2.15, using settings 'jaseci_serv.jaseci_serv.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```
### **2. Installing Jaseci Studio**

You can find the Jaseci Studio Binery that is relevant to your operating system [here](https://github.com/Jaseci-Labs/jaseci/releases/tag/v1.4.0.8).

Once we have the application installed and launch it, you'll see a login screen similar to this.

![Jaseci Studio Login]("./../../images/jaseci_studio_login.png)

There you have to enter the server endpoint in the host and port fields. And also enter the login credentials which you created with jaseci server setup. To verify the information click on the "Test Connection". If there is an error, check that your server is still running and ensure that there is no typo in any of the fields.

Click connect once you have verified that all is good.

### **3. Collecting data for codelab**

Movie scripts data is the textual data that we use in this coding lab. Here we are going to scrap movie scrip data from [Imbdsm](https://imsdb.com/) website. We have given you the python script [here](../code/scrapy.py) which we can be run as a Jaseci action.

Steps to run Jaseci custom action to scrape data.

1. Get the `scrapy.py` python from [here](../code/scrapy.py).
2. Open the `jsctl` shell session.
3. Load the custom action in local with following command.
   ```
   actions load local scrapy.py
   ```
4. Create a `scrap.jac` file and include the following;
    ```jac
    walker init{
        can scrapy.scrape_content;

        report scrapy.scrape_content("https://imsdb.com/scripts/Thor.html");
    }
    ```
5. Run `scrap.jac`
   ```
   jac run scrap.jac
   ```
6. You will see the `movie_data.json` file in the current directory.

Sample of the `movie_data.json` file is as follows;

```json
{
    "1 EXT. PUENTE ANTIGUO, NEW MEXICO - NIGHT 1": "A main street extends before us in this one-horse town, set amid endless flat, arid scrubland. A large SUV slowly moves down the street and heads out of town.",
    "2 EXT. SUV - NIGHT 2": [
        "The SUV sits parked in the desert. Suddenly, the roof panels of the SUV FOLD OPEN. The underside of the panels house a variety of hand-built ASTRONOMICAL DEVICES, which now point at the sky. JANE FOSTER (late 20's) pops her head through the roof. She positions a MAGNETOMETER, so its monitor calibrates with the constellations above. It appears to be cobbled together from spare parts of other devices.",
        {
            "JANE": [
                "Hurry! We hear a loud BANG followed by muffled CURSING from below. Jane offers a hand down to ERIK SELVIG (60) who emerges as well, rubbing his head. JANE (CONT'D) Oh-- watch your head.",
                "It's a little different each time. Once it looked like, I don't know, melted stars, pooling in a corner of the sky. But last week it was a rolling rainbow ribbon--",
            ],
            "SELVIG": [
                "Thanks. So what's this anomaly of yours supposed to look like?",
                "(GENTLY TEASING) Racing round Orion? I've always said you should have been a poet. Jane reigns in her excitement. She tries for dignity. 4th BLUE REVISIONS 03-26-10 1A.",
                "(re: the gloves) I recognize those. Think how proud he'd be to see you now. Jane's grin fades to a sad smile.",
                "For what?"
            ]
        }
    ],
    "3 INT. SUV - NIGHT 3": [
        "The SUV is bathed in the glow of high-tech monitoring equipment and laptops, some looking like they're held together with duct tape. Jane opens a well-worn NOTEBOOK of handwritten notes and calculations. Selvig watches the frustrated Jane with sympathy.",
        {
            "JANE": [
                "The anomalies are always precipitated by geomagnetic storms. She shows him a complicated CHART she's drawn in the book, tracking occurrences and patterns. I just don't understand. Something catches Darcy's eye out the driver's side mirror. She adjusts it. In the distance",
            ],
            "DARCY": [
                "Jane? Jane SHUSHES her, leafs through her notes. The bottle of champagne begins to vibrate.",
                "The champagne bottle starts to RATTLE noisily now as it shakes more violently, pressure building up inside it, when the cork EXPLODES out of it. Champagne goes spewing everywhere -- over equipment, over Jane. DARCY (CONT'D) Jane?",
            ],
            "SELVIG": [
                "That's your subtle aurora?!"
            ]
        }
    ],
}
```

7. If you are interested to know more details about custom Jaseci actions and scrapping data. You can read it [here](../codelabs/7_creating_custom_action_to_scrap_movie_data.md).
