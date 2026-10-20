import os;
import tempfile;
import from contextlib { ExitStack }
import from pathlib { Path }
import from unittest.mock { patch }
import jaclang.byllm.model_cache as model_cache;
import from jaclang.byllm.model_cache { gguf_path }
import from jaclang.byllm.local_runtime { LOCAL_MODELS }
import from jaclang.byllm.cli { model }

glob ALIAS: str = "gemma-4-e2b",
     GOOD: bytes = b"GGUF" + bytes(range(60));

"""Point the cache at `<base>/models`, fake `_download` to record each call in `calls`
and, like huggingface_hub, write `GOOD` only where no file is, and give consent; return
the cache dir."""
def use_temp_cache(stack: ExitStack, base: Path, calls: list[str]) -> Path {
    cache_dir = base / "models";
    cache_dir.mkdir(parents=True);
    def fake_download(alias: str, spec: dict[str, any]) -> Path {
        calls.append(alias);
        target = gguf_path(alias, spec);
        target.parent.mkdir(parents=True, exist_ok=True);
        if not target.exists() {
            target.write_bytes(GOOD);
        }
        return target;
    }
    stack.enter_context(
        patch.object(model_cache, "get_cache_dir", return_value=cache_dir)
    );
    stack.enter_context(
        patch.object(model_cache, "_download", side_effect=fake_download)
    );
    stack.enter_context(patch.dict(os.environ, {"BYLLM_AUTO_DOWNLOAD": "1"}));
    return cache_dir;
}

test "jac model rm deletes only a known alias" {
    rows = [
        ("parent", "..", 2),
        ("current", ".", 2),
        ("empty", "", 2),
        ("hidden", ".hidden", 2),
        ("slash", f"{ALIAS}/../..", 2),
        ("alias", ALIAS, 0)
    ];
    for (label, name, want_rc) in rows {
        with tempfile.TemporaryDirectory() as tmp, ExitStack() as stack {
            base = Path(tmp);
            cache_dir = use_temp_cache(stack, base, []);
            weight = gguf_path(ALIAS, LOCAL_MODELS[ALIAS]);
            weight.parent.mkdir(parents=True);
            weight.write_bytes(GOOD);
            hidden = cache_dir / ".hidden" / "keep";
            hidden.parent.mkdir();
            hidden.write_bytes(b"keep");
            beside_cache = base / "other-cache-data";
            beside_cache.write_bytes(b"keep");
            rc = model("rm", name);
            assert rc == want_rc , f"{label}: exit code {rc}, expected {want_rc}";
            assert beside_cache.exists() , f"{label}: deleted data beside the model cache";
            assert hidden.exists() , f"{label}: deleted a hidden cache entry";
            if want_rc == 0 {
                assert not weight.parent.exists() , f"{label}: the alias was not deleted";
            } else {
                assert weight.exists() , f"{label}: deleted the cached weight";
            }
        }
    }
}

test "jac model pull replaces a bad weight and keeps a good one" {
    rows = [("good weight", GOOD, 0), ("junk bytes", b"junk", 1)];
    for (label, on_disk, want_downloads) in rows {
        with tempfile.TemporaryDirectory() as tmp, ExitStack() as stack {
            calls: list[str] = [];
            use_temp_cache(stack, Path(tmp), calls);
            weight = gguf_path(ALIAS, LOCAL_MODELS[ALIAS]);
            weight.parent.mkdir(parents=True);
            weight.write_bytes(on_disk);
            rc = model("pull", ALIAS);
            assert rc == 0 , f"{label}: exit code {rc}";
            downloads = len(calls);
            assert downloads == want_downloads , f"{label}: {downloads} downloads, expected {want_downloads}";
            assert weight.read_bytes() == GOOD , f"{label}: the weight is not the real file";
        }
    }
}
