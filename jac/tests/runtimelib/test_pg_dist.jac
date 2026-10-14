"""The Postgres distribution resolves through the artifact router: a configured
dist wins, a cached one is found without the network, and a missing one is
provisioned loudly -- or refused in an offline project."""

import os;
import from pathlib { Path }
import from tempfile { TemporaryDirectory }
import from unittest.mock { patch }
import from jaclang.artifacts.model { ArtifactUnavailable, Source }
import from jaclang.artifacts.router { forget, require, resolve }
import from jaclang.project.config { DatabaseConfig, JacConfig }
import from tests.support { offline_project }

def _fake_dist(bin_dir: Path) -> Path {
    bin_dir.mkdir(parents=True);
    (bin_dir / "postgres").write_text("");
    return bin_dir;
}

def _project_config(project: Path, database: DatabaseConfig) -> JacConfig {
    config = JacConfig();
    config.project_root = project;
    config.database = database;
    return config;
}

def _resolve_in(cache: str, config: (JacConfig | None)) -> any {
    forget("postgres");
    with patch.dict(os.environ, {"JAC_CACHE_HOME": cache}), patch(
        "jaclang.project.config.get_config", return_value=config
    ), patch("jaclang.data.pg_dist._system", return_value=None) {
        return resolve("postgres");
    }
}

test "a configured distribution wins, relative to its project" {
    with TemporaryDirectory() as tmp {
        project = Path(tmp);
        _fake_dist(project / "pg" / "bin");
        resolution = _resolve_in(
            str(project / "cache"),
            _project_config(project, DatabaseConfig(postgres_dist="pg"))
        );
        assert resolution.found is not None;
        assert resolution.found.source == Source.CONFIGURED;
        assert resolution.found.path == str(project / "pg" / "bin");
    }
}

test "a configured distribution without binaries is named, not skipped" {
    with TemporaryDirectory() as tmp {
        project = Path(tmp);
        resolution = _resolve_in(
            str(project / "cache"),
            _project_config(project, DatabaseConfig(postgres_dist="nope"))
        );
        assert resolution.found is None;
        assert "postgres_dist" in resolution.reason , resolution.reason;
    }
}

test "a cached distribution of the pinned major is found without the network" {
    import from jaclang.data.pg_dist { PG_MAJOR, platform_slug }
    slug = platform_slug();
    if slug is None {
        return;
    }
    with TemporaryDirectory() as tmp {
        dist = Path(tmp) / "pg" / "dist";
        _fake_dist(dist / f"{slug}-{PG_MAJOR - 1}.4.0" / "bin");
        pinned = _fake_dist(dist / f"{slug}-{PG_MAJOR}.1.0" / "bin");
        with patch("jaclang.data.pg_dist._published", side_effect=AssertionError) {
            resolution = _resolve_in(tmp, None);
        }
        assert resolution.found is not None;
        assert resolution.found.source == Source.CACHE;
        assert resolution.found.path == str(pinned);
    }
}

test "an offline project refuses to provision a missing distribution" {
    with TemporaryDirectory() as tmp {
        forget("postgres");
        with patch.dict(os.environ, {"JAC_CACHE_HOME": tmp}), patch(
            "jaclang.project.config.get_config", return_value=None
        ), patch("jaclang.data.pg_dist._system", return_value=None), patch(
            "jaclang.data.pg_dist.download_dist", side_effect=AssertionError
        ), offline_project() {
            try {
                require("postgres");
                assert False , "an offline project must not provision";
            } except ArtifactUnavailable as e {
                assert "offline" in str(e) , str(e);
            }
        }
        forget("postgres");
    }
}

test "a missing distribution is provisioned once, loudly" {
    import from jaclang.data.pg_dist { platform_slug }
    slug = platform_slug();
    if slug is None {
        return;
    }
    with TemporaryDirectory() as tmp {
        calls: list[str] = [];
        def _download -> str {
            calls.append("download");
            return str(
                _fake_dist(Path(tmp) / "pg" / "dist" / f"{slug}-19.0.0" / "bin")
            );
        }
        forget("postgres");
        with patch.dict(os.environ, {"JAC_CACHE_HOME": tmp}), patch(
            "jaclang.project.config.get_config", return_value=None
        ), patch("jaclang.data.pg_dist._system", return_value=None), patch(
            "jaclang.data.pg_dist.download_dist", side_effect=_download
        ), patch("jaclang.project.config.offline_mode", return_value=False) {
            found = require("postgres").found;
            assert found is not None and found.source == Source.CACHE;
            require("postgres");
        }
        assert calls == ["download"] , calls;
        forget("postgres");
    }
}
