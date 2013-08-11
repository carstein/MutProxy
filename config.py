import injectors

MATCH_RESPONSE=1
MATCH_REQUEST=2

## Available injectors
# Simple Injector - blabla
# Swap Injector - blabla
# Overflow Injector - blabla

setup = [
  {"injector": injectors.OverflowInjector(), "match": "erostream", "endpoint": MATCH_REQUEST},
  {"injector": injectors.SwapInjector(), "match": "unknown", "endpoint": MATCH_REQUEST},
  {"injector": injectors.SimpleInjector(), "endpoint": MATCH_REQUEST},
]