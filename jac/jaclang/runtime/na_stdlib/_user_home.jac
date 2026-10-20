import struct;
import from c { def getuid -> u32;  }
import from c {
    def getpwuid_r(
        uid: u32, record: bytes, buffer: bytes, size: u64, result: bytes
    ) -> i32;
}
import from c {
    def getpwnam_r(
        name: str, record: bytes, buffer: bytes, size: u64, result: bytes
    ) -> i32;
}
import from c { def strlen(pointer: int) -> u64;  }
import from c { def memcpy(target: bytes, source: int, length: u64) -> int;  }

def:pub user_home(name: str) -> str | None;
