import from "@jac/runtime" { __getApiBaseUrl }
import from "@noble/hashes/sha2.js" { sha256 }
import from "@noble/hashes/utils.js" { utf8ToBytes, bytesToHex }

async def:pub register_with_challenge(username: str, password: str) -> str;
