# **Building an Application with Jaseci**

This guide introduces how the Jaseci Stack accelerates application development by leveraging its graph-based programming model. With Jaseci, we can focus on implementing features rather than setting up complex systems. As you explore Jaseci’s features, you’ll uncover its wide range of use cases. This guide provides a quick introduction, helping you set up the Jaseci framework, define nodes, edges, and walkers, and craft application logic for your project.

## **What We Will Build**

We’ll develop a web application called **LittleX**, a streamlined and efficient version of Elon Musk’s X, using the Jaseci Stack. This project highlights the simplicity and power of Jaseci, enabling us to implement advanced features with minimal code and effort, tasks that typically require considerable time in traditional frameworks.

## **Key Features**
- **User authentication:** Sign up, log in, and profile management.
- **Content management:** Create, view, and interact with posts.
- **Social interactions:** Follow users and explore their content.

With Jaseci, we can focus on building these features seamlessly rather than dealing with the complexities of system setup. This guide focuses on the **backend** for LittleX, showcasing how Jaseci efficiently handles user authentication and database operations.

## Why Jaseci?

Jaseci empowers developers to build smarter applications with less hassle by:

- **Simplifying User Management:** It handles signup, login, and security out of the box.
- **Connecting Data Easily:** Perfect for building apps that need to model relationships, like social networks or recommendation systems.
- **Scalability Built-In:** Designed for cloud performance, so your app grows seamlessly with your users.
- **AI at Your Fingertips:** Adds intelligent features like personalization and moderation with minimal effort.

## **What You Need**

To get started with building **LittleX**, ensure you have the following:

- **About 15 minutes**: Time required to set up and explore the basics.
- **A favorite text editor or IDE**: Any development environment you are comfortable with.
- **Python 3.12 or later**: Ensure that Python 3.12 or higher is installed in your environment.
- **Install required libraries**: Jaclang, Jac-Cloud, MTLLM, and Jac-Splice-Orc.
- **Node.js (optional)**: If you plan to integrate a frontend in future steps.

## **LittleX Architecture**

=== "Single user"
      ![Image title](images/single-user.jpg)
=== "Multiple user"
      ![Image title](images/multi-user.jpg)

LittleX’s graph-based architecture uses nodes for entities like users and posts and edges for relationships like following or reacting. Nodes store attributes and behaviors, while edges capture properties like timestamps. Walkers traverse the graph, enabling dynamic actions and interactions. This design ensures efficient relationship handling, scalability, and extensibility for social media-like features.

## **Getting Started**

### **Set Up Jaseci**
```bash
pip install jaclang jac-cloud mtllm jac-splice-orc
```

### **Lesson 1: Let's create our first Node**

**Jaclang**, language used in Jaseci stack, organizes data as interconnected nodes within a spatial or graph-like structure. It focuses on the **relationships** between data points, rather than processing them **step-by-step**.

**Node**: A node is the fundamental unit of the Jaseci stack. Each node represents an object, entity, or a piece of data.

First create a node with name Person and attributes name, age.
```jac
node Person {
      has name: str;
      has age: int;
}
```

* The `node` keyword defines a node entity in the graph (`Person`).
* The `has` keyword specifies the attributes of the node.
* `name`, `age` are variable names (attributes of the `Person` node).
* `str`, `int` are the corresponding data types of these variables (`str` for string, `int` for integer).

Now, let's create the required nodes for LittleX.

=== "Guide"
      Nodes are essential for representing entities in LittleX. Here are the nodes we need to create:

      - **Profile Node**
        * Represents the user.
        * Fields: username
            ```jac
            node Profile {
                  has username: str = "";
            }
            ```

      - **Tweet Node**
        * Represents an individual tweet.
        * Fields: content, embedding, created_at (timestamp)
            ```jac
            node Tweet {
                  has content: str;
                  has embedding: list;
                  has created_at: str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S");
            }
            ```

      - **Comment Node**
        * Represents comments for the tweets.
        * Fields: content.
            ```jac
            node Comment {
                  has content: str;
            }
            ```
=== "LittleX Architecture Upto Now"
    ```jac linenums="1"
    --8<-- "support/jac-lang.org/docs/examples/littleX/src/LittleX_step2.jac"
    ```
For more explanation [visit](../../for_coders/data_spatial/nodes_and_edges.md)

### **Lesson 2: Creating Edges**

