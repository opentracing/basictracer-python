import random

guid_rng = random.Random()

def generate_id():
    return guid_rng.getrandbits(64) - 1
