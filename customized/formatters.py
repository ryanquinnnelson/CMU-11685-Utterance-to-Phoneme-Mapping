"""
Contains all Formatter objects customized to the data.
"""
__author__ = 'ryanquinnnelson'

import pandas as pd
import logging
from customized.helper import out_to_phonemes, target_to_phonemes, convert_to_string, decode_output
import customized.phoneme_list as pl


class OutputFormatter:
    """
    Defines an object to manage formatting of test output.
    """

    def __init__(self):
        """
        Initialize OutputFormatter.
        Args:
            data_dir (str): fully-qualified path to data directory
        """
        logging.info('Initializing output formatter...')

    def format_output(self, out):
        """
        Format given model output as desired.

        Args:
            out (np.array): Model output

        Returns: DataFrame after formatting

        """

        # convert string array to dataframe
        df = pd.DataFrame(out).reset_index(drop=False)
        # logging.info('dataframe')
        # logging.info(f'\n{df.head()}')
        # logging.info(df.columns)

        # change column names
        df = df.rename(columns={0: 'label', 'index': 'id'})
        # logging.info(f'\n{df.head()}')

        return df
