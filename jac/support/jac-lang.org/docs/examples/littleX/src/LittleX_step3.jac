node profile {
    has username: str = "";
    has count_tag: dict = {};
    has followees: list = [];
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
