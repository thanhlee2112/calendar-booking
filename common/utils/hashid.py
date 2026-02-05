from hashids import Hashids
from django.conf import settings

hashids = Hashids(salt=settings.SECRET_KEY, min_length=10)

def encode_id(id)->str:
    return hashids.encode(id)

def decode_id(hashid)->int:
    id = hashids.decode(hashid)
    if id:
        return id[0]
    else: 
        raise ValueError("Invalid hashid")