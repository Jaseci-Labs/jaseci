import from crypto { def EVP_MD_CTX_new -> int;  }
import from crypto { def EVP_MD_CTX_free(ctx: int) -> None;  }
import from crypto { def EVP_MD_CTX_copy_ex(dst: int, src: int) -> i32;  }
import from crypto { def EVP_DigestInit_ex(ctx: int, md: int, engine: int) -> i32;  }
import from crypto { def EVP_DigestUpdate(ctx: int, data: bytes, n: u64) -> i32;  }
import from crypto {
    def EVP_DigestFinal_ex(ctx: int, md_out: bytes, outlen: bytes) -> i32;
}

import from crypto { def EVP_md5 -> int;  }
import from crypto { def EVP_sha1 -> int;  }
import from crypto { def EVP_sha224 -> int;  }
import from crypto { def EVP_sha256 -> int;  }
import from crypto { def EVP_sha384 -> int;  }
import from crypto { def EVP_sha512 -> int;  }
import from crypto { def EVP_sha3_224 -> int;  }
import from crypto { def EVP_sha3_256 -> int;  }
import from crypto { def EVP_sha3_384 -> int;  }
import from crypto { def EVP_sha3_512 -> int;  }
import from crypto { def EVP_blake2b512 -> int;  }
import from crypto { def EVP_blake2s256 -> int;  }

import from crypto { def HMAC_CTX_new -> int;  }
import from crypto { def HMAC_CTX_free(ctx: int) -> None;  }
import from crypto { def HMAC_CTX_copy(dst: int, src: int) -> i32;  }
import from crypto {
    def HMAC_Init_ex(ctx: int, key: bytes, keylen: i32, md: int, engine: int) -> i32;
}
import from crypto { def HMAC_Update(ctx: int, data: bytes, n: u64) -> i32;  }
import from crypto { def HMAC_Final(ctx: int, md_out: bytes, outlen: bytes) -> i32;  }

glob _EVP_MAX_MD_SIZE: int = 64;

def:pub evp_md_for(name: str) -> int;


def:pub digest_size_for(name: str) -> int;


def:pub block_size_for(name: str) -> int;


def:pub ctx_require(ctx: int, what: str);


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
