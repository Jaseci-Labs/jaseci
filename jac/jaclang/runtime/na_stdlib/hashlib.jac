obj Hash {
    has _ctx: int,
        digest_size: int,
        block_size: int,
        name: str;

    def update(data: bytes);
    def digest -> bytes;
    def hexdigest -> str;
    def copy -> Hash;
    def drop;
}


def:pub new(name: str, data: bytes = b"") -> Hash;


def:pub md5(data: bytes = b"") -> Hash;


def:pub sha1(data: bytes = b"") -> Hash;


def:pub sha224(data: bytes = b"") -> Hash;


def:pub sha256(data: bytes = b"") -> Hash;


def:pub sha384(data: bytes = b"") -> Hash;


def:pub sha512(data: bytes = b"") -> Hash;


def:pub sha3_224(data: bytes = b"") -> Hash;


def:pub sha3_256(data: bytes = b"") -> Hash;


def:pub sha3_384(data: bytes = b"") -> Hash;


def:pub sha3_512(data: bytes = b"") -> Hash;


def:pub blake2b(data: bytes = b"") -> Hash;


def:pub blake2s(data: bytes = b"") -> Hash;

impl Hash.update(data: bytes) {
    ctx_require(self._ctx, "hash");
    evp_ctx_update(self._ctx, data);
}

impl Hash.digest -> bytes {
    ctx_require(self._ctx, "hash");
    return evp_ctx_digest(self._ctx);
}

impl Hash.hexdigest -> str {
    return to_hex(self.digest());
}

impl Hash.copy -> Hash {
    ctx_require(self._ctx, "hash");
    return Hash(
        _ctx=evp_ctx_clone(self._ctx),
        digest_size=self.digest_size,
        block_size=self.block_size,
        name=self.name
    );
}

impl Hash.drop {
    if self._ctx != 0 {
        evp_ctx_free(self._ctx);
        self._ctx = 0;
    }
}


impl new(name: str, data: bytes = b"") -> Hash {
    md: int = evp_md_for(name);
    if md == 0 {
        raise ValueError("unsupported hash type " + name);
    }
    h = Hash(
        _ctx=evp_ctx_new(md),
        digest_size=digest_size_for(name),
        block_size=block_size_for(name),
        name=name
    );
    h.update(data);
    return h;
}


impl md5(data: bytes = b"") -> Hash {
    return new("md5", data);
}


impl sha1(data: bytes = b"") -> Hash {
    return new("sha1", data);
}


impl sha224(data: bytes = b"") -> Hash {
    return new("sha224", data);
}


impl sha256(data: bytes = b"") -> Hash {
    return new("sha256", data);
}


impl sha384(data: bytes = b"") -> Hash {
    return new("sha384", data);
}


impl sha512(data: bytes = b"") -> Hash {
    return new("sha512", data);
}


impl sha3_224(data: bytes = b"") -> Hash {
    return new("sha3_224", data);
}


impl sha3_256(data: bytes = b"") -> Hash {
    return new("sha3_256", data);
}


impl sha3_384(data: bytes = b"") -> Hash {
    return new("sha3_384", data);
}


impl sha3_512(data: bytes = b"") -> Hash {
    return new("sha3_512", data);
}


impl blake2b(data: bytes = b"") -> Hash {
    return new("blake2b", data);
}


impl blake2s(data: bytes = b"") -> Hash {
    return new("blake2s", data);
}
