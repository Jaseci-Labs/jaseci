# fmt: off
# the above line of code is to disbale black linting
# so it doesn't add a extra ',' at end of every list
# which in turns furether create issue while parsing through fast api
test_train_request = {
    "traindata": {
        "tell a joke": [
            "hey can you tell me a joke",
            "can you make me laugh?",
            "do you know of any jokes",
            "i want to laugh, tell me a joke please"
        ],
        "greeting": [
            "hello",
            "hi",
            "hey",
            "how's it going",
            "how are you",
            "whats up",
            "what's going on",
            "what's good",
            "how goes it"
        ],
        "agreement": [
            "yes let's do it",
            "I agree with you",
            "That's so true",
            "that's for sure",
            "for sure",
            "you are absolutely right",
            "absolutely",
            "that's exactly how i feel",
            "i suppose so",
            "i guess so",
            "you have a point there",
            "yes",
            "let's give it a try",
            "that sounds like a good idea",
            "can you hook me up",
            "please do",
            "you read my mind",
            "i was just going to say that",
            "good idea",
            "good call"
        ],
        "disagreement": [
            "i don't think so",
            "no",
            "nope",
            "nah",
            "no way",
            "i disagree",
            "that is not necessary",
            "not necessarily",
            "that's not true",
            "i am not sure about that",
            "let's hold off on that for now",
            "hold that thought",
            "we can come back to this later",
            "let's revisit this later",
            "bad idea",
            "bad call"
        ]
    },
    "train_with_existing": True
}

test_predict_request = {"sentences": ["what's going on"]}
