"""PDF documents: how a `Document` reaches the model, and what it refuses.

Assert on the request byLLM actually sent, not on a rendered string.
"""

import base64;
import os;
import tempfile;
import from jaclang.byllm.lib { Document, MockLLM }
import from support { call, document_blocks, roles, say, sent_messages, user_blocks }


glob PDF: bytes = b"%PDF-1.4\n1 0 obj\n<< /Type /Catalog >>\nendobj\ntrailer\n<< /Root 1 0 R >>\n%%EOF\n";

def _pdf_data_url(raw: bytes) -> str {
    return "data:application/pdf;base64," + base64.b64encode(raw).decode("utf-8");
}

def _write(name: str, raw: bytes) -> str {
    path = os.path.join(tempfile.mkdtemp(prefix="doc-"), name);
    with open(path, "wb") as f {
        f.write(raw);
    }
    return path;
}


test "a PDF path is sent as one file block carrying its data url and file name" {
    llm = MockLLM(outputs=[say("PINEAPPLE")]);

    def read_secret(brief: Document) -> str by llm();

    path = _write("brief.pdf", PDF);
    assert read_secret(Document(path)) == "PINEAPPLE";
    assert roles(llm) == ["system", "user"] , f"got {roles(llm)}";
    assert document_blocks(llm)
        == [
            {
                "type": "file",
                "file": {"file_data": _pdf_data_url(PDF), "filename": "brief.pdf"}
            }
        ] , f"got {user_blocks(llm)}";
    assert user_blocks(llm)[0]["type"] == "text" , (
        f"the caller name introduces the argument, got {user_blocks(llm)[0]}"
    );
}


test "PDF bytes carry no file name unless one is given" {
    llm = MockLLM(outputs=[say("ok"), say("ok")]);

    def read_secret(brief: Document) -> str by llm();

    assert read_secret(Document(PDF)) == "ok";
    assert document_blocks(llm, 0)
        == [{"type": "file", "file": {"file_data": _pdf_data_url(PDF)}}] , f"got {document_blocks(
        llm, 0
    )}";

    assert read_secret(Document(PDF, filename="spec.pdf")) == "ok";
    assert document_blocks(llm, 1)[0]["file"]["filename"] == "spec.pdf" , (
        f"got {document_blocks(llm, 1)}"
    );
}


test "an explicit file name wins over the path's" {
    doc = Document(_write("tmp_1234.pdf", PDF), filename="Q3 brief.pdf");
    assert doc.to_dict()[0]["file"]["filename"] == "Q3 brief.pdf";
}


test "the content decides, not the extension" {
    no_extension = Document(_write("brief", PDF));
    assert no_extension.to_dict()[0]["file"]["file_data"] == _pdf_data_url(PDF);

    for (name, raw) in [
        ("notes.pdf", b"# Notes\nThe secret word is MANGO.\n"),
        ("notes.md", b"# Notes\n"),
        ("empty.pdf", b"")
    ] {
        try {
            Document(_write(name, raw));
            assert False , f"{name}: a non-PDF must be refused";
        } except ValueError as e {
            assert "PDF" in str(e) , f"{name}: got {e}";
            assert "Text" in str(e) , f"{name}: the error points to Text, got {e}";
        }
    }
}


test "non-PDF bytes are refused before any call is made" {
    llm = MockLLM(outputs=[say("never sent")]);
    try {
        Document(b"\x89PNG\r\n\x1a\n");
        assert False , "image bytes must be refused";
    } except ValueError as e {
        assert "PDF" in str(e) , f"got {e}";
    }
    assert len(llm.seen) == 0;
}


test "a missing file and an unsupported input type fail with their own errors" {
    try {
        Document(os.path.join(tempfile.mkdtemp(prefix="doc-"), "absent.pdf"));
        assert False , "a missing file must be refused";
    } except ValueError as e {
        assert "does not exist" in str(e) , f"got {e}";
    }
    for bad in [42, None, ["%PDF-"]] {
        try {
            Document(bad);
            assert False , f"{bad!r}: an unsupported input must be refused";
        } except TypeError as e {
            assert "Document" in str(e) , f"{bad!r}: got {e}";
        }
    }
}


test "a document a tool returns reaches the model in a user turn, not in the tool message" {
    llm = MockLLM(outputs=[call("fetch_brief", {}, call_id="c1"), say("PINEAPPLE")]);

    def fetch_brief -> Document {
        return Document(PDF, filename="brief.pdf");
    }

    def summarise(topic: str) -> str by llm(tools=[fetch_brief]);

    assert summarise("the brief") == "PINEAPPLE";
    second = sent_messages(llm, 1);
    tool = [
        m
        for m in second
        if m["role"] == "tool"
    ];
    assert len(tool) == 1 , f"got {[m['role'] for m in second]}";
    in_tool = [
        b
        for b in (tool[0]["content"] if isinstance(tool[0]["content"], list) else [])
        if b.get("type") == "file"
    ];
    assert in_tool == [] , f"the file must not stay inside the tool message: {tool[0]}";

    assert second[-1]["role"] == "user" , f"got {[m['role'] for m in second]}";
    assert [
        b
        for b in second[-1]["content"]
        if b.get("type") == "file"
    ]
        == [
            {
                "type": "file",
                "file": {"file_data": _pdf_data_url(PDF), "filename": "brief.pdf"}
            }
        ] , f"got {second[-1]}";
}
