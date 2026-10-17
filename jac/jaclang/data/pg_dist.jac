import logging;
import os;
import platform;
import shutil;
import subprocess;
import urllib.request;
import zipfile;
import from pathlib { Path }

glob logger = logging.getLogger(__name__),
     PG_MAJOR: int = 19,
     MIN_SYSTEM_MAJOR: int = 14,
     ZONKY_BASE: str = (
         'https://repo1.maven.org/maven2/io/zonky/test/postgres/'
         'embedded-postgres-binaries-'
     ),
     SYSTEM_ROOTS: tuple[str, ...] = (
         '/usr/lib/postgresql',
         '/usr/pgsql',
         '/opt/homebrew/opt'
     );

def _database_config -> (DatabaseConfig | None) {
    config = get_config();
    return config.database if config is not None else None;
}

def _configured_dist -> str {
    config = get_config();
    if config is None or not config.database.postgres_dist {
        return "";
    }
    dist = os.path.expanduser(config.database.postgres_dist);
    if config.project_root is not None {
        dist = os.path.join(str(config.project_root), dist);
    }
    return dist;
}

def pinned_major -> int {
    database = _database_config();
    wanted = database.postgres_version if database is not None else '';
    if wanted {
        try {
            return int(wanted.split('.')[0]);
        } except ValueError {
            logger.warning(
                f"[database] postgres_version {wanted!r} is not a version; using {PG_MAJOR}"
            );
        }
    }
    return PG_MAJOR;
}

def dist_cache_dir -> str {
    return str(bucket("pg").path() / 'dist');
}

def platform_slug -> (str | None) {
    arch = {
        'x86_64': 'amd64',
        'amd64': 'amd64',
        'aarch64': 'arm64v8',
        'arm64': 'arm64v8'
    }.get(
        platform.machine().lower()
    );
    system = {'Linux': 'linux', 'Darwin': 'darwin'}.get(platform.system());
    return f"{system}-{arch}" if arch and system else None;
}

def _bin_of(dist: str) -> (str | None) {
    for candidate in [os.path.join(dist, 'bin'), dist] {
        if os.path.isfile(os.path.join(candidate, 'postgres')) {
            return candidate;
        }
    }
    return None;
}

def pg_major_of(bin_dir: str) -> (int | None) {
    postgres = os.path.join(bin_dir, 'postgres');
    if not os.path.isfile(postgres) {
        return None;
    }
    try {
        out = subprocess.run(
            [postgres, '--version'], capture_output=True, text=True, timeout=10
        ).stdout.strip();
    } except (OSError, subprocess.SubprocessError) as e {
        logger.debug(f"pg version probe failed for {postgres}: {e}");
        return None;
    }
    for part in out.split() {
        if part[:1].isdigit() {
            digits = part.split('.')[0];
            return int(digits) if digits.isdigit() else None;
        }
    }
    return None;
}

def _version_key(version: str) -> tuple[int, ...] {
    return tuple(int(p) if p.isdigit() else 0 for p in version.split('.'));
}

def _cached(major: int) -> (str | None) {
    slug = platform_slug();
    cache = dist_cache_dir();
    if slug is None or not os.path.isdir(cache) {
        return None;
    }
    versions = [
        name[len(slug) + 1:]
        for name in os.listdir(cache)
        if name.startswith(slug + '-')
            and not name.endswith('.part')
            and os.path.isfile(os.path.join(cache, name, 'bin', 'postgres'))
    ];
    if not versions {
        return None;
    }
    pinned = [
        v
        for v in versions
        if v.split('.')[0] == str(major)
    ];
    best = max(pinned or versions, key=_version_key);
    return os.path.join(cache, f"{slug}-{best}", 'bin');
}

def _system(major: int) -> (str | None) {
    candidates: list[str] = [];
    exe = shutil.which('postgres');
    if exe {
        candidates.append(os.path.dirname(os.path.realpath(exe)));
    }
    for base in SYSTEM_ROOTS {
        if os.path.isdir(base) {
            for name in sorted(os.listdir(base), reverse=True) {
                cand = os.path.join(base, name, 'bin');
                if os.path.isfile(os.path.join(cand, 'postgres')) {
                    candidates.append(cand);
                }
            }
        }
    }
    best: (str | None) = None;
    best_major = 0;
    for cand in candidates {
        found = pg_major_of(cand);
        if found == major {
            return cand;
        }
        if found is not None and found >= MIN_SYSTEM_MAJOR and found > best_major {
            (best, best_major) = (cand, found);
        }
    }
    if best is not None {
        logger.warning(
            f"postgres {major} not found on the system; using the installed "
            f"postgres {best_major} at {best} (set [database] postgres_dist or "
            f"postgres_version to choose)"
        );
    }
    return best;
}

