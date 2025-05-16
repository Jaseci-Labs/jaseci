
:can:search_tweets {
    query_embedding = sentence_transformer.encode([query]);
    tweet_embeddings = sentence_transformer.encode([tweet]);
    similarity = cosine_similarity(query_embedding, tweet_embeddings)[0];
    return similarity;
}
 
:node:Profile:can:update {
    self.username = here.new_username;
    report self;
}

:node:Profile:can:get {
        follwers=[{"id": jid(i), "username": i.username} for i in [self-->(`?Profile)]];
        report {"user": self, "followers": follwers};
    }

:node:Profile:can:follow{
        current_profile = [root-->(`?Profile)];
        current_profile[0] +:Follow():+> self;
        report self;
    }

:node:Profile:can:un_follow {
        current_profile = [root-->(`?Profile)];
        follow_edge = :e:[ current_profile[0] -:Follow:-> self];
        Jac.destroy(follow_edge[0]);
        report self;
    }

:node:Tweet:can:update {
        self.content = here.updated_content;
        report self;
    }

:node:Tweet:can:delete {
        Jac.destroy(self);
    }

:node:Tweet:can:like_tweet {
        current_profile = [root-->(`?Profile)];
        self +:Like():+> current_profile[0];
        report self;
    }

:node:Tweet:can:remove_like {
        current_profile = [root-->(`?Profile)];
        like_edge = :e:[ self -:Like:-> current_profile[0]];
        Jac.destroy(like_edge[0]);
        report self;
    }

:node:Tweet:can:comment {
        current_profile = [root-->(`?Profile)];
        comment_node = current_profile[0] ++> Comment(content=here.content);
        Jac.unrestrict(comment_node[0], level="CONNECT");
        self ++> comment_node[0];
        report comment_node[0];
    }

:node:Tweet:can:get_info {
        return TweetInfo(
            username=[self<-:Post:-][0].username,
            id=jid(self),
            content=self.content,
            embedding=self.embedding,
            likes=[i.username for i in [self-:Like:->]],
            comments=[{"username": [i<--(`?Profile)][0].username, "id": jid(i), "content": i.content} for i in [self-->(`?Comment)]]
        );
    }

:node:Tweet:can:get {
        tweet_info = self.get_info();
        similarity = search_tweets(here.search_query, tweet_info.content);
        here.results.append({"Tweet_Info": tweet_info, "similarity": similarity});
    }

:node:Comment:can:update {
        self.content = here.updated_content;
        report self;
    }

:node:Comment:can:delete {
        Jac.destroy(self);
    }

:walker:visit_profile:can:visit_profile {
        visit [-->(`?Profile)] else {
            new_profile = here ++> Profile();
            Jac.unrestrict(new_profile[0], level="CONNECT");
            visit new_profile;
        }
    }

:walker:load_user_profiles:can:load_profiles {
        self.profiles: list = [];
        
        for user in NodeAnchor.Collection.find({"name": "Profile"}) {
            user_node = user.architype;
            self.profiles.append(
                {"name": user_node.username, "id": jid(user_node)}
            );
        }
        report self.profiles;
    }

:walker:create_tweet:can:tweet {
        embedding = sentence_transformer.encode(self.content).tolist();
        tweet_node = here +:Post:+> Tweet(content=self.content, embedding=embedding);
        Jac.unrestrict(tweet_node[0], level="CONNECT");
        report tweet_node;
    }

:walker:load_feed:can:load {
        visit [-->(`?Tweet)];
        for user_node in [-:Follow:->(`?Profile)] {
            visit [user_node-->(`?Tweet)];
        }
        report self.results;
    }