#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Alamouti Scheme
# Author: Oehme, Reuter
# GNU Radio version: 3.10.7.0

from packaging.version import Version as StrictVersion
from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio import analog
from gnuradio import blocks
from gnuradio import digital
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio.qtgui import Range, RangeWidget
from PyQt5 import QtCore
import Alamouti_epy_block_0 as epy_block_0  # embedded python block
import Alamouti_epy_block_2 as epy_block_2  # embedded python block
import math
import numpy as np
import random



class Alamouti(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Alamouti Scheme", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Alamouti Scheme")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "Alamouti")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.payload_size = payload_size = 100
        self.theta_1 = theta_1 = 0
        self.theta_0 = theta_0 = 0
        self.qpsk_0 = qpsk_0 = digital.constellation_rect([0.707+0.707j, -0.707+0.707j, -0.707-0.707j, 0.707-0.707j], [0, 1, 2, 3],
        4, 2, 2, 1, 1).base()
        self.noise_level = noise_level = 0
        self.data = data = [random.randint(0,255) for i in range(payload_size)]
        self.alpha_1 = alpha_1 = 1
        self.alpha_0 = alpha_0 = 1
        self.S2_pen = S2_pen = ((0.5, 0.5), (0.5, -0.5))
        self.Pilot_1 = Pilot_1 = [1,-1]
        self.Pilot_0 = Pilot_0 = [1,1]

        ##################################################
        # Blocks
        ##################################################

        self._theta_1_range = Range(0, 2*math.pi, 0.001, 0, 200)
        self._theta_1_win = RangeWidget(self._theta_1_range, self.set_theta_1, "'theta_1'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._theta_1_win)
        self._theta_0_range = Range(0, 2*math.pi, 0.001, 0, 200)
        self._theta_0_win = RangeWidget(self._theta_0_range, self.set_theta_0, "'theta_0'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._theta_0_win)
        self._noise_level_range = Range(0, 1, 0.001, 0, 200)
        self._noise_level_win = RangeWidget(self._noise_level_range, self.set_noise_level, "'noise_level'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._noise_level_win)
        self._alpha_1_range = Range(0, 1, 0.001, 1, 200)
        self._alpha_1_win = RangeWidget(self._alpha_1_range, self.set_alpha_1, "'alpha_1'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._alpha_1_win)
        self._alpha_0_range = Range(0, 1, 0.001, 1, 200)
        self._alpha_0_win = RangeWidget(self._alpha_0_range, self.set_alpha_0, "'alpha_0'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._alpha_0_win)
        self.epy_block_2 = epy_block_2.blk()
        self.epy_block_0 = epy_block_0.blk()
        self.digital_constellation_encoder_bc_0 = digital.constellation_encoder_bc(qpsk_0)
        self.digital_constellation_decoder_cb_0 = digital.constellation_decoder_cb(qpsk_0)
        self.blocks_vector_source_x_2_0 = blocks.vector_source_c(Pilot_1, True, 1, [])
        self.blocks_vector_source_x_2 = blocks.vector_source_c(Pilot_0, True, 1, [])
        self.blocks_vector_source_x_1_0 = blocks.vector_source_c([alpha_1*np.exp(1j*theta_1)], True, 1, [])
        self.blocks_vector_source_x_1 = blocks.vector_source_c([alpha_0*np.exp(1j*theta_0)], True, 1, [])
        self.blocks_vector_source_x_0 = blocks.vector_source_b(data, True, 1, [])
        self.blocks_vector_sink_x_0 = blocks.vector_sink_b(1, 1024)
        self.blocks_throttle2_2 = blocks.throttle( gr.sizeof_char*1, 100000, True, 0 if "auto" == "auto" else max( int(float(0.1) * 100000) if "auto" == "time" else int(0.1), 1) )
        self.blocks_stream_mux_0_0 = blocks.stream_mux(gr.sizeof_gr_complex*1, (2, 8))
        self.blocks_stream_mux_0 = blocks.stream_mux(gr.sizeof_gr_complex*1, (2, 8))
        self.blocks_stream_demux_0_0 = blocks.stream_demux(gr.sizeof_gr_complex*1, (1, 1))
        self.blocks_stream_demux_0 = blocks.stream_demux(gr.sizeof_gr_complex*1, (2, 8))
        self.blocks_repeat_0_0 = blocks.repeat(gr.sizeof_gr_complex*1, 8)
        self.blocks_repeat_0 = blocks.repeat(gr.sizeof_gr_complex*1, 8)
        self.blocks_repack_bits_bb_1 = blocks.repack_bits_bb(2, 8, "", False, gr.GR_MSB_FIRST)
        self.blocks_repack_bits_bb_0 = blocks.repack_bits_bb(8, 2, "", False, gr.GR_MSB_FIRST)
        self.blocks_multiply_xx_0_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_matrix_xx_0 = blocks.multiply_matrix_cc(S2_pen, gr.TPP_DONT)
        self.blocks_add_xx_0 = blocks.add_vcc(1)
        self.analog_noise_source_x_0 = analog.noise_source_c(analog.GR_GAUSSIAN, noise_level, 0)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_noise_source_x_0, 0), (self.blocks_add_xx_0, 2))
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_stream_demux_0, 0))
        self.connect((self.blocks_multiply_matrix_xx_0, 0), (self.blocks_repeat_0, 0))
        self.connect((self.blocks_multiply_matrix_xx_0, 1), (self.blocks_repeat_0_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.blocks_multiply_xx_0_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.blocks_repack_bits_bb_0, 0), (self.blocks_throttle2_2, 0))
        self.connect((self.blocks_repack_bits_bb_1, 0), (self.blocks_vector_sink_x_0, 0))
        self.connect((self.blocks_repeat_0, 0), (self.epy_block_2, 1))
        self.connect((self.blocks_repeat_0_0, 0), (self.epy_block_2, 2))
        self.connect((self.blocks_stream_demux_0, 0), (self.blocks_stream_demux_0_0, 0))
        self.connect((self.blocks_stream_demux_0, 1), (self.epy_block_2, 0))
        self.connect((self.blocks_stream_demux_0_0, 0), (self.blocks_multiply_matrix_xx_0, 0))
        self.connect((self.blocks_stream_demux_0_0, 1), (self.blocks_multiply_matrix_xx_0, 1))
        self.connect((self.blocks_stream_mux_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.blocks_stream_mux_0_0, 0), (self.blocks_multiply_xx_0_0, 0))
        self.connect((self.blocks_throttle2_2, 0), (self.digital_constellation_encoder_bc_0, 0))
        self.connect((self.blocks_vector_source_x_0, 0), (self.blocks_repack_bits_bb_0, 0))
        self.connect((self.blocks_vector_source_x_1, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.blocks_vector_source_x_1_0, 0), (self.blocks_multiply_xx_0_0, 1))
        self.connect((self.blocks_vector_source_x_2, 0), (self.blocks_stream_mux_0, 0))
        self.connect((self.blocks_vector_source_x_2_0, 0), (self.blocks_stream_mux_0_0, 0))
        self.connect((self.digital_constellation_decoder_cb_0, 0), (self.blocks_repack_bits_bb_1, 0))
        self.connect((self.digital_constellation_encoder_bc_0, 0), (self.epy_block_0, 0))
        self.connect((self.epy_block_0, 0), (self.blocks_stream_mux_0, 1))
        self.connect((self.epy_block_0, 1), (self.blocks_stream_mux_0_0, 1))
        self.connect((self.epy_block_2, 0), (self.digital_constellation_decoder_cb_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "Alamouti")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_payload_size(self):
        return self.payload_size

    def set_payload_size(self, payload_size):
        self.payload_size = payload_size
        self.set_data([random.randint(0,255) for i in range(self.payload_size)])

    def get_theta_1(self):
        return self.theta_1

    def set_theta_1(self, theta_1):
        self.theta_1 = theta_1
        self.blocks_vector_source_x_1_0.set_data([self.alpha_1*np.exp(1j*self.theta_1)], [])

    def get_theta_0(self):
        return self.theta_0

    def set_theta_0(self, theta_0):
        self.theta_0 = theta_0
        self.blocks_vector_source_x_1.set_data([self.alpha_0*np.exp(1j*self.theta_0)], [])

    def get_qpsk_0(self):
        return self.qpsk_0

    def set_qpsk_0(self, qpsk_0):
        self.qpsk_0 = qpsk_0
        self.digital_constellation_decoder_cb_0.set_constellation(self.qpsk_0)
        self.digital_constellation_encoder_bc_0.set_constellation(self.qpsk_0)

    def get_noise_level(self):
        return self.noise_level

    def set_noise_level(self, noise_level):
        self.noise_level = noise_level
        self.analog_noise_source_x_0.set_amplitude(self.noise_level)

    def get_data(self):
        return self.data

    def set_data(self, data):
        self.data = data
        self.blocks_vector_source_x_0.set_data(self.data, [])

    def get_alpha_1(self):
        return self.alpha_1

    def set_alpha_1(self, alpha_1):
        self.alpha_1 = alpha_1
        self.blocks_vector_source_x_1_0.set_data([self.alpha_1*np.exp(1j*self.theta_1)], [])

    def get_alpha_0(self):
        return self.alpha_0

    def set_alpha_0(self, alpha_0):
        self.alpha_0 = alpha_0
        self.blocks_vector_source_x_1.set_data([self.alpha_0*np.exp(1j*self.theta_0)], [])

    def get_S2_pen(self):
        return self.S2_pen

    def set_S2_pen(self, S2_pen):
        self.S2_pen = S2_pen
        self.blocks_multiply_matrix_xx_0.set_A(self.S2_pen)

    def get_Pilot_1(self):
        return self.Pilot_1

    def set_Pilot_1(self, Pilot_1):
        self.Pilot_1 = Pilot_1
        self.blocks_vector_source_x_2_0.set_data(self.Pilot_1, [])

    def get_Pilot_0(self):
        return self.Pilot_0

    def set_Pilot_0(self, Pilot_0):
        self.Pilot_0 = Pilot_0
        self.blocks_vector_source_x_2.set_data(self.Pilot_0, [])




def main(top_block_cls=Alamouti, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
