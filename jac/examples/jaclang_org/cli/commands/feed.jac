import from jaclang.server.bridge { BridgeError }

obj FeedLine {
    has author: str = "",
        content: str = "",
        created_at: str = "",
        likes: int = 0,
        comments: int = 0;
}


def render_line(line: FeedLine) -> str;

async def run_feed(limit: int, query: str) -> int;

async def run_post(text: str) -> int;
