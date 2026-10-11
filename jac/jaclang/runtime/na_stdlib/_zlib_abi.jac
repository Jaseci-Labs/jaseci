"""The layout of zlib's `z_stream` where `unsigned long` is 64 bits (LP64:
Linux and macOS). `uLong` is `unsigned long`, so the running totals are 64
bits wide and the record is 112 bytes."""

glob:pub ZS_NEXT_IN: int = 0,
     ZS_AVAIL_IN: int = 8,
     ZS_TOTAL_IN: int = 16,
     ZS_NEXT_OUT: int = 24,
     ZS_AVAIL_OUT: int = 32,
     ZS_TOTAL_OUT: int = 40,
     Z_STREAM_SIZE: int = 112;

"""A running total (`total_in` or `total_out`) at `addr`."""
def:pub zs_load_total(addr: int) -> int {
    return __mem_load_i64(addr);
}
