import requests
import os
import re
import uuid

from jaseci.actions.live_actions import jaseci_action
from PyPDF2 import PdfFileReader
from fastapi import HTTPException


def download_pdf(url: str, filename: str):
    r"""method for downloading PDF from URL
    :param url: URL for the downloading a pdf file.
    :param filename: filename for saveing downloaded pdf locally.
    """
    with requests.get(url, stream=True) as req:
        req.raise_for_status()
        with open(filename, "wb") as f:
            for chunk in req.iter_content(chunk_size=2048):
                f.write(chunk)


def valid_url(url: str):
    r"""validating whether given url is a valid pdf url or not
    :param url: URL for the downloading a pdf file.
    """
    r = requests.get(url)
    content_type = r.headers.get("content-type")
    return True if "application/pdf" in content_type else False


def remove_pdf(filename: str):
    r"""REMOVE locally downloaded PDF
    :param filename: filename for the deleting pdf file.
    """
    if os.path.exists(filename):
        os.remove(filename)
        return True
    return False


@jaseci_action(act_group=["pdf_ext"], allow_remote=True)
def extract_pdf(url: str, metadata: bool = False):
    r"""REMOVE locaaly downloaded PDF
    :param filename: filename for the deleting pdf file.
    :param metadata: boolean if you want to diaplay available metadata of PDF.
    """
    filename = str(uuid.uuid4().hex) + ".pdf"
    data = {"pages": 0, "content": None}
    if valid_url(url):
        try:
            download_pdf(url, filename)
            with open(filename, "rb") as pdf_file:
                pdf_reader = PdfFileReader(pdf_file)
                if metadata:
                    data.update({"metadata": {}})
                    md = dict(pdf_reader.documentInfo)
                    for k, v in md.items():
                        data["metadata"][re.sub("[^a-zA-Z0-9]+", "", k)] = v
                data["pages"] = len(pdf_reader.pages)
                data["content"] = [page.extractText() for page in pdf_reader.pages]
            remove_pdf(filename)
            return data
        except Exception:
            remove_pdf(filename)
            raise HTTPException(
                status_code=500, detail="Unable to extract data from pdf"
            )
    else:
        raise HTTPException(status_code=415, detail=str("Invalid file format"))


if __name__ == "__main__":
    from jaseci.actions.remote_actions import launch_server

    launch_server(port=8000)
