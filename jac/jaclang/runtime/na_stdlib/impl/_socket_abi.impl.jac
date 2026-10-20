impl errno_pointer -> int {
    return __errno_location();
}

impl address_family(address: bytes) -> int {
    return address[0] + address[1] * 256;
}
