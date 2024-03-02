"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Decode Alamouti',   # will show up in GRC
            in_sig=[np.complex64, np.complex64, np.complex64],
            out_sig=[np.complex64]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).

    def work(self, input_items, output_items):
        """example: multiply with constant"""

        h0 = input_items[1][0]
        h1 = input_items[2][0]
        output_items[0][0] = np.conj(h0)*input_items[0][0]+h1*np.conj(input_items[0][1])
        output_items[0][1] = np.conj(h1)*input_items[0][0]-h0*np.conj(input_items[0][1])

        return 2
