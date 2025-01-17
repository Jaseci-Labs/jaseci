import:py logging;
import:py datetime;
import:py from jac_cloud.core.architype { NodeAnchor }
import:py from mtllm.llms {Ollama}
import:py from sentence_transformers { SentenceTransformer }
import:py from sklearn.metrics.pairwise { cosine_similarity }
import:py numpy;

glob logger = logging.getLogger("littleX");
glob llm = Ollama(host="http://127.0.0.1:11434", model_name="llama3.2:1b");
glob model = SentenceTransformer('all-MiniLM-L6-v2');

node profile {
    has username: str = "";
    has count_tag: dict = {};
    has followees: list = [];

    can get with get_profile entry {
        logger.info(f"profile info: Username: {here.username}, Followees: {here.followees}");
    }

    can confirm with update_profile exit {
        logger.info(f"Profile updated");
    }
}

node tweet;

node comment {
    has content: str;
}

edge follow {}

edge like {}

edge post {}

:node:tweet {
    has content: str;
    has created_at: str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S");
}

can 'Summarize latest trends, major events, and notable interactions from the recent tweets in one line.'
summarise_tweets(tweets: list[str]) -> 'Summarisation': str by llm();

can search_tweets(query: str, tweets: list, tweet_embeddings: any, similarity_threshold: float=0.25) -> list {
    query_embedding = model.encode([query]);
    similarities = cosine_similarity(query_embedding, tweet_embeddings)[0];
    results = [{**tweets[i], "similarity": similarities[i]} for i in range(len(similarities)) if similarities[i] >= similarity_threshold]
    ;
    return results;
}

walker visit_profile {
    can visit_profile with `root entry {
        visit [-->(`?profile)] else {
            logger.info("Creating new profile");
            new_profile = here ++> profile();
            visit new_profile;
        }
    }
}

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

walker update_profile :visit_profile: {
    has new_username: str;

    can update_profile with profile entry {
        logger.info("Updating profile");
        here.username = self.new_username;
        report here;
    }
}

walker get_profile :visit_profile: {
    can get_profile with profile entry {
        report here;
    }
}

walker follow_request :visit_profile: {
    has profile_id: str;

    can follow with profile entry {
        here.followees.append(self.profile_id);
        logger.info(f"New followee addded: {self.profile_id}");
        here +:follow():+> &self.profile_id;
        report here;
    }
}

walker un_follow_request :visit_profile: {
    has profile_id: str;

    can un_follow with profile entry {
        here.followees.remove(self.profile_id);
        logger.info(f"Followe removed: {self.profile_id}");
        here del-:follow:-> &self.profile_id;
        report here;
    }
}

walker load_likes {
    has likes: list = [];

    can load_likes with tweet entry {
        visit [-:like:->];
    }

    can load_profile with profile entry {
        Jac.unrestrict(here, level="READ");
        self.likes.append({"username": here.username});
    }

}

walker load_tweet {
    has tweet_info: dict = {};

    can load_tweets with tweet entry {
        self.tweet_info["content"] = here;
        visit [<-:post:-];
    }

    can load_profile with profile entry {
        self.tweet_info["username"] = here.username;
    }

}

walker load_comments {
    has comments: list = [];

    can load_comments with tweet entry {
        visit [-->](`?comment);
    }

    can report_comments with comment entry {
        Jac.unrestrict(here, level="READ");
        commenter = [<--](`?profile);
        self.comments.append(
            {"commenter": commenter[0].username, "comment": here}
        );
    }
}

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

walker load_feed :visit_profile: {
    has search_query: str = "";

    can load with profile entry {
        self.feeds: list = [];
        user_tweets = here spawn load_tweets();
        self.feeds.extend(user_tweets.tweets);

        for user in here.followees {
            user_node = &user;
            Jac.unrestrict(user_node, level="READ");
            logger.info("Acess has given to profile node");
            user_tweets = user_node spawn load_tweets();
            self.feeds.extend(user_tweets.tweets);
        }
        tweets = [feed['tweet']['content'].content for feed in self.feeds];
        self.summary: str = summarise_tweets(tweets);

        # Filter tweets based on search query
        if (self.search_query) {
            tweet_embeddings = model.encode(tweets);
            filtered_results = search_tweets(
                self.search_query,
                self.feeds,
                tweet_embeddings
            );
            report {"feeds": filtered_results, "summary": self.summary};
        } else {
            report {"feeds": self.feeds, "summary": self.summary};
        }

    }
}

walker create_tweet :visit_profile: {
    has content: str;

    can tweet with profile entry {
        tweet_node = here +:post:+> tweet(content=self.content);
        visit tweet_node;
    }

    can report_tweet with tweet entry {
        logger.info(f"Creating new tweet: {here.content}");
        Jac.unrestrict(here, level="READ");
        report here;
    }
}

walker update_tweet :visit_profile: {
    has tweet_id: str;
    has updated_content: str;

    can visit_tweet with profile entry {
        tweet_node = &self.tweet_id;
        visit tweet_node;
        logger.info(f"Tweet deleted: {tweet_node}");
    }
    # can be enhanced to directly use the jid instead
    can update_tweet with tweet entry {
        here.content = self.updated_content;
        report here;
    }
}

walker remove_tweet :visit_profile: {
    has tweet_id: str;

    can remove_tweet with profile entry {
        tweet_node = &self.tweet_id;
        here del--> tweet_node;
        logger.info(f"Tweet deleted: {tweet_node}");
    }
}

walker like_tweet :visit_profile: {
    has tweet_id: str;

    can like with profile entry {
        tweet_node = &self.tweet_id;
        Jac.unrestrict(tweet_node, level="CONNECT");
        tweet_node +:like():+> here;
        logger.info(f"liked to a tweet: {tweet_node}");
        report tweet_node;
    }
}

walker remove_like :visit_profile: {
    has tweet_id: str;

    can remove_like with profile entry {
        tweet_node = &self.tweet_id;
        tweet_node del-:like:-> here;
        logger.info(f"Reomve liked to a tweet: {tweet_node}");
        report tweet_node;
    }
}

walker comment_tweet :visit_profile: {
    has tweet_id: str;
    has content: str;

    can add_comment with profile entry {
        comment_node = here ++> comment(content=self.content);
        tweet_node = &self.tweet_id;
        Jac.unrestrict(tweet_node, level="CONNECT");
        tweet_node ++> comment_node[0];
        logger.info(f"comment added: {comment_node[0]}");
        report comment_node[0];
    }
}