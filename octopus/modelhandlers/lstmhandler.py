"""
Handler for LSTM models.
"""
__author__ = 'ryanquinnnelson'

import logging

from octopus.models import LSTM


def _convert_dict_to_dicts(d):
    """
    Convert given dictionary to a list of dictionaries in which each dictionary in the list contains only the arguments
    related to a single CNN layer.

    Args:
        d (Dict): dictionary in which each key is composed of an integer representing a layer number and a parameter

    Returns: List of dictionaries

    """
    # determine number of dictionaries to create
    layer_number_set = set()
    for key in d:
        layer_number, layer_parm = key.strip().split('.')
        layer_number_set.add(int(layer_number))
    num_layers = len(layer_number_set)

    # create a dictionary of parmeters for each layer, in layer order (1,2,3...)
    layer_dicts = []
    for i in range(1, num_layers + 1):  # extract values in order

        layer_dict = {}

        # find all dictionary entries that start with this layer name
        # extract parameter names and values and place into a dictionary for this layer
        for key in d:
            layer_number, layer_parm = key.strip().split('.')
            if int(layer_number) == i:
                layer_dict[layer_parm] = d[key]
        layer_dicts.append(layer_dict)

    return layer_dicts


class LstmHandler:
    """
    Defines object to handle LSTM model initialization.

    """

    def __init__(self, model_type, lstm_input_size, hidden_size, num_layers,
                 output_size, bidirectional, dropout, conv_dict, lin1_output_size, lin1_dropout):
        """
        Initialize LstmHandler.

        :param model_type (str): Type of LSTM model. Allows BasicLSTM and CnnLSTM.
        :param lstm_input_size (int): Dimension of features being input into the LSTM portion of the model.
        :param hidden_size (int): Dimension of each hidden layer in the LSTM model.
        :param num_layers (int): Number of LSTM layers in LSTM portion of the model.
        :param output_size (int): The number of labels in the feature dimension of linear layer output.
        :param bidirectional (Boolean): True if LSTM is bidirectional. False otherwise.
        :param dropout (float): The percent of node dropout in the LSTM model.
        :param conv_dict (Dict): A dictionary containing the parameters for each cnn layer.
        :param lin1_output_size (int): The number of labels in the feature dimension of the first linear layer if there are multiple linear layers.
        :param lin1_dropout (float): The percent of node dropout in between linear layers in the model if there are multiple linear layers.
        """
        logging.info('Initializing LSTM handler...')

        self.model_type = model_type
        self.lstm_input_size = lstm_input_size
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.output_size = output_size
        self.bidirectional = bidirectional
        self.dropout = dropout
        self.conv_dicts = _convert_dict_to_dicts(conv_dict)
        self.lin1_output_size = lin1_output_size
        self.lin1_dropout = lin1_dropout

    def get_model(self):
        """
        Initialize the LSTM model based on model_type.

        :return (nn.Module): LSTM model
        """
        model = None

        if self.model_type == 'BasicLSTM':
            model = LSTM.BasicLSTM(self.lstm_input_size, self.hidden_size, self.num_layers,
                                   self.output_size, self.bidirectional, self.dropout)
        elif self.model_type == 'CnnLSTM':

            model = LSTM.CnnLSTM(self.lstm_input_size, self.hidden_size, self.num_layers, self.output_size,
                                 self.bidirectional, self.dropout, self.conv_dicts, self.lin1_output_size,
                                 self.lin1_dropout)
        logging.info(f'Model initialized:\n{model}')
        return model
