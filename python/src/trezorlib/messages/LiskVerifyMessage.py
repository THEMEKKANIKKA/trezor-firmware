# Automatically generated by pb2py
# fmt: off
from .. import protobuf as p

if __debug__:
    try:
        from typing import Dict, List  # noqa: F401
        from typing_extensions import Literal  # noqa: F401
    except ImportError:
        pass


class LiskVerifyMessage(p.MessageType):
    MESSAGE_WIRE_TYPE = 120

    def __init__(
        self,
        public_key: bytes = None,
        signature: bytes = None,
        message: bytes = None,
    ) -> None:
        self.public_key = public_key
        self.signature = signature
        self.message = message

    @classmethod
    def get_fields(cls) -> Dict:
        return {
            1: ('public_key', p.BytesType, 0),
            2: ('signature', p.BytesType, 0),
            3: ('message', p.BytesType, 0),
        }