def _published(slug: str) -> list[str] {
    url = f"{ZONKY_BASE}{slug}/maven-metadata.xml";
    try {
        with urllib.request.urlopen(url, timeout=30) as response {
            body = response.read().decode('utf-8', errors='replace');
        }
    } except OSError as e {
        logger.debug(f"zonky metadata fetch failed: {e}");
        return [];
    }
    return [
        chunk.split('</version>')[0].strip() for chunk in body.split('<version>')[1:]
    ];
}

def _unpack(slug: str, version: str, dist_dir: str) {
    name = f"embedded-postgres-binaries-{slug}";
    jar_url = f"{ZONKY_BASE}{slug}/{version}/{name}-{version}.jar";
    with urllib.request.urlopen(jar_url + '.sha1', timeout=30) as response {
        want_sha = response.read().decode().strip().split()[0];
    }
    jar_path = fetch(Download("postgres", version, slug, jar_url, want_sha, "sha1"));
    with zipfile.ZipFile(jar_path) as jar {
        payloads = [
            n
            for n in jar.namelist()
            if n.endswith('.txz')
        ];
    }
    if not payloads {
        raise ArtifactUnavailable(f"no .txz payload in {jar_url}");
    }
    staging = dist_dir + '.part';
    shutil.rmtree(staging, ignore_errors=True);
    os.makedirs(staging);
    try {
        extract(jar_path, Path(staging));
        extract(Path(staging) / payloads[0], Path(staging));
        os.remove(os.path.join(staging, payloads[0]));
        os.replace(staging, dist_dir);
    } finally {
        shutil.rmtree(staging, ignore_errors=True);
    }
}

def download_dist -> str {
    slug = platform_slug();
    if slug is None {
        raise ArtifactUnavailable(
            f"no embedded postgres is published for {platform.system()} {platform.machine()}"
        );
    }
    published = _published(slug);
    want = pinned_major();
    versions = [
        v
        for v in published
        if v.split('.')[0] == str(want)
    ];
    if not versions and published {
        newest = max(
            {
                int(v.split('.')[0])
                for v in published
                if v[:1].isdigit()
            }
        );
        logger.warning(
            f"postgres {want} is not yet published to the embedded channel; using {newest}"
        );
        versions = [
            v
            for v in published
            if v.split('.')[0] == str(newest)
        ];
    }
    if not versions {
        raise ArtifactUnavailable(
            "the embedded postgres channel (Maven Central) is unreachable"
        );
    }
    version = versions[-1];
    dist_dir = os.path.join(dist_cache_dir(), f"{slug}-{version}");
    bin_dir = os.path.join(dist_dir, 'bin');
    os.makedirs(dist_cache_dir(), exist_ok=True);
    with FileLock(Path(dist_cache_dir()) / f".{slug}-{version}.lock") {
        if not os.path.isfile(os.path.join(bin_dir, 'postgres')) {
            logger.info(f"fetching embedded postgres {version} ({slug})...");
            _unpack(slug, version, dist_dir);
        }
    }
    return bin_dir;
}

obj PostgresArtifact(Artifact) {
    has name: str = "postgres",
        kind: ArtifactKind = ArtifactKind.CAPABILITY,
        release: ReleasePolicy = ReleasePolicy.ON_DEMAND,
        summary: str = "the embedded Postgres distribution",
        hosts: list[str] = ["linux", "darwin"],
        provision: bool = True;

    override def probe_checkout -> Probe {
        configured = _configured_dist();
        if configured {
            found = _bin_of(configured);
            return Probe.hit(Source.CONFIGURED, found, {})
                if found
                else Probe.missing(
                    f"[database] postgres_dist {configured!r} has no bin/postgres"
                );
        }
        major = pinned_major();
        found = _cached(major);
        if found is not None {
            return Probe.hit(Source.CACHE, found, {});
        }
        found = _system(major);
        if found is not None {
            return Probe.hit(Source.SYSTEM, found, {});
        }
        return Probe.missing(f"postgres {major} is not provisioned");
    }

    override def checkout_path -> str {
        return dist_cache_dir();
    }

    override def build(log: Callable[[str], None], force: bool, exact: bool) {
        log(f"  postgres {pinned_major()} -> {download_dist()}");
    }
}

def postgres_bin_dir -> str {
    found = require("postgres").found;
    assert found is not None;
    return found.path;
}
