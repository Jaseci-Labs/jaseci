import datetime;
import from jac_cloud.core.architype { NodeAnchor }
import from mtllm.llms { Ollama }
import numpy;
import from sentence_transformers { SentenceTransformer }
import from sklearn.metrics.pairwise { cosine_similarity }

glob llm = Ollama(host="http://127.0.0.1:11434", model_name="llama3.2:1b");
glob sentence_transformer = SentenceTransformer('all-MiniLM-L6-v2');

can search_tweets(query: str, tweets: list, tweet_embeddings: any, similarity_threshold: float=0.25) -> list {
    query_embedding = sentence_transformer.encode([query]);
    similarities = cosine_similarity(query_embedding, tweet_embeddings)[0];
    results = [{"Tweet_Info": tweets[i], "similarity": similarities[i]} for i in range(len(tweets)) if similarities[i] > similarity_threshold];
    return results;
}

can 'Extract and summarize trending themes, major highlights, and key interactions from recent tweets in one concise sentence.'
summarize_tweets(tweets: list[str]) -> 'Summarisation': str by llm();

node Profile {
    has username: str = "";
}

node Tweet {
    has content: str;
    has embedding: list;
    has created_at: str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S");
}

node Comment {
    has content: str;
}

edge Follow {}

edge Like {}

edge Post {}

obj TweetInfo {
    has id: str;
    has content: str;
    has embedding: list;
    has likes: list;
    has comments: list;
}

walker visit_profile {
    can visit_profile with `root entry {
        visit [-->(`?Profile)] else {
            new_profile = here ++> Profile();
            Jac.unrestrict(new_profile[0], level="CONNECT");
            visit new_profile;
        }
    }
}

walker update_profile :visit_profile: {
    has new_username: str;
}

walker get_profile :visit_profile: {}

walker load_user_profiles {
    obj __specs__ {
        static has auth: bool = False;
    }
    can load_profiles with `root entry {
        self.profiles: list = [];

        for user in NodeAnchor.Collection.find({"name": "Profile"}) {
            user_node = user.architype;
            self.profiles.append(
                {"name": user_node.username, "id": jid(user_node)}
            );
        }
        report self.profiles;
    }
}

walker follow_request {}

walker un_follow_request {}

walker create_tweet :visit_profile: {
    has content: str;

    can tweet with Profile entry {
        embedding = sentence_transformer.encode(self.content).tolist();
        tweet_node = here +>:Post:+> Tweet(content=self.content, embedding=embedding);
        Jac.unrestrict(tweet_node[0], level="CONNECT");
        report tweet_node;
    }
}

walker update_tweet {
    has updated_content: str;
}

walker remove_tweet {}

walker like_tweet {}

walker remove_like {}

walker comment_tweet {
    has content: str;
}

walker load_tweets :visit_profile: {
    has if_report: bool = False;
    has tweet_info: list[TweetInfo] = [];

    can go_to_tweet with Profile entry {
        visit [-->(`?Tweet)];
        if (self.if_report) {
            report self.tweet_info;
        }
    }

    can report_tweet with Tweet entry {
        self.tweet_info.append(here.get_info());
    }
}

walker load_feed :visit_profile: {
    has search_query: str = "";

    can load with Profile entry {
        feeds: list = [];
        user_tweets = here spawn load_tweets();
        feeds.extend(user_tweets.tweet_info);

        for user_node in [->:Follow:->](`?Profile) {
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