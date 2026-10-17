import struct;
import sys;

impl JirHeader.to_bytes -> bytes {
    return struct.pack(
        HEADER_FMT,
        self.magic,
        self.format_version,
        self.python_version,
        self.reserved,
        self.source_content_hash,
        self.node_count,
        self.symbol_count,
        self.string_pool_size,
        self.flags
    );
}

impl JirHeader.is_compatible -> bool {
    return self.python_version
        == ((sys.version_info.major << 8) | sys.version_info.minor);
}
