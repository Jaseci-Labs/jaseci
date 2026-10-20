import from bcrypt {
    def BCryptOpenAlgorithmProvider(
        provider: bytes, algorithm: bytes, implementation: int, flags: u32
    ) -> i32;
}
import from bcrypt {
    def BCryptCreateHash(
        provider: int,
        hash: bytes,
        work: int,
        work_size: u32,
        secret: int,
        secret_size: u32,
        flags: u32
    ) -> i32;
}
import from bcrypt {
    def BCryptHashData(hash: int, data: bytes, n: u32, flags: u32) -> i32;
}
import from bcrypt {
    def BCryptDuplicateHash(
        hash: int, copy: bytes, work: int, work_size: u32, flags: u32
    ) -> i32;
}
import from bcrypt {
    def BCryptFinishHash(hash: int, out: bytes, n: u32, flags: u32) -> i32;
}
import from bcrypt { def BCryptDestroyHash(hash: int) -> i32;  }
import from c { def memchr(s: bytes, c: i32, n: u64) -> int;  }
import from bcrypt {
    def BCryptGetProperty(
        object: int, property: bytes, out: bytes, n: u32, written: bytes, flags: u32
    ) -> i32;
}

glob _BCRYPT_ALG_HANDLE_HMAC_FLAG: int = 8,
     _HASH_CHUNK: int = 1073741824;

glob _providers: dict[int, int] = {};

glob _HASH_LENGTH: bytes = b"H\x00a\x00s\x00h\x00D\x00i\x00g\x00e\x00s\x00t\x00L\x00e\x00n\x00g\x00t\x00h\x00\x00\x00";

def _digest_index(name: str) -> int;

def _algorithm_id(index: int) -> bytes;

def _provider(index: int, keyed: bool) -> int;

def:pub evp_md_for(name: str) -> int;


def:pub digest_size_for(name: str) -> int;


def:pub block_size_for(name: str) -> int;


def:pub ctx_require(ctx: int, what: str);


def _hash_new(index: int, key: bytes, keyed: bool) -> int;

def _hash_update(ctx: int, data: bytes);

def _hash_clone(ctx: int) -> int;

def _hash_digest(ctx: int) -> bytes;

def:pub evp_ctx_new(md: int) -> int;


def:pub evp_ctx_update(ctx: int, data: bytes);


def:pub evp_ctx_clone(ctx: int) -> int;


def:pub evp_ctx_digest(ctx: int) -> bytes;


def:pub evp_ctx_free(ctx: int);


def:pub hmac_ctx_new(md: int, key: bytes) -> int;


def:pub hmac_ctx_update(ctx: int, data: bytes);


def:pub hmac_ctx_clone(ctx: int) -> int;


def:pub hmac_ctx_digest(ctx: int) -> bytes;


def:pub hmac_ctx_free(ctx: int);

impl _digest_index(name: str) -> int {
    if name == "md5" {
        return 1;
    } elif name == "sha1" {
        return 2;
    } elif name == "sha256" {
        return 3;
    } elif name == "sha384" {
        return 4;
    } elif name == "sha512" {
        return 5;
    } elif name == "sha3_256" {
        return 6;
    } elif name == "sha3_384" {
        return 7;
    } elif name == "sha3_512" {
        return 8;
    }
    return 0;
}

impl _algorithm_id(index: int) -> bytes {
    if index == 1 {
        return b"M\x00D\x005\x00\x00\x00";
    } elif index == 2 {
        return b"S\x00H\x00A\x001\x00\x00\x00";
    } elif index == 3 {
        return b"S\x00H\x00A\x002\x005\x006\x00\x00\x00";
    } elif index == 4 {
        return b"S\x00H\x00A\x003\x008\x004\x00\x00\x00";
    } elif index == 5 {
        return b"S\x00H\x00A\x005\x001\x002\x00\x00\x00";
    } elif index == 6 {
        return b"S\x00H\x00A\x003\x00-\x002\x005\x006\x00\x00\x00";
    } elif index == 7 {
        return b"S\x00H\x00A\x003\x00-\x003\x008\x004\x00\x00\x00";
    } elif index == 8 {
        return b"S\x00H\x00A\x003\x00-\x005\x001\x002\x00\x00\x00";
    }
    return b"";
}

impl _provider(index: int, keyed: bool) -> int {
    slot: int = index * 2 + (1 if keyed else 0);
    if slot in _providers {
        return _providers[slot];
    }
    handle = b"\x00" * 8;
    flags: int = _BCRYPT_ALG_HANDLE_HMAC_FLAG if keyed else 0;
    opened: int = 0;
    if BCryptOpenAlgorithmProvider(handle, _algorithm_id(index), 0, u32(flags)) == 0 {
        opened = int.from_bytes(handle, "little");
    }
    _providers[slot] = opened;
    return opened;
}

