import sys

print("hello world", flush=True)
print("have a nice day", flush=True)
print("support your friendly neighborhood anti-fascist", file=sys.stderr, flush=True)
print("say hello to your librarian", flush=True)
print("trans rights are human rights", file=sys.stderr, flush=True)

sys.exit(42)
