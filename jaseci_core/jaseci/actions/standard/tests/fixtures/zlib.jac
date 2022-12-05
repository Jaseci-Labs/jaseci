global data_uncompressed = "iVBORw0KGgoAAAANSUhEUgAAAAgAAAAIAQMAAAD+wSzIAAAABlBMVEX///+/v7+jQ3Y5AAAADklEQVQI12P4AIX8EAgALgAD/aNpbtEAAAAASUVORK5CYII=";

walker compress_test {
    report zlib.compress(global.data_uncompressed);
}

global data_compressed = "eJzrDPBz5+WS4mJgYOD19HAJAtIcIMzIDCT/HdQ5AaTYAnxCXP///79///7FzmWWQBE+TxfHEI7ryT8YWv8IcDDoMTD/XZyZdxEow+Dp6ueyzimhCQDLCRkd";

walker decompress_test {
    report zlib.decompress(global.data_compressed);
}