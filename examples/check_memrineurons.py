"""
Check Memrineurons
"""

from simulator.src import BoardSimulator # connect to the board
from MemriNeurons.cores import HardCore # core handler

# connect the board
CONN = BoardSimulator()
_ = CONN.connect('simulator')

# creating a core handler
device = HardCore(CONN)

# checking the functionality
_ = device.write_weight(0, 0, 0.1)
print(device.read_one_weight(0, 0))
