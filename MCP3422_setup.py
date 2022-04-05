#!/usr/bin/env python
# Modified code from Steve Marple, reused under the
# MIT Licence

import glob
import logging
import smbus
from MCP342x import MCP342x



# Create a list of all the objects. They will be sampled in this
# order, unless any later objects can be sampled can be moved earlier
# for simultaneous sampling.
adcs = [addr68_ch0, addr68_ch1]
r = MCP342x.convert_and_read_many(adcs, samples=3)
print('return values: ')
print(r)