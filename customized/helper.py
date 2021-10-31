import logging

import numpy as np
import torch

from customized import phoneme_list as pl


def convert_to_phonemes(i, beam_results, out_lens, phoneme_list):
    # i is the ith item in the batch, indexed from 0
    j = 0  # top jth beam, where 0 is the highest
    beam = beam_results[i][j][:out_lens[i][j]]
    beam = beam.cpu().numpy()
    converted = np.array([phoneme_list[idx] for idx in beam.flatten()])

    logging.info('beam array', beam.shape)
    logging.info('beam tensor', beam.shape)
    logging.info('converted', converted.shape)
    return converted


def target_to_phonemes(target, phoneme_list):
    target = target.cpu().numpy()
    converted = np.array([phoneme_list[idx] for idx in target.flatten()])
    return converted


def convert_to_string(converted_list):
    return ''.join(converted_list.tolist())


def decode_output(out, ctcdecode):
    # decode requires BATCHSIZE x N_TIMESTEPS x N_LABELS
    out = torch.transpose(out, 0, 1)
    logging.info('out transposed', out.shape)

    # decode batch
    beam_results, beam_scores, timesteps, out_lens = ctcdecode.decode(out)
    logging.info('beam_results', beam_results.shape)  # BATCHSIZE x N_BEAMS X N_TIMESTEPS
    logging.info('beam_scores', beam_scores.shape)  # BATCHSIZE x N_BEAMS
    logging.info('timesteps', timesteps.shape)  # BATCHSIZE x N_BEAMS
    logging.info('out_lens', out_lens.shape)  # BATCHSIZE x N_BEAMS

    return beam_results, beam_scores, timesteps, out_lens


def calculate_distances(beam_results, out_lens, targets):
    import Levenshtein
    n_batches = beam_results.shape[0]
    logging.info(f'Calculating distance for {n_batches} entries...')
    distances = []

    for i in range(n_batches):
        out_converted = convert_to_phonemes(i, beam_results, out_lens, pl.PHONEME_LIST)
        target_converted = target_to_phonemes(targets[i], pl.PHONEME_LIST)

        out_str = convert_to_string(out_converted)
        target_str = convert_to_string(target_converted)

        distance = Levenshtein.distance(out_str, target_str)
        distances.append(distance)

        logging.info(f'targets[{i}]', targets[i])
        logging.info('out_converted', out_converted)
        logging.info('target_converted', target_converted)
        logging.info('out_str', out_str)
        logging.info('target_str', target_str)
        logging.info('distance', distance)

    return np.array(distances).sum()