**Edge**: Edge represents the connections or relationships between nodes. Edges can be unidirectional or bidirectional.
![Image title](images/Family.jpg)

First, create an edge named Relation with the attribute 'since'.
```jac
edge Relation {
      has since: int;
}
```

* The `edge` keyword defines a relationship between nodes (Relation).
* The `has` keyword specifies the attributes of the edge.
* `int` is used for integer values (years).
* `str` is used for string values (names).

Now, let's create the required edges for LittleX.

=== "Guide"
      Edges define the relationships between nodes. Here are the edges we need to create:

      - **Follows Edge**
        * Represents the relationship between users who follow each other.
            ```jac
            edge Follow {}
            ```

      - **Like Edge**
        * Represents the interactions between users and the tweets.
            ```jac
            edge Like {}
            ```

      - **Post Edge**
        * Represents the relationship between the tweets and its authors.
            ```jac
            edge Post {}
            ```
=== "LittleX.jac Upto Now"
    ```jac linenums="1"
    --8<-- "support/jac-lang.org/docs/examples/littleX/src/LittleX_step3.jac"
    ```
For more explanation [visit](../../for_coders/data_spatial/nodes_and_edges.md)

### **Lesson 3: Creating our first Walker**
Walkers are graph-traversing agents in Jaclang that perform tasks without requiring initialization and can define abilities for various node types. The Jaseci stack automatically converts walkers into RESTful API endpoints.

First, create a walker named Relation with the attribute 'since'.
```jac
walker Agent {
      has name: str;
}
```
Now Lets create required walkers for LittleX.

