from jaseci.utils.test_core import CoreTest, jac_testcase


class ZlibTest(CoreTest):
    fixture_src = __file__

    data_uncompressed = "iVBORw0KGgoAAAANSUhEUgAAAAgAAAAIAQMAAAD+wSzIAAAABlBMVEX///+/v7+jQ3Y5AAAADklEQVQI12P4AIX8EAgALgAD/aNpbtEAAAAASUVORK5CYII="
    data_compressed = "eJzrDPBz5+WS4mJgYOD19HAJAtIcIMzIDCT/HdQ5AaTYAnxCXP///79///7FzmWWQBE+TxfHEI7ryT8YWv8IcDDoMTD/XZyZdxEow+Dp6ueyzimhCQDLCRkd"

    @jac_testcase("zlib.jac", "compress_test", True)
    def test_compress(self, ret):
        print(ret["report"])
        self.assertEqual(
            ret["report"][0],
            self.data_compressed,
        )

    @jac_testcase("zlib.jac", "decompress_test")
    def test_decompress(self, ret):
        print(ret["report"])
        self.assertEqual(
            ret["report"][0],
            self.data_uncompressed,
        )
