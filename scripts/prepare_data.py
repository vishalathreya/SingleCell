import numpy as np
from sklearn.model_selection import StratifiedShuffleSplit, StratifiedKFold
import pdb
import sys
import argparse
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument('--use_labelled_only', default=False, action='store_true')
parser.add_argument('--num_samples', type=int, required=False)
args = parser.parse_args()

data_path = "C:/Users/bvish/Documents/UNC/COMP 991 - Junier Oliva/gmm/data/"
with open(data_path + 'Levine_32_matrix.csv') as f:
    data = f.readlines()

data = data[1:]
numpy_array = np.zeros((len(data), 33))
for i in tqdm(range(len(data))):
    split_data = data[i].strip('\n').split(',')
    if split_data[-1] == 'NaN':
        split_data[-1] = '0'
    array_data = np.array(split_data).astype('float')
    numpy_array[i] = array_data


# Taking only random `num_samples` labelled data if specified else entire data
if(args.use_labelled_only):
    numpy_array = numpy_array[np.where(numpy_array[:, -1] > 0)[0]]

num_samples = args.num_samples if args.num_samples else numpy_array.shape[0]
print(num_samples)
inds = np.random.permutation(numpy_array.shape[0])
numpy_array = numpy_array[inds][:num_samples, :]
label = numpy_array[:, -1]

# Normalize
data_mean = np.mean(numpy_array, 0)
data_std = np.std(numpy_array, 0)
norm_array = (numpy_array - data_mean[None, :]) / data_std[None, :]       # None indexing adds a new dimension/axis

ss = StratifiedKFold(n_splits=5, shuffle=True)
splits = list(ss.split(norm_array, label))


for i, (train_inds, test_inds) in enumerate(splits):
    train_data = norm_array[train_inds]
    test_data = norm_array[test_inds]
    train_data[:, -1] = label[train_inds]
    test_data[:, -1] = label[test_inds]

    np.save(data_path + 'Levine_32_matrix_train_split{}.npy'.format(i), train_data)
    np.save(data_path + 'Levine_32_matrix_test_split{}.npy'.format(i), test_data)