=== "Guide"
      Walkers are graph-traversing agents that perform tasks. Here are the walkers we need to create:

      - **User Initialization Walker**
        * Creates or visits a new profile node for a user.
        * Ensures profiles exist in the system for any user action.
            ```jac
            walker visit_profile {
                  can visit_profile with `root entry {
                        visit [-->(`?Profile)] else {
                              new_profile = here ++> Profile();
                              visit new_profile;
                        }
                  }
            }
            ```
        * If current walker enter via `root`, `visit_profile` ability will be executed.
        * `visit [-->(``?profile)] else {}` Checks whether profile node exist from root, if yes, visit to that profile node. Otherwise execute to else part.
        * `here ++> profile()` It creates a profile node and connects with current node(`root`).
        * `visit new_profile` Walker visit to that node (`profile`).

      - **Load User Profile Walker**
        * Loads all profiles from the database.
        * Useful for managing or listing all users in the system.
            ```jac
            walker load_user_profiles {
                  obj __specs__ {
                        static has auth: bool = False;
                  }
                  can load_profiles with `root entry {
                        self.profiles: list = [];

                        for user in NodeAnchor.Collection.find({"name": "profile"}) {
                              user_node = user.architype;
                              self.profiles.append(
                              {"name": user_node.username, "id": jid(user_node)}
                              );
                        }
                        report self.profiles;
                  }
            }
            ```
        * `static has auth: bool = False` Set disable authentication for that walker.
        * `NodeAnchor.Collection.find({"name": "profile"})` Get list of profiles.
        * `user.architype` Get architype of user node.
        * `jid(user_node)` Get the unique id of an object.

      - **Update Profile Walker**
        * Updates a user's profile, specifically the username.
            ```jac
            walker update_profile :visit_profile: {
                  has new_username: str;
            }
            ```
        * First `visit_profile` walker is called and it visits to `Profile` node.
        * `here.username = self.new_username` Update username.
        * How `update_profile` walker spawned on `Profile` node, update the name will be discussed later.

      - **Get Profile Walker**
        * Retrieves profile details and logs them.
            ```jac
            walker get_profile :visit_profile: {
            }
            ```
        * First `visit_profile` walker is called and it visits to `Profile` node.
        * How `get_profile` walker spawned on `Profile` node, get the profile detailes will be discussed later.

      - **Follow Request Walker**
        * Creates a follow edge.
            ```jac
            walker follow_request {}
            ```
        * Walker `follow_request`, when spawned on the followee profile, will create a Follow edge from the follower to the followee.
        * How it is executed will be discussed later.

      - **Unfollow Request Walker**
        * Removes the follow edge.
            ```jac
            walker un_follow_request {}
            ```
        * Walker `un_follow_request` spawned on followee profile will remove the `Follow` edge from follower to followee.
        * How it is executed will be discussed later.

      - **Create Tweet Walker**
        * Creates a new tweet for a profile and adds it to the graph using a `Post` edge.
            ```jac
            walker create_tweet :visit_profile: {
                  has content: str;

                  can tweet with profile entry {
                        embedding = sentence_transformer.encode(self.content).tolist();
                        tweet_node = here +:Post:+> Tweet(content=self.content, embedding=embedding);
                        report tweet_node;
                  }
            }
            ```
        * `embedding = sentence_transformer.encode(self.content).tolist()` Embedding the content.
        * `tweet_node = here +:post:+> tweet(content=self.content, embedding=embedding)` Create a new tweet with content, its embedding.
        * `report tweet_node` reports the newly created tweet node.

      - **Update Tweet Walker**
        * Updates the content of an existing tweet by its ID.
            ```jac
            walker update_tweet {
                  has updated_content: str;
            }
            ```
        * Walker `update_tweet` spawned on tweet node, that will update the content of the tweet.
        * How it is executed will be discussed later.

      - **Remove Tweet Walker**
        * Deletes a tweet by removing its connection to the profile.
            ```jac
            walker remove_tweet {}
            ```
        * Walker `remove_tweet`, when spawned on a tweet node, will remove the tweet.
        * How it is executed will be discussed later.

      - **Like Tweet Walker**
        * Adds a like edge between a tweet and the profile liking it.
            ```jac
            walker like_tweet {}
            ```
        * Walker `like_tweet` spawned on tweet node, that will like the tweet.
        * How it is executed will be discussed later.

      - **Remove Like Walker**
        * Removes the like edge
            ```jac
            walker remove_like {}
            ```
        * Walker `remove_like` spawned on tweet node, that will remove the like.
        * How it is executed will be discussed later.

      - **Comment Tweet Walker**
        * Adds a comment to a tweet by creating a comment node and connecting it to the tweet.
            ```jac
            walker comment_tweet {
                  has content: str;
            }
            ```
        * Walker `comment_tweet` spawned on tweet node, that will add a comment to tweet and create a edge with author of the comment.
        * How it is executed will be discussed later.


      - **Load Tweet Walker**
        * Loads detailed information about a tweet, including its content, embedding and author.
            ```jac
            walker load_tweet:visit_profile: {
                  has if_report: bool = False;
                  has tweet_info: list[TweetInfo] = [];

                  can go_to_tweet with Profile entry {
                        visit [-->(`?Tweet)];
                        if self.if_report {
                              report self.tweet_info;
                        }
                  }
            }
            ```
        * First `visit_profile` walker is called and it visits to `Profile` node.
        * `visit [-->(`?Tweet)]` visits to each tweet and retrieve the info of tweets posted by the user.
        * How those tweets are retrieved will be discussed later.

      - **Load Feed Walker**
        * Fetches all tweets for a profile, including their comments and likes.
            ```jac
            walker load_feed :visit_profile: {
                  has search_query: str = "";

                  can load with Profile entry {
                        feeds: list = [];
                        user_tweets = here spawn load_tweets();
                        feeds.extend(user_tweets.tweet_info);

                        for user_node in [-:Follow:->](`?Profile) {
                              user_tweets = user_node spawn load_tweets();
                              feeds.extend(user_tweets.tweet_info);
                        }
                        tweets = [feed.content for feed in feeds];
                        tweet_embeddings = [numpy.array(feed.embedding) for feed in feeds];
                        summary: str = summarize_tweets(tweets);

                        # Filter tweets based on search query
                        if (self.search_query) {
                              filtered_results = search_tweets(
                              self.search_query,
                              feeds,
                              tweet_embeddings
                              );
                              report {"feeds": filtered_results, "summary": summary};
                        } else {
                              report {"feeds": self.feeds, "summary": summary};
                        }
                  }
            }
            ```
        * First `visit_profile` walker is called and it visits to `Profile` node.
        * With `Profile` entry following things are executed.
        * `user_tweets = here spawn load_tweets();` Spawn load_tweets walker with current node.
        * `feeds.extend(user_tweets.tweets);` Add the user's tweets to the profile's feed.
        * `user_node = &user;` Get the user node.
        * `self.summary: str = summarise_tweets(tweets);` Summarize the tweets.
        * `if (self.search_query) { ... } else { ... }` If a search query is provided, filter the tweets based on the query. Otherwise, return all tweets.

=== "LittleX.jac Upto Now"
    ```jac linenums="1"
    --8<-- "support/jac-lang.org/docs/examples/littleX/src/LittleX_step4.jac"
    ```

**Test functionality**

Using tools like Swagger or Postman, you can test these APIs to confirm their functionality.

1. Start the Server
`jac serve filename.jac` run using command line.

2. Access Swagger Docs
Open your browser and navigate to http://localhost:8000/docs

3. Test an API Endpoint
      - Click on an endpoint
      - Click "Try it out" to enable input fields.
      - Enter required parameters (if any).
      - Click "Execute" to send the request.
      - View the response (status code, headers, and JSON response body).

### **Lesson 4: Let's add some AI magic to our application using the power of MTLLM:**

In this lesson, we'll explore how to leverage AI to enhance your application. MTLLM supports easy integration of multiple LLM models, and for this tutorial, we are using Llama. If you need more details on integrating different models, please check the [MTLLM documentation](../../for_coders/jac-mtllm/quickstart.md). (You can also explore OpenAI’s LittleX for additional insights.)
Using Llama, you can summarize tweets to quickly understand trends, major events, and notable interactions in just one line.

**Why This Feature Matters**

Think of your application as a personalized newsfeed or trend analyzer.

- **Save Time:** Instead of scrolling through dozens of tweets, users get a quick summary of what's happening.
- **Gain Insights:** By distilling key information, the application helps users make sense of large volumes of data.
- **Engage Users:** AI-powered summaries make the experience dynamic and intelligent, setting your platform apart from others.

=== "Guide"
      - **Import Lamma with MTLLM**
      ```jac
      import from mtllm.llms {Ollama}
      glob llm = Ollama(host="http://127.0.0.1:11434", model_name="llama3.2:1b");
      ```
      - **Summarize Tweets Using Lamma:**
        * Summarize the latest trends, events, and interactions in tweets
            ```jac
            can 'Summarize latest trends, major events, and notable interactions from the recent tweets in one line.'
                  summarise_tweets(tweets: list[str]) -> 'Summarisation': str by llm();
            ```
      - **Test with Swagger**
       * Run the above mtllm example with `jac serve mtllm_example.jac`.
       * Register with email and password.
       * Login with registered email and password.
       * Copy the authentication key and paste it in authentication box.
       * Run the get_summary api endpoint.

=== "MTLLM Example"
    ```jac linenums="1"
    --8<-- "support/jac-lang.org/docs/examples/littleX/src/mtllm_example.jac"
    ```

### **Lesson 5: Exploring Graph Security**

Up until this point, you’ve successfully created a single-user social media application where a user can post tweets, like them, and interact with comments.

Now, imagine scaling this application to handle multiple users. Questions arise, such as:

- How do you ensure users cannot modify or view others' data without permission?
- How do you securely enable collaboration, such as liking or commenting on someone else's tweet?

This is where graph security in Jaclang simplifies managing access and permissions between users' graphs.

Jaclang offers explicit access control, ensuring data privacy and secure interactions between user graphs. Permissions define what other users can do with specific parts of a graph.

**Access Levels**

- **`NO_ACCESS`:** No access to the current archetype.
- **`READ`:** Read-only access to the current archetype.
- **`CONNECT`:** Allows other users' nodes to connect to the current node.
- **`WRITE`:** Full access, including modification of the current archetype.

**Granting and Managing Access**

By default, users cannot access other users' nodes. To grant access, permission mapping must be added explicitly.

- **Grant Access Using Walkers**
      ```jac
      Jac.allow_root(here, NodeAnchor.ref(self.root_ref_jid), self.access);
      ```
- **Remove Access**
      ```jac
      Jac.disallow_root(here, NodeAnchor.ref(self.root_ref_jid));
      ```
- **Grant Read Access to All**
      ```jac
      Jac.unrestrict(here, "READ");
      ```
- **Restrict Access**
      ```jac
      Jac.restrict(here);
      ```

=== "Guide"
      **Scenarios**

      - Posting a Tweet (Granting Read Access)

        * When a user creates a tweet, it is private by default.
        * To make it viewable by others, the system explicitly grants READ access to the tweet.
        * **Create Tweet Walker**
                  ```jac
                  walker create_tweet :visit_profile: {
                        has content: str;

                        can tweet with Profile entry {
                              embedding = sentence_transformer.encode(self.content).tolist();
                              tweet_node = here +:Post:+> Tweet(content=self.content, embedding=embedding);
                              Jac.unrestrict(tweet_node[0], level="CONNECT");
                              report tweet_node;
                        }
                  }
                  ```
        * `Jac.unrestrict(here, level="READ")` Unrestrict that tweet node to everyone with read access.

      - Commenting on a Tweet

        * Similar to liking, commenting requires CONNECT access.
        * A new comment node is created and linked to the tweet while granting READ access for others to view it.
        * **Comment Tweet Ability**
                  ```jac
                  can comment with comment_tweet entry {
                        current_profile = [root-->(`?Profile)];
                        comment_node = current_profile[0] ++> Comment(content=here.content);
                        Jac.unrestrict(comment_node[0], level="CONNECT");
                        self ++> comment_node[0];
                        report comment_node[0];
                  }
                  ```
        * `Jac.unrestrict(tweet_node, level="CONNECT")` Unrestrict the tweet node to connect level.

=== "LittleX.jac Upto Now"
    ```jac linenums="1"
    --8<-- "support/jac-lang.org/docs/examples/littleX/src/LittleX_step4.jac"
    ```

### **Lesson 6: Adding node abilities**
Nodes in Jaclang can have abilities defined to perform specific tasks. These abilities are structured as entry and exit points.

Imagine a smart home system where each room is represented as a node. Walkers traverse these nodes, performing tasks like turning lights on or off, adjusting temperature, or sending alerts when entering or exiting a room.

**Entry**
When someone enters a room:

- **Lights Turn On:** The system detects entry and automatically switches on the lights to ensure the person feels welcomed.
- **Room Occupied:** The system marks the room as occupied in its database or tracking system.

You enter the Living Room, and the system turns on the lights and logs your presence.

**Exit**
When someone exits a room:

- **Lights Turn Off:** The system detects the exit and switches off the lights to save energy.
- **Room Vacant:** It marks the room as unoccupied in its tracking system.

You leave the Living Room, and the system turns off the lights and updates its records to show the room is vacant.

=== "Guide"
      **Scenarios in node**

      - Update profile

        * A user updates their profile.
        * **Update Tweet Walker Ability**
                  ```jac
                  walker update_tweet :visit_profile: {
                        has tweet_id: str;
                        has updated_content: str;

                        can visit_tweet with profile entry {
                              tweet_node = &self.tweet_id;
                              visit tweet_node;
                        }

                        can update_tweet with tweet entry {
                              here.content = self.updated_content;
                              report here;
                        }
                  }
                  ```
        * **Update Profile Node Ability**

            * It replaces the abilities in walker.
                  ```jac
                  can update with update_profile entry {
                        self.username = here.new_username;
                        report self;
                  }
                  ```
        * As `update_profile` walker is spawned on `Profile`, it visits to `Profile`.
        *  With the entry of the `update_profile` walker, Profile will be updated.

      - Get profile

        * Get profile details.
        * **Update Tweet Walker Ability**
                  ```jac
                  walker get_profile :visit_profile: {
                        can get_profile with profile entry {
                              report here;
                        }
                  }
                  ```
        * **Create get ability**

            * It replaces the abilities in walker.
                  ```jac
                  can get with get_profile entry {
                        report self;
                  }
                  ```
        * As `get_profile` walker is spawned on `Profile`, It visits to `Profile`.
        *  With the entry of the `get_profile` walker, Profile will be reported.

      - Follow profile

        * Following a user.
        * **Update Tweet Walker Ability**
                  ```jac
                  walker follow_request :visit_profile: {
                        has profile_id: str;

                        can follow with profile entry {
                              here.followees.append(self.profile_id);
                              here +:follow():+> &self.profile_id;
                              report here;
                        }
                  }
                  ```
        * **Follow Request Node Ability**

            * It replaces the abilities in walker.
                  ```jac
                  can follow with follow_request entry {
                        current_profile = [root-->(`?Profile)];
                        current_profile[0] +:Follow():+> self;
                        report self;
                  }
                  ```
        * As `follow_request` walker is spawned on `Profile`, it visits to `Profile`.
        *  With the entry of the `follow_request` walker, `Follow` edge is created and connected.
        * `[root-->(`?Profile)]` gets the current user profile.
        * `current_profile[0] +:Follow():+> self` connects the followee with Follow edge.

      - Unfollow profile

        * Unfollowing a user.
        * **Unfollow Profile Walker Ability**
                  ```jac
                  walker un_follow_request :visit_profile: {
                        has profile_id: str;

                        can un_follow with profile entry {
                              here.followees.remove(self.profile_id);
                              here del-:follow:-> &self.profile_id;
                              report here;
                        }
                  }
                  ```
        * **Unfollow Profile Node Ability**

            * It replaces the abilities in walker.
                  ```jac
                  can un_follow with un_follow_request entry {
                        current_profile = [root-->(`?Profile)];
                        current_profile[0] del-:Follow:-> self;
                        report self;
                  }
                  ```
        * As `un_follow_request` walker is spawned on `Profile`, it visits to `Profile`.
        *  With the entry of the `un_follow_request` walker, `Follow` edge is disconnected.
        * `[root-->(`?Profile)]` gets the current user profile.
        * `current_profile[0] del-:Follow:-> self` disconnects the followee with Follow edge.

      - Update Tweet

        * User updated their tweet.
        * **Update Tweet Walker Ability**

                  ```jac
                  walker update_tweet :visit_profile: {
                        has tweet_id: str;
                        has updated_content: str;

                        can visit_tweet with profile entry {
                              tweet_node = &self.tweet_id;
                              visit tweet_node;
                        }

                        can update_tweet with tweet entry {
                              here.content = self.updated_content;
                              report here;
                        }
                  }
                  ```
        * **Update Tweet Node Ability**

            * It replaces the abilities in walker.
                  ```jac
                  can update with update_tweet exit {
                        self.content = here.updated_content;
                        report self;
                  }
                  ```
        * As `update_tweet` walker is spawned on `Tweet`, it visits to `Tweet`.
        *  With the exit of the `update_tweet` walker, the tweet is updated.
        * `self.content = here.updated_content` updated the current tweet.

      - Delete Tweet

        * Deletes the tweet.
        * **Delete Tweet Walker Ability**
                  ```jac
                  walker remove_tweet :visit_profile: {
                        has tweet_id: str;

                        can remove_tweet with profile entry {
                              tweet_node = &self.tweet_id;
                              here del--> tweet_node;
                        }
                  }
                  ```
        * **Delete Tweet Node Ability**

            * It replaces the abilities in walker.
                  ```jac
                  can delete with remove_tweet exit {
                        del self;
                  }
                  ```
        * As `remove_tweet` walker is spawned on `Tweet`, It visits to `Tweet`.
        *  With the exit of the `remove_tweet` walker, tweet is deleted.
        * `del self` deletes the current tweet.

      - Like Tweet

        * User likes the tweet.
        * **Like Tweet Walker Ability**
                  ```jac
                  walker like_tweet :visit_profile: {
                        has tweet_id: str;

                        can like with profile entry {
                              tweet_node = &self.tweet_id;
                              Jac.unrestrict(tweet_node, level="CONNECT");
                              tweet_node +:like():+> here;
                              report tweet_node;
                        }
                  }
                  ```
        * **Like Tweet Node Ability**

            * It replaces the abilities in walker.
                  ```jac
                  can like_tweet with like_tweet entry {
                        current_profile = [root-->(`?Profile)];
                        self +:Like():+> current_profile[0];
                        report self;
                  }
                  ```
        * As `like_tweet` walker is spawned on `Tweet`, it visits to `Tweet`.
        *  With the entry of the `like_tweet` walker, tweet is liked.
        * `[root-->(`?Profile)]` gets the current user profile.
        * `self +:Like():+> current_profile[0]` connects the user with `Like` edge.

      - Remove Like Ability

        * User removes the like.
        * **Remove Like Walker Ability**
                  ```jac
                  walker remove_like :visit_profile: {
                        has tweet_id: str;

                        can remove_like with profile entry {
                              tweet_node = &self.tweet_id;
                              tweet_node del-:like:-> here;
                              report tweet_node;
                        }
                  }
                  ```
        * **Remove Like Node Ability**

            * It replaces the abilities in walker.
                  ```jac
                  can remove_like with remove_like entry {
                        current_profile = [root-->(`?Profile)];
                        self del-:Like:-> current_profile[0];
                        report self;
                  }
                  ```
        * As `remove_like` walker is spawned on `Tweet`, it visits to `Tweet`.
        *  With the entry of the `remove_like` walker, like is removed.
        * `[root-->(`?Profile)]` gets the current user profile.
        * `self del-:Like:-> current_profile[0]` disconnects the user with `Like` edge.

      - Comment Ability

        * When a user creates a tweet, it is private by default.
        * **Comment Walker Ability**
                  ```jac
                  walker comment_tweet :visit_profile: {
                        has tweet_id: str;
                        has content: str;

                        can add_comment with profile entry {
                              comment_node = here ++> comment(content=self.content);
                              tweet_node = &self.tweet_id;
                              Jac.unrestrict(tweet_node, level="CONNECT");
                              tweet_node ++> comment_node[0];
                              report comment_node[0];
                        }
                  }
                  ```
        * **Comment Ability**

            * It replaces the abilities in walker.
                  ```jac
                  can comment with comment_tweet entry {
                        current_profile = [root-->(`?Profile)];
                        comment_node = current_profile[0] ++> Comment(content=here.content);
                        Jac.unrestrict(comment_node[0], level="CONNECT");
                        self ++> comment_node[0];
                        report comment_node[0];
                  }
                  ```
        * As `comment_tweet` walker is spawned on `Tweet`, it visits to `Tweet`.
        *  With the entry of the `comment_tweet` walker, comment is added to the tweet.
        * `[root-->(`?Profile)]` gets the current user profile.
        * `comment_node = current_profile[0] ++> Comment(content=here.content)` connects the user with `Comment` node.

      - Load Tweets

        * Load tweet information.
        * **Load Tweet Walker Ability**
                  ```jac
                  walker load_tweets :visit_profile: {
                        has if_report: bool = False;
                        has tweets: list = [];

                        can go_to_tweet with profile entry {
                              visit [-->](`?tweet);
                        }

                        can load_tweets with tweet entry {
                              Jac.unrestrict(here, level="READ");
                              comments = here spawn load_comments();
                              likes = here spawn load_likes();
                              tweet_content = here spawn load_tweet();

                              tweet_info = {
                                    "comments": comments.comments,
                                    "likes": likes.likes,
                                    "tweet": tweet_content.tweet_info
                              };
                              self.tweets.append(tweet_info);
                              if self.if_report {
                                    report self.tweets;
                              }
                        }
                  }
                  ```
        * **Load Tweets Node Ability**

            * It replaces the abilities in walker.
                  ```jac
                  can get_info()-> TweetInfo {
                        return TweetInfo(
                              id=jid(self),
                              content=self.content,
                              embedding=self.embedding,
                              likes=[i.username for i in [self-:Like:->]],
                              comments=[{"id": jid(i), "content": i.content} for i in [self-->(`?Comment)]]
                        );
                  }
                  ```
                  * This defines a abilitiy named `get_info` within the `Tweet` node and it returns an instance of the `TweetInfo` node.
                  * `id=jid(self)`retrieves the unique jac identifier (jid) of the current `Tweet` node.
                  * This assigns the `content` property of the current `Tweet` object to the `content` field of the `TweetInfo` object that has variables id, content, embedding, likes, comments.

=== "LittleX.jac Upto Now"
    ```jac linenums="1"
    --8<-- "support/jac-lang.org/docs/examples/littleX/src/LittleX_step6.jac"
    ```

### **Lesson 7: Integrating Jac Splice Orchestrator**

**JAC Cloud Orchestrator (jac-splice-orc)** transforms Python modules into scalable, cloud-based microservices. By deploying them as Kubernetes Pods and exposing them via gRPC, it empowers developers to seamlessly integrate dynamic, distributed services into their applications.

**Why is it important?**

- **Scalability at its Core**: It handles dynamic workloads by effortlessly scaling microservices.
- **Seamless Integration**: Makes advanced cloud-based service deployment intuitive and efficient, reducing the operational overhead.
- **Flexible and Dynamic**: Allows you to import Python modules dynamically, adapting to evolving application requirements.
- **Optimized for Developers**: Simplifies complex backend orchestration, enabling more focus on feature development and innovation.

=== "Guide"
      1. Setup Configuration file and Create Cluster
            ```bash
            kind create cluster --name cluster_name --config kind-config.yaml
            ```
      2. Initialize Jac Splice Orchestrator
            ```bash
            jac orc_initialize cluster_name
            ```

=== "kind-config.yaml"
    ```yaml linenums="1"
    --8<-- "support/jac-lang.org/docs/examples/littleX/src/kind-config.yaml"
    ```