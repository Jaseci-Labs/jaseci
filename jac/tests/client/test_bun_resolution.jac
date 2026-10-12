"""Bun is an artifact the router resolves: the sealed image's, the checkout's
(fetched by `jac native build bun`) or the kit's, each accepted only when its
record names the pinned version. Nothing scans PATH."""

import json;
import os;
import from tempfile { TemporaryDirectory }
import from jaclang.artifacts.model { Source }
import from jaclang.client.js_runtime {
    BUN_VERSION,
    RECORD_SUFFIX,
    _probe_bun,
    write_bun_record
}

def _fake_bun(directory: str) -> str {
    path = os.path.join(directory, "bun");
    with open(path, "w") as f {
        f.write("#!/bin/sh\nexit 0\n");
    }
    return path;
}

test "a bun carrying the pinned version's record is current, and made executable" {
    with TemporaryDirectory() as td {
        bun = _fake_bun(td);
        write_bun_record(bun);
        found = _probe_bun(bun, Source.CHECKOUT);
        assert found.found is not None and found.found.path == bun;
        assert os.access(bun, os.X_OK);
    }
}

test "a bun of another or unknown version is stale" {
    with TemporaryDirectory() as td {
        bun = _fake_bun(td);
        unrecorded = _probe_bun(bun, Source.CHECKOUT);
        assert unrecorded.found is None and "unknown version" in unrecorded.drift[0];
        with open(bun + RECORD_SUFFIX, "w") as f {
            json.dump({"version": "0.0.1"}, f);
        }
        old = _probe_bun(bun, Source.CHECKOUT);
        assert old.found is None and BUN_VERSION in old.drift[0];
    }
}

test "a missing bun is missing" {
    with TemporaryDirectory() as td {
        assert _probe_bun(os.path.join(td, "bun"), Source.CHECKOUT).absent;
    }
}