impl evp_md_for(name: str) -> int {
    index: int = _digest_index(name);
    if index == 0 or _provider(index, False) == 0 {
        return 0;
    }
    return index;
}


impl digest_size_for(name: str) -> int {
    if name == "md5" {
        return 16;
    } elif name == "sha1" {
        return 20;
    } elif name == "sha224" {
        return 28;
    } elif name == "sha256" {
        return 32;
    } elif name == "sha384" {
        return 48;
    } elif name == "sha512" {
        return 64;
    } elif name == "sha3_224" {
        return 28;
    } elif name == "sha3_256" {
        return 32;
    } elif name == "sha3_384" {
        return 48;
    } elif name == "sha3_512" {
        return 64;
    } elif name == "blake2b" {
        return 64;
    } elif name == "blake2s" {
        return 32;
    }
    return 0;
}


impl block_size_for(name: str) -> int {
    if name == "md5" {
        return 64;
    } elif name == "sha1" {
        return 64;
    } elif name == "sha224" {
        return 64;
    } elif name == "sha256" {
        return 64;
    } elif name == "sha384" {
        return 128;
    } elif name == "sha512" {
        return 128;
    } elif name == "sha3_224" {
        return 144;
    } elif name == "sha3_256" {
        return 136;
    } elif name == "sha3_384" {
        return 104;
    } elif name == "sha3_512" {
        return 72;
    } elif name == "blake2b" {
        return 128;
    } elif name == "blake2s" {
        return 64;
    }
    return 0;
}


impl ctx_require(ctx: int, what: str) {
    if ctx == 0 {
        raise ValueError(what + " object is finalized");
    }
}


impl _hash_new(index: int, key: bytes, keyed: bool) -> int {
    provider: int = _provider(index, keyed);
    if provider == 0 {
        raise ValueError("the system has no provider for this digest");
    }
    secret: int = 0;
    if keyed and len(key) > 0 {
        secret = memchr(key, i32(key[0]), u64(1));
    }
    handle = b"\x00" * 8;
    if BCryptCreateHash(provider, handle, 0, u32(0), secret, u32(len(key)), u32(0))
        != 0 {
        raise ValueError("BCryptCreateHash failed");
    }
    return int.from_bytes(handle, "little");
}

impl _hash_update(ctx: int, data: bytes) {
    total: int = len(data);
    if total <= _HASH_CHUNK {
        if BCryptHashData(ctx, data, u32(total), u32(0)) != 0 {
            raise ValueError("BCryptHashData failed");
        }
        return;
    }
    done: int = 0;
    while done < total {
        step: int = total - done;
        if step > _HASH_CHUNK {
            step = _HASH_CHUNK;
        }
        if BCryptHashData(ctx, data[done:done + step], u32(step), u32(0)) != 0 {
            raise ValueError("BCryptHashData failed");
        }
        done += step;
    }
}

impl _hash_clone(ctx: int) -> int {
    handle = b"\x00" * 8;
    if BCryptDuplicateHash(ctx, handle, 0, u32(0), u32(0)) != 0 {
        raise ValueError("BCryptDuplicateHash failed");
    }
    return int.from_bytes(handle, "little");
}

impl _hash_digest(ctx: int) -> bytes {
    size = b"\x00" * 4;
    written = b"\x00" * 4;
    if BCryptGetProperty(ctx, _HASH_LENGTH, size, u32(4), written, u32(0)) != 0 {
        raise ValueError("BCryptGetProperty failed");
    }
    n: int = int.from_bytes(size, "little");
    tmp: int = _hash_clone(ctx);
    out = b"\x00" * n;
    status: int = int(BCryptFinishHash(tmp, out, u32(n), u32(0)));
    BCryptDestroyHash(tmp);
    if status != 0 {
        raise ValueError("BCryptFinishHash failed");
    }
    return out;
}

impl evp_ctx_new(md: int) -> int {
    return _hash_new(md, b"", False);
}


impl evp_ctx_update(ctx: int, data: bytes) {
    _hash_update(ctx, data);
}


impl evp_ctx_clone(ctx: int) -> int {
    return _hash_clone(ctx);
}


impl evp_ctx_digest(ctx: int) -> bytes {
    return _hash_digest(ctx);
}


impl evp_ctx_free(ctx: int) {
    BCryptDestroyHash(ctx);
}


impl hmac_ctx_new(md: int, key: bytes) -> int {
    return _hash_new(md, key, True);
}


impl hmac_ctx_update(ctx: int, data: bytes) {
    _hash_update(ctx, data);
}


impl hmac_ctx_clone(ctx: int) -> int {
    return _hash_clone(ctx);
}


impl hmac_ctx_digest(ctx: int) -> bytes {
    return _hash_digest(ctx);
}


impl hmac_ctx_free(ctx: int) {
    BCryptDestroyHash(ctx);
}
