#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# GNU Radio version: 3.10.7.0

from packaging.version import Version as StrictVersion
from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio import blocks
from gnuradio import fft
from gnuradio.fft import window
from gnuradio import gr
from gnuradio.filter import firdes
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import iio
import math
import numpy as np
import sip



class loopback_chirp(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Not titled yet")
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

        self.settings = Qt.QSettings("GNU Radio", "loopback_chirp")

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
        self.tiempo_integral = tiempo_integral = 0.1
        self.samp_rate = samp_rate = 2**20
        self.lenght_vector_process = lenght_vector_process = 256
        self.freq = freq = 2400000000
        self.ID_SDR = ID_SDR = "ip:169.254.34.234"

        ##################################################
        # Blocks
        ##################################################

        self.qtgui_vector_sink_f_0_0 = qtgui.vector_sink_f(
            lenght_vector_process,
            0,
            1.0,
            "x-Axis",
            "y-Axis",
            "CORRELACION",
            1, # Number of inputs
            None # parent
        )
        self.qtgui_vector_sink_f_0_0.set_update_time(0.10)
        self.qtgui_vector_sink_f_0_0.set_y_axis((-140), 10)
        self.qtgui_vector_sink_f_0_0.enable_autoscale(True)
        self.qtgui_vector_sink_f_0_0.enable_grid(True)
        self.qtgui_vector_sink_f_0_0.set_x_axis_units("")
        self.qtgui_vector_sink_f_0_0.set_y_axis_units("")
        self.qtgui_vector_sink_f_0_0.set_ref_level(0)


        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_vector_sink_f_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_vector_sink_f_0_0.set_line_label(i, labels[i])
            self.qtgui_vector_sink_f_0_0.set_line_width(i, widths[i])
            self.qtgui_vector_sink_f_0_0.set_line_color(i, colors[i])
            self.qtgui_vector_sink_f_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_vector_sink_f_0_0_win = sip.wrapinstance(self.qtgui_vector_sink_f_0_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_vector_sink_f_0_0_win)
        self.qtgui_sink_x_0_2 = qtgui.sink_c(
            256, #fftsize
            window.WIN_BLACKMAN_hARRIS, #wintype
            freq, #fc
            samp_rate, #bw
            "TX", #name
            True, #plotfreq
            True, #plotwaterfall
            True, #plottime
            True, #plotconst
            None # parent
        )
        self.qtgui_sink_x_0_2.set_update_time(1.0/10)
        self._qtgui_sink_x_0_2_win = sip.wrapinstance(self.qtgui_sink_x_0_2.qwidget(), Qt.QWidget)

        self.qtgui_sink_x_0_2.enable_rf_freq(False)

        self.top_layout.addWidget(self._qtgui_sink_x_0_2_win)
        self.qtgui_sink_x_0 = qtgui.sink_c(
            256, #fftsize
            window.WIN_BLACKMAN_hARRIS, #wintype
            freq, #fc
            samp_rate, #bw
            "RX", #name
            True, #plotfreq
            True, #plotwaterfall
            True, #plottime
            True, #plotconst
            None # parent
        )
        self.qtgui_sink_x_0.set_update_time(1.0/10)
        self._qtgui_sink_x_0_win = sip.wrapinstance(self.qtgui_sink_x_0.qwidget(), Qt.QWidget)

        self.qtgui_sink_x_0.enable_rf_freq(False)

        self.top_layout.addWidget(self._qtgui_sink_x_0_win)
        self.iio_fmcomms2_source_0 = iio.fmcomms2_source_fc32(ID_SDR, [True, True, False, False], 32768)
        self.iio_fmcomms2_source_0.set_len_tag_key('packet_len')
        self.iio_fmcomms2_source_0.set_frequency(freq)
        self.iio_fmcomms2_source_0.set_samplerate(samp_rate)
        if True:
            self.iio_fmcomms2_source_0.set_gain_mode(0, 'slow_attack')
            self.iio_fmcomms2_source_0.set_gain(0, 64)
        if False:
            self.iio_fmcomms2_source_0.set_gain_mode(1, 'slow_attack')
            self.iio_fmcomms2_source_0.set_gain(1, 64)
        self.iio_fmcomms2_source_0.set_quadrature(True)
        self.iio_fmcomms2_source_0.set_rfdc(True)
        self.iio_fmcomms2_source_0.set_bbdc(True)
        self.iio_fmcomms2_source_0.set_filter_params('Auto', '', 0, 0)
        self.iio_fmcomms2_sink_0 = iio.fmcomms2_sink_fc32(ID_SDR, [True, True, False, False], 32768, False)
        self.iio_fmcomms2_sink_0.set_len_tag_key('')
        self.iio_fmcomms2_sink_0.set_bandwidth(20000000)
        self.iio_fmcomms2_sink_0.set_frequency(freq)
        self.iio_fmcomms2_sink_0.set_samplerate(samp_rate)
        if True:
            self.iio_fmcomms2_sink_0.set_attenuation(0, 10.0)
        if False:
            self.iio_fmcomms2_sink_0.set_attenuation(1, 10.0)
        self.iio_fmcomms2_sink_0.set_filter_params('Auto', '', 0, 0)
        self.fft_vxx_0_1_0 = fft.fft_vcc(lenght_vector_process, False, window.blackmanharris(lenght_vector_process), True, 1)
        self.fft_vxx_0_0 = fft.fft_vcc(lenght_vector_process, True, window.blackmanharris(lenght_vector_process), False, 1)
        self.fft_vxx_0 = fft.fft_vcc(lenght_vector_process, True, window.blackmanharris(lenght_vector_process), False, 1)
        self.blocks_vector_source_x_0_0 = blocks.vector_source_c([1.0, 0.9999982468065842, 0.9999719490282958, 0.9998579946528786, 0.999551215926306, 0.9989044538903371, 0.9977287209751704, 0.9957935337510887, 0.9928275082145868, 0.9885193297732039, 0.9825192290313257, 0.9744411120453355, 0.9638655092122512, 0.9503435194858377, 0.9334019350711988, 0.91254973480858, 0.8872861305823831, 0.8571103385515829, 0.8215332239061813, 0.7800909322280405, 0.7323605703802927, 0.6779779332808464, 0.6166571883022492, 0.5482123251948804, 0.47258005583026225, 0.3898437051035512, 0.3002574736202584, 0.20427027742862977, 0.10254818496216722, -0.004005716462074285, -0.1142353734390923, -0.22672125014972055, -0.33977688440682685, -0.4514542378971589, -0.5595595743954677, -0.6616815230972753, -0.755232798323915, -0.8375067318464654, -0.9057493126031176, -0.9572468078424915, -0.9894282538320682, -0.9999811568946576, -0.986977652633938, -0.9490071636835057, -0.8853103223167849, -0.7959076508358318, -0.6817153063513274, -0.5446392025286281, -0.38763814012537257, -0.21474634253921182, -0.03104613719672535, 0.15741742360419347, 0.3437863400375491, 0.5206074208853054, 0.6801179338386816, 0.8145945417150223, 0.9167556700493559, 0.98020171713856, 0.9998716359447362, 0.9724888344783221, 0.8969645972922216, 0.7747239344727002, 0.609917554676996, 0.4094851493914271, 0.18303988795514106, -0.05744769317801341, -0.2981762733598817, -0.5242452941943242, -0.7205678051040615, -0.8729210963351541, -0.9690716062781763, -0.9998923727259534, -0.9603770962781805, -0.8504470504180232, -0.6754478421207798, -0.44624422833601074, -0.1788439292456884, 0.1064842964778607, 0.3865884053322071, 0.6372445557719054, 0.8352848253583369, 0.9608707426371385, 0.999698524516813, 0.944894552144514, 0.7983552662557868, 0.5713095423328588, 0.28393644085776887, -0.03604373563029642, -0.35577686997512387, -0.6405266848097284, -0.8574882325307233, -0.9797675191147917, -0.9900514664048495, -0.8834630181614823, -0.66913120009296, -0.3701123380009624, -0.021474080275468887, 0.33341501877114593, 0.6480855444033261, 0.8790936390966169, 0.9922965311707276, 0.9683720126427311, 0.8066705224054026, 0.526626193362473, 0.16623682700267145, -0.22247044314366385, -0.5805895573621919, -0.8512184262693191, -0.9887862131683213, -0.967298693764607, -0.7859738434603893, -0.47101356092940916, -0.0727996298363527, 0.3414473080484381, 0.698659251600187, 0.9328816930381907, 0.9979468341413251, 0.8773944048098223, 0.5894341925892373, 0.1854869781925058, -0.2580163620340067, -0.6535380180357299, -0.9196842095454986, -0.9984740918978074, -0.8689268193318261, -0.5536730409175785, -0.11649717216220831, 0.34945473733588783, 0.7409511253549588, 0.9676458261737826, 0.9736852329260876, 0.7526958538648207, 0.3519658903113137, -0.1361272887282213, -0.5943990397767963, -0.9087295565707191, -0.9970453595686403, -0.8320002142420373, -0.45088471951631187, 0.05091392945100424, 0.5424689209815693, 0.8910057080782882, 0.9982784269205661, 0.8296257648473939, 0.4268616166343908, -0.09997587968796975, -0.6012391163328701, -0.9297391141057649, -0.9846733479295472, -0.7442078747301109, -0.27583677347459956, 0.28036365459139595, 0.7523031908659962, 0.9890499754353389, 0.9103173230336258, 0.535784599682234, -0.01692091800324839, -0.5671367115955227, -0.9294332062851877, -0.9768329951605418, -0.6873153408917616, -0.1560621903766226, 0.43327744330786055, 0.8707374785085378, 0.995180026890941, 0.7555606558685097, 0.23449633686293897, -0.37727656715428126, -0.8490333785942069, -0.9972335173307668, -0.7588893017289575, -0.221225927626873, 0.4070373297886628, 0.8749017023474475, 0.9896202953185408, 0.6983397942166137, 0.11555681274875859, -0.5185800042230361, -0.9355945823808534, -0.9530514462091001, -0.5571237261447686, 0.0849644650660967, 0.6923907462693539, 0.9925033544808847, 0.8447509652101016, 0.3099440482501589, -0.3705270124066556, -0.8810285079294863, -0.9781482651716011, -0.6094877222706304, 0.05424990923628927, 0.6944911574288127, 0.9963126121827782, 0.8050579906896755, 0.20953768212473575, -0.494547427934387, -0.9488190354970143, -0.9152834557695331, -0.40461672207193816, 0.3210488699421346, 0.8791036353760099, 0.9678978263372717, 0.5329609617625546, -0.19502273633252923, -0.8182742873589206, -0.988246120234632, -0.603362907815517, 0.12531528005795037, 0.785031944266848, 0.9936449893023314, 0.6236517494742377, -0.11467885207580475, -0.7876676258167185, -0.9912946942128856, -0.5965364268708043, 0.16340290517120387, 0.8255643738751214, 0.9777773384814513, 0.5184442267754007, -0.2698789286569914, -0.88907030098354, -0.9392691526101254, -0.38107741827419217, 0.42803442057603647, 0.9578264130275317, 0.8528839662400491, 0.1760487425633118, -0.6219945405947046, -0.9988718274703408, -0.6907698739929059, 0.09678863465660156, 0.819294269995994, 0.9673176890418871, 0.4292849781860798, -0.4175732758290552, -0.9659245338830051, -0.8137856721702763, -0.06488192617482534, 0.7342265102641088, 0.989225252279012, 0.5028755768000951, -0.3651249372974048, -0.9574986468627734, -0.8164359639601504, -0.0432735033324852, 0.7658631708741204, 0.9756784925363803, 0.41381015206709276, -0.47966201604626624, -0.9902331696685692, -0.7006286538089671, 0.16115608501539685, 0.892900775710287, 0.887649278806749, 0.14235473842879975, -0.7244804883941369], True, 1, [])
        self.blocks_stream_to_vector_0_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, lenght_vector_process)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, lenght_vector_process)
        self.blocks_repeat_0 = blocks.repeat(gr.sizeof_gr_complex*lenght_vector_process, 9)
        self.blocks_multiply_conjugate_cc_0 = blocks.multiply_conjugate_cc(lenght_vector_process)
        self.blocks_integrate_xx_0 = blocks.integrate_cc((int(tiempo_integral*samp_rate/lenght_vector_process)), lenght_vector_process)
        self.blocks_complex_to_mag_0_0 = blocks.complex_to_mag(lenght_vector_process)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_complex_to_mag_0_0, 0), (self.qtgui_vector_sink_f_0_0, 0))
        self.connect((self.blocks_integrate_xx_0, 0), (self.fft_vxx_0_1_0, 0))
        self.connect((self.blocks_multiply_conjugate_cc_0, 0), (self.blocks_integrate_xx_0, 0))
        self.connect((self.blocks_repeat_0, 0), (self.blocks_complex_to_mag_0_0, 0))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.fft_vxx_0, 0))
        self.connect((self.blocks_stream_to_vector_0_0, 0), (self.fft_vxx_0_0, 0))
        self.connect((self.blocks_vector_source_x_0_0, 0), (self.blocks_stream_to_vector_0, 0))
        self.connect((self.blocks_vector_source_x_0_0, 0), (self.iio_fmcomms2_sink_0, 0))
        self.connect((self.blocks_vector_source_x_0_0, 0), (self.qtgui_sink_x_0_2, 0))
        self.connect((self.fft_vxx_0, 0), (self.blocks_multiply_conjugate_cc_0, 0))
        self.connect((self.fft_vxx_0_0, 0), (self.blocks_multiply_conjugate_cc_0, 1))
        self.connect((self.fft_vxx_0_1_0, 0), (self.blocks_repeat_0, 0))
        self.connect((self.iio_fmcomms2_source_0, 0), (self.blocks_stream_to_vector_0_0, 0))
        self.connect((self.iio_fmcomms2_source_0, 0), (self.qtgui_sink_x_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "loopback_chirp")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_tiempo_integral(self):
        return self.tiempo_integral

    def set_tiempo_integral(self, tiempo_integral):
        self.tiempo_integral = tiempo_integral

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.iio_fmcomms2_sink_0.set_samplerate(self.samp_rate)
        self.iio_fmcomms2_source_0.set_samplerate(self.samp_rate)
        self.qtgui_sink_x_0.set_frequency_range(self.freq, self.samp_rate)
        self.qtgui_sink_x_0_2.set_frequency_range(self.freq, self.samp_rate)

    def get_lenght_vector_process(self):
        return self.lenght_vector_process

    def set_lenght_vector_process(self, lenght_vector_process):
        self.lenght_vector_process = lenght_vector_process

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.iio_fmcomms2_sink_0.set_frequency(self.freq)
        self.iio_fmcomms2_source_0.set_frequency(self.freq)
        self.qtgui_sink_x_0.set_frequency_range(self.freq, self.samp_rate)
        self.qtgui_sink_x_0_2.set_frequency_range(self.freq, self.samp_rate)

    def get_ID_SDR(self):
        return self.ID_SDR

    def set_ID_SDR(self, ID_SDR):
        self.ID_SDR = ID_SDR




def main(top_block_cls=loopback_chirp, options=None):

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
