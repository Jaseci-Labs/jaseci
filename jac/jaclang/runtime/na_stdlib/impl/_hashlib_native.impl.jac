impl evp_md_for(name: str) -> int {
    if name == "md5" {
        return EVP_md5();
    } elif name == "sha1" {
        return EVP_sha1();
    } elif name == "sha224" {
        return EVP_sha224();
    } elif name == "sha256" {
        return EVP_sha256();
    } elif name == "sha384" {
        return EVP_sha384();
    } elif name == "sha512" {
        return EVP_sha512();
    } elif name == "sha3_224" {
        return EVP_sha3_224();
    } elif name == "sha3_256" {
        return EVP_sha3_256();
    } elif name == "sha3_384" {
        return EVP_sha3_384();
    } elif name == "sha3_512" {
        return EVP_sha3_512();
    } elif name == "blake2b" {
        return EVP_blake2b512();
    } elif name == "blake2s" {
        return EVP_blake2s256();
    }
    return 0;
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

impl evp_ctx_new(md: int) -> int {
    ctx: int = EVP_MD_CTX_new();
    if ctx == 0 {
        raise ValueError("EVP_MD_CTX_new failed (out of memory)");
    }
    if EVP_DigestInit_ex(ctx, md, 0) != 1 {
        EVP_MD_CTX_free(ctx);
        raise ValueError("EVP_DigestInit_ex failed");
    }
    return ctx;
}

impl evp_ctx_update(ctx: int, data: bytes) {
    if EVP_DigestUpdate(ctx, data, u64(len(data))) != 1 {
        raise ValueError("EVP_DigestUpdate failed");
    }
}

impl evp_ctx_clone(ctx: int) -> int {
    tmp: int = EVP_MD_CTX_new();
    if tmp == 0 {
        raise ValueError("EVP_MD_CTX_new failed (out of memory)");
    }
    if EVP_MD_CTX_copy_ex(tmp, ctx) != 1 {
        EVP_MD_CTX_free(tmp);
        raise ValueError("EVP_MD_CTX_copy_ex failed");
    }
    return tmp;
}

impl evp_ctx_digest(ctx: int) -> bytes {
    tmp: int = evp_ctx_clone(ctx);
    out = b"\x00" * _EVP_MAX_MD_SIZE;

    outlen = b"\x00" * 4;
    if EVP_DigestFinal_ex(tmp, out, outlen) != 1 {
        EVP_MD_CTX_free(tmp);
        raise ValueError("EVP_DigestFinal_ex failed");
    }
    EVP_MD_CTX_free(tmp);
    return out[0:int.from_bytes(outlen, "little")];
}

impl evp_ctx_free(ctx: int) {
    EVP_MD_CTX_free(ctx);
}

impl hmac_ctx_new(md: int, key: bytes) -> int {
    ctx: int = HMAC_CTX_new();
    if ctx == 0 {
        raise ValueError("HMAC_CTX_new failed (out of memory)");
    }
    if HMAC_Init_ex(ctx, key, i32(len(key)), md, 0) != 1 {
        HMAC_CTX_free(ctx);
        raise ValueError("HMAC_Init_ex failed");
    }
    return ctx;
}

impl hmac_ctx_update(ctx: int, data: bytes) {
    if HMAC_Update(ctx, data, u64(len(data))) != 1 {
        raise ValueError("HMAC_Update failed");
    }
}

impl hmac_ctx_clone(ctx: int) -> int {
    tmp: int = HMAC_CTX_new();
    if tmp == 0 {
        raise ValueError("HMAC_CTX_new failed (out of memory)");
    }
    if HMAC_CTX_copy(tmp, ctx) != 1 {
        HMAC_CTX_free(tmp);
        raise ValueError("HMAC_CTX_copy failed");
    }
    return tmp;
}

impl hmac_ctx_digest(ctx: int) -> bytes {
    tmp: int = hmac_ctx_clone(ctx);
    out = b"\x00" * _EVP_MAX_MD_SIZE;

    outlen = b"\x00" * 4;
    if HMAC_Final(tmp, out, outlen) != 1 {
        HMAC_CTX_free(tmp);
        raise ValueError("HMAC_Final failed");
    }
    HMAC_CTX_free(tmp);
    return out[0:int.from_bytes(outlen, "little")];
}

impl hmac_ctx_free(ctx: int) {
    HMAC_CTX_free(ctx);
}
