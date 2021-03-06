from common import *

from trezor.messages.TxInputType import TxInputType
from trezor.messages import InputScriptType

from apps.common import coins
from apps.common.seed import Keychain
from apps.wallet.sign_tx import writers


class TestWriters(unittest.TestCase):
    def test_tx_input(self):
        inp = TxInputType(
            address_n=[0],
            amount=390000,
            prev_hash=unhexlify(
                "d5f65ee80147b4bcc70b75e4bbf2d7382021b871bd8867ef8fa525ef50864882"
            ),
            prev_index=0,
            sequence=0xffffffff,
            script_sig=b"0123456789",
        )

        b = bytearray()
        writers.write_tx_input(b, inp)
        self.assertEqual(len(b), 32 + 4 + 1 + 10 + 4)

        for bad_prevhash in (b"", b"x", b"hello", b"x" * 33):
            inp.prev_hash = bad_prevhash
            self.assertRaises(AssertionError, writers.write_tx_input, b, inp)

    def test_tx_input_check(self):
        inp = TxInputType(
            address_n=[0],
            amount=390000,
            prev_hash=unhexlify(
                "d5f65ee80147b4bcc70b75e4bbf2d7382021b871bd8867ef8fa525ef50864882"
            ),
            prev_index=0,
            script_type=InputScriptType.SPENDWITNESS,
            sequence=0xffffffff,
            script_sig=b"0123456789",
        )

        b = bytearray()
        writers.write_tx_input_check(b, inp)
        self.assertEqual(len(b), 32 + 4 + 4 + 4 + 4 + 4 + 8)

        for bad_prevhash in (b"", b"x", b"hello", b"x" * 33):
            inp.prev_hash = bad_prevhash
            self.assertRaises(AssertionError, writers.write_tx_input_check, b, inp)

if __name__ == "__main__":
    unittest.main()
