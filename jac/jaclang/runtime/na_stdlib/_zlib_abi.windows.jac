"""The layout of zlib's `z_stream` on Windows, where `unsigned long` is 32
bits (LLP64): the running totals are 32 bits wide, each packs beside the
count before it, and the record is 88 bytes."""

glob:pub ZS_NEXT_IN: int = 0,
     ZS_AVAIL_IN: int = 8,
     ZS_TOTAL_IN: int = 12,
     ZS_NEXT_OUT: int = 16,
     ZS_AVAIL_OUT: int = 24,
     ZS_TOTAL_OUT: int = 28,
     Z_STREAM_SIZE: int = 88;

"""A running total (`total_in` or `total_out`) at `addr`."""
def:pub zs_load_total(addr: int) -> int {
    return int(__mem_load_i32(addr)) & 4294967295;
}
