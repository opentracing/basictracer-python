import random
import time

guid_rng = random.Random()

def generate_id():
    return guid_rng.getrandbits(64) - 1
