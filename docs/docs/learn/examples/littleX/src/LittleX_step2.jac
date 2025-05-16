node profile {
    has username: str = "";
    has count_tag: dict = {};
    has followees: list = [];
}

node tweet; # Declaration of tweet node

node comment {
    has content: str;
}

:node:tweet { # Definition of tweet node
    has content: str;
    has created_at: str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S");
}
