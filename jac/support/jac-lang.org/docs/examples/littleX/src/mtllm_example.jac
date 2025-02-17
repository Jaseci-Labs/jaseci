import:py from mtllm.llms {Ollama}

glob llm = Ollama(host="http://127.0.0.1:11434", model_name="llama3.2:1b");

can 'Summarize latest trends, major events, and notable interactions from the recent tweets in one line.'
summarise_tweets(tweets: list[str]) -> 'Summarisation': str by llm();


with entry {
    Tweets = ["Just finished a thrilling book that I couldn't put down! What's your latest page-turner? 📚 #BookRecommendations"

,"Movie nights are the best! What's a film that you can watch over and over? 🎬 #FilmLovers"

,"Diving into a new fantasy series this weekend—what genre do you love to escape into? 🧙‍♂️ #Reading"

,"Caught the latest blockbuster last night! What's your favorite film of the year so far? 🍿 #Cinema"

,"Nothing like curling up with a good book and a cup of tea. What's your ideal reading setup? ☕📖 #CozyVibes"

,"Just started a new hobby: film photography! What hobbies are you passionate about? 📸 #CreativeLife"

,"Books can transport us to different worlds. What fictional universe would you love to live in? 🌌 #BookLovers"

,"Anyone else binge-watching classic films lately? What's a must-see that everyone should experience? 🎥 #MovieMarathon"

,"Reading is my escape. What's a book that changed your perspective on life? 🌍 #ImpactfulReads",

"I love discovering indie films! What's an underrated gem you'd recommend? 🌟 #HiddenGems"];
    print(summarise_tweets(Tweets));
}


