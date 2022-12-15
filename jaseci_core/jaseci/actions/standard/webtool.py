"""Built in actions for Jaseci"""
from fastapi import HTTPException
from jaseci.actions.live_actions import jaseci_action
import metadata_parser


@jaseci_action()
def get_page_meta(url: str = ""):
    """
    Util to parse metadata out of urls and html documents
    """

    if url == "":
        raise HTTPException(status_code=400, detail=str("No url provided"))

    page = metadata_parser.MetadataParser(url=url)
    return page.metadata
