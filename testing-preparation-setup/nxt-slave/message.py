# https://ni.srht.site/nxt-python/latest/

import nxt.locator

b = nxt.locator.find()
b.message_write(1, "test".encode("utf-8"))


b.message_write(1, "B".encode("utf-8"))
b.message_write(1, (90).to_bytes(4, "little", signed=True))

b.message_write(1, "A".encode("utf-8"))
b.message_write(1, (90).to_bytes(4, "little", signed=True))

# https://lab.open-roberta.org/#
