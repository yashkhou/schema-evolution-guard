import json,sys
from .core import compare
f=compare(json.load(open(sys.argv[1])),json.load(open(sys.argv[2]))); print(json.dumps([x.as_dict() for x in f],indent=2)); raise SystemExit(2 if any(x.breaking for x in f) else 0)
