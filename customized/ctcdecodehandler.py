"""
Everything related to CTCDecode.
"""
__author__ = 'ryanquinnnelson'

import logging
import multiprocessing
import customized.phoneme_details as pl


def get_ctcdecoder(labels, model_path, alpha, beta, cutoff_top_n, cutoff_prob, beam_width, num_processes, blank_id,
                   log_probs_input):
    import ctcdecode

    # vals = [labels, model_path, alpha, beta, cutoff_top_n, cutoff_prob, beam_width, num_processes, blank_id,
    #                log_probs_input]
    # logging.info(f'decoder values:{vals}')
    d = ctcdecode.CTCBeamDecoder(labels=labels, model_path=model_path, alpha=alpha, beta=beta,
                                 cutoff_top_n=cutoff_top_n, cutoff_prob=cutoff_prob, beam_width=beam_width,
                                 num_processes=num_processes,
                                 blank_id=blank_id, log_probs_input=log_probs_input)
    return d


class CTCDecodeHandler:

    def __init__(self, model_path, alpha, beta, cutoff_top_n, cutoff_prob, beam_width, blank_id,
                 log_probs_input):
        logging.info('Initializing ctcdecode handler...')

        self.model_path = None if model_path == 'None' else model_path
        self.alpha = alpha
        self.beta = beta
        self.cutoff_top_n = cutoff_top_n
        self.cutoff_prob = cutoff_prob
        self.beam_width = beam_width  # beam_width=1 (greedy search); beam_width>1 (beam search)
        self.blank_id = blank_id
        self.log_probs_input = log_probs_input

        n_cpus = multiprocessing.cpu_count()
        logging.info(f'CPU count:{n_cpus}.')
        self.num_processes = n_cpus
        self.labels = pl.PHONEME_MAP

    def ctcdecoder(self):
        return get_ctcdecoder(self.labels, self.model_path, self.alpha, self.beta, self.cutoff_top_n,
                              self.cutoff_prob, self.beam_width, self.num_processes, self.blank_id,
                              self.log_probs_input)
