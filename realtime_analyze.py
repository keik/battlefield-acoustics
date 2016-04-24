#!/usr/bin/env python

import argparse
import logging

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
logger.addHandler(handler)


def main(filepath,
         rate,
         bufsize,
         win,
         shift):

    import time
    import threading
    import numpy as np
    import matplotlib
    matplotlib.use('TkAgg')

    from matplotlib.image import NonUniformImage
    import matplotlib.pyplot as plt
    import pyaudio

    if filepath:
        import wave
        wf = wave.open(filepath, 'rb')

    else:
        raise 'Not Implement'

    D = None

    def analyze():
        def callback(in_data, frame_count, time_info, status):
            nonlocal D

            data = wf.readframes(frame_count)
            # normalize
            idata = np.fromstring(data, np.int16) / 2 ** (16 - 1)
            # mono
            idata = idata.reshape(-1, 2).T[0]
            D = np.abs(np.fft.fft(idata))

            return (data, pyaudio.paContinue)

        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True,
                        frames_per_buffer=1024,
                        stream_callback=callback)

        logger.debug('open stream')
        stream.start_stream()

        while stream.is_active():
            time.sleep(0.1)

        stream.stop_stream()
        stream.close()
        wf.close()

        p.terminate()

    th = threading.Thread(target=analyze)
    th.start()

    fig = plt.figure()
    axes = fig.add_subplot(1, 1, 1)
    axes.set_aspect('auto')
    axes.set_xlim(0, 1024 / 2)
    axes.set_xticks(np.linspace(0, 1024 / 2, 5))
    axes.set_xticklabels(np.linspace(0, 44100 / 2, 5))
    axes.set_yticks(np.linspace(0, 300, 5))
    axes.set_ylim(0, 300)
    line = axes.plot(1, 1)[0]
    fig.show()

    background = fig.canvas.copy_from_bbox(axes.bbox)

    while True:
        time.sleep(0.01)
        logger.debug('len: {}, max: {}, min: {}'.format(len(D), D.max(), D.min()))
        line.set_data(np.arange(len(D)), D)
        fig.canvas.restore_region(background)
        axes.draw_artist(line)
        fig.canvas.blit(axes.bbox)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Process real-time HPSS and plotting.')
    parser.add_argument('filepath', nargs='?',
                        help="""
                        File path to analyze. If not specified, analyze mic input
                        """)
    parser.add_argument('-r', '--rate', dest='rate', default=44100,
                        help="""
                        Frame rate to read audio. Default value is 44100
                        """)
    parser.add_argument('-b', '--bufsize', dest='bufsize', default=1024,
                        help="""
                        Frames count to process fft per buffer. Default value is 1024
                        """)
    parser.add_argument('-w', '--win', dest='win', default='hamming',
                        help="""
                        Window function. Select from `hamming`, `hanning`, or `none`.
                        Default value is `hamming
                        """)
    parser.add_argument('-s', '--shift', dest='shift', default=256,
                        help="""
                        Shift size for window function. Default value is 256
                        """)
    parser.add_argument('-v', '--verbose', action='store_true', default=False,
                        help="""
                        Run as verbose mode
                        """)

    args = parser.parse_args()

    if args.verbose:
        logger.setLevel(logging.DEBUG)
        handler.setLevel(logging.DEBUG)

    main(args.filepath,
         int(args.rate),
         int(args.bufsize),
         args.win,
         int(args.shift))
