import mutators
import logger

MATCH_RESPONSE=1
MATCH_REQUEST=2

## Available mutators
# Simple Mutator - blabla
# Swap Mutator - blabla
# Overflow Mutator - blabla

#setup = [
#  {"mutator": mutators.OverflowMutator(), "match": "erostream", "endpoint": MATCH_REQUEST},
#  {"mutator": mutators.SwapMutator(), "match": "unknown", "endpoint": MATCH_REQUEST},
#  {"mutator": mutators.SimpleMutator(), "endpoint": MATCH_REQUEST},
#]

setup = [
	 {"target": ("127.0.0.1", 8888), "mutator": mutators.ReverseMutator(), "endpoint": MATCH_REQUEST, "logger": logger.BinaryLogger()}
]
