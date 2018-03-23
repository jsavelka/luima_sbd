# Tokenization
TOKENIZATION_STRING = r'[A-z]+|\d+|[ \t\f]+|[\n\r\v]+|[^A-z\d\s]'

# File paths
DATA_DIR = 'data'
SEN_MODEL = 'sbd_SEN.crfsuite'
NSEN_MODEL = 'sbd_NSEN.crfsuite'
INTEGRATING_MODEL = 'sbd_INT.crfsuite'
SIMPLE_MODEL = '20180322.crfsuite'

# CRF params
CRF_WINDOW = 3

# Useful constants
PRINT_SEP = "-----sep-----"

# Flask server params
DEFAULT_PORT = 5000
