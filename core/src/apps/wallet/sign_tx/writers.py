from micropython import const

from trezor.crypto.hashlib import sha256
from trezor.messages.TxInputType import TxInputType
from trezor.messages.TxOutputBinType import TxOutputBinType
from trezor.utils import ensure

from apps.common.writers import (  # noqa: F401
    empty_bytearray,
    write_bytes_fixed,
    write_bytes_reversed,
    write_bytes_unchecked,
    write_uint8,
    write_uint16_le,
    write_uint32_le,
    write_uint64_le,
)

if False:
    from apps.common.writers import Writer

write_uint16 = write_uint16_le
write_uint32 = write_uint32_le
write_uint64 = write_uint64_le

TX_HASH_SIZE = const(32)


def write_bytes_prefixed(w: Writer, b: bytes) -> None:
    write_varint(w, len(b))
    write_bytes_unchecked(w, b)


def write_tx_input(w, i: TxInputType):
    write_bytes_reversed(w, i.prev_hash, TX_HASH_SIZE)
    write_uint32(w, i.prev_index)
    write_bytes_prefixed(w, i.script_sig)
    write_uint32(w, i.sequence)


def write_tx_input_check(w, i: TxInputType):
    write_bytes_fixed(w, i.prev_hash, TX_HASH_SIZE)
    write_uint32(w, i.prev_index)
    write_uint32(w, i.script_type)
    write_uint32(w, len(i.address_n))
    for n in i.address_n:
        write_uint32(w, n)
    write_uint32(w, i.sequence)
    write_uint64(w, i.amount or 0)


def write_tx_input_decred(w, i: TxInputType):
    write_bytes_reversed(w, i.prev_hash, TX_HASH_SIZE)
    write_uint32(w, i.prev_index or 0)
    write_uint8(w, i.decred_tree or 0)
    write_uint32(w, i.sequence)


def write_tx_input_decred_witness(w, i: TxInputType):
    write_uint64(w, i.amount or 0)
    write_uint32(w, 0)  # block height fraud proof
    write_uint32(w, 0xFFFFFFFF)  # block index fraud proof
    write_bytes_prefixed(w, i.script_sig)


def write_tx_output(w, o: TxOutputBinType):
    write_uint64(w, o.amount)
    if o.decred_script_version is not None:
        write_uint16(w, o.decred_script_version)
    write_bytes_prefixed(w, o.script_pubkey)


def write_op_push(w, n: int):
    ensure(n >= 0 and n <= 0xFFFFFFFF)
    if n < 0x4C:
        w.append(n & 0xFF)
    elif n < 0xFF:
        w.append(0x4C)
        w.append(n & 0xFF)
    elif n < 0xFFFF:
        w.append(0x4D)
        w.append(n & 0xFF)
        w.append((n >> 8) & 0xFF)
    else:
        w.append(0x4E)
        w.append(n & 0xFF)
        w.append((n >> 8) & 0xFF)
        w.append((n >> 16) & 0xFF)
        w.append((n >> 24) & 0xFF)


def write_varint(w, n: int):
    ensure(n >= 0 and n <= 0xFFFFFFFF)
    if n < 253:
        w.append(n & 0xFF)
    elif n < 0x10000:
        w.append(253)
        w.append(n & 0xFF)
        w.append((n >> 8) & 0xFF)
    else:
        w.append(254)
        w.append(n & 0xFF)
        w.append((n >> 8) & 0xFF)
        w.append((n >> 16) & 0xFF)
        w.append((n >> 24) & 0xFF)


def get_tx_hash(w, double: bool = False, reverse: bool = False) -> bytes:
    d = w.get_digest()
    if double:
        d = sha256(d).digest()
    if reverse:
        d = bytes(reversed(d))
    return d
