from base64 import encode
import os
import json

BENIGN_FILE_DIR = 'benign-dataset/'
MALICIOUS_FILE_DIR = 'malicious-dataset/'
BENIGN_APKS_UNIQUE_API_CALLS = 'ben_unique_api_calls/'
MALICOUS_APKS_UNIQUE_API_CALLS = 'mal_unique_api_calls/'

def get_all_api_calls(PATH):
  """
  This function get all the distinct api calls for all the apks
  and make a list of them. After that, it will take only the unique
  api calls for all the apks and return as a list.
  """

  all_api_calls = []
  files = os.listdir(PATH)
  for file in files:
    fileObj = open(PATH + file, 'r')
    api_calls = fileObj.read()
    fileObj.close()

    api_calls = api_calls.splitlines()
    all_api_calls += api_calls

  all_api_calls = set(all_api_calls)
  return all_api_calls


def import_benign_files(benign_unique_api_calls):
  """
  This function takes all the unique api calls specially for benign apks
  and concatenate them to all the unique feature vector for benign apks.
  In addition to this, this function also maintains the data of all the unique
  features for respective apks in dictionary format.
  """

  benign_feature_vector_dict = {}
  benign_unique_feature_vector = []

  files = os.listdir(BENIGN_FILE_DIR)
  print(files)

  for file in files:
    ext = file.split('.')[-1]

    if(ext == 'json'):
      fileObj = open(BENIGN_FILE_DIR + file, 'r')
      apk_feature_dict = json.load(fileObj)
      fileObj.close()

      # append both the dictionaries into one
      benign_feature_vector_dict = { **benign_feature_vector_dict, **apk_feature_dict }
    elif ext == 'txt':
      fileObj = open(BENIGN_FILE_DIR + file, 'rb')
      apk_feature_vector = fileObj.read()
      fileObj.close()

      # concat the feature vector
      benign_unique_feature_vector += list(apk_feature_vector.splitlines())
  
  # add the benign unique api calls to the benign unique feature vector
  benign_unique_feature_vector += benign_unique_api_calls
  
  # get all unique benign feature vector
  benign_unique_feature_vector = set(benign_unique_feature_vector)

  return benign_unique_feature_vector, benign_feature_vector_dict


def import_malicious_files(malicious_unique_api_calls):
  """
  This function takes all the unique api calls specially for malicious apks
  and concatenate them to all the unique feature vector for malicious apks.
  In addition to this, this function also maintains the data of all the unique
  features for respective apks in dictionary format.
  """

  malicious_feature_vector_dict = {}
  malicious_unique_feature_vector = []

  files = os.listdir(MALICIOUS_FILE_DIR)
  print(files)

  for file in files:
    ext = file.split('.')[-1]

    if(ext == 'json'):
      fileObj = open(MALICIOUS_FILE_DIR + file, 'r')
      apk_feature_dict = json.load(fileObj)
      fileObj.close()

      # append both the dictionaries into one
      malicious_feature_vector_dict = { **malicious_feature_vector_dict, **apk_feature_dict }
    elif ext == 'txt':
      fileObj = open(MALICIOUS_FILE_DIR + file, 'rb')
      apk_feature_vector = fileObj.read()
      fileObj.close()

      # concat the feature vector
      malicious_unique_feature_vector += list(apk_feature_vector.splitlines())
  
  # add the malicious unique api calls to the malicious unique feature vector
  malicious_unique_feature_vector += malicious_unique_api_calls

  # get all unique malicious feature vector
  malicious_unique_feature_vector = set(malicious_unique_feature_vector)

  return malicious_unique_feature_vector, malicious_feature_vector_dict

def create_binary_matrix(all_apk_features, all_apk_features_dict):
  """
  This function specially focuses on creating the binary matrix for all the apks
  and their feature vectors.
  """
  
  binary_matrix = []    # dim = (total_apks x len(all_apk_features))

  # store all apk names (i.e. keys in all_apk_features_dict) in list
  apk_names = list(all_apk_features_dict.keys())    # rows
  # print(apk_names)
  apk_full_features = list(all_apk_features_dict.values()) 

  for name in apk_names:
    apks_info = [0] * len(all_apk_features)   # cols
    
    i = 0
    for feat in all_apk_features:
      # print(feat)
      # feat = feat.decode('ascii')
      feat = str(feat)
      feat = feat[2:-1]
      # print(feat)
      if feat in all_apk_features_dict[name]:
        # print('marking')
        apks_info[i] = 1
      
      i += 1
    
    binary_matrix.append(apks_info)
  
  print('d1: ', len(binary_matrix))
  print('d2: ', len(binary_matrix[0]))
  
  return binary_matrix

def writeIntoFile(data, file_name):
  file_obj = open(file_name, 'w')
  for feat in data:
    file_obj.write(str(feat))
    file_obj.write('\n')
  file_obj.close()

def writeObjIntoTxtFile(data, file_name):
  file_obj = open(file_name, 'w')
  for key in list(data.keys()):
    curr_line = str(key) + "   ::   " + str(data[key]);

    file_obj.write(curr_line)
    file_obj.write('\n')

  file_obj.close()

def writeObjIntoJSONFile(data, file_name):
  file_obj = open(file_name, 'w')
  json.dump(data, file_obj)
  file_obj.close()


benign_unique_api_calls = get_all_api_calls(BENIGN_APKS_UNIQUE_API_CALLS)
# print('ben_api: ', len(benign_unique_api_calls))
benign_unique_feature_vector, benign_feature_vector_dict = import_benign_files(benign_unique_api_calls)

malicious_unique_api_calls = get_all_api_calls(MALICOUS_APKS_UNIQUE_API_CALLS)
malicious_unique_feature_vector, malicious_feature_vector_dict = import_malicious_files(malicious_unique_api_calls)

# combined_unique_feature_vector = benign_unique_feature_vector.union(malicious_unique_feature_vector)
# features_in_benign_not_in_malicious = benign_unique_feature_vector.difference(malicious_unique_feature_vector)
# features_in_malicious_not_in_benign = malicious_unique_feature_vector.difference(benign_unique_feature_vector)
# features_common_in_benign_and_malicious = benign_unique_feature_vector.intersection(malicious_unique_feature_vector)

# benign_binary_matrix = create_binary_matrix(combined_unique_feature_vector, benign_feature_vector_dict)
# malicious_binary_matrix = create_binary_matrix(combined_unique_feature_vector, malicious_feature_vector_dict)

# writeIntoFile(combined_unique_feature_vector, 'unique_feature_vector.txt')
# writeIntoFile(benign_binary_matrix, 'benign_binary_matrix.txt')
# writeIntoFile(malicious_binary_matrix, 'malicious_binary_matrix.txt')
# writeIntoFile(features_in_benign_not_in_malicious, 'features_in_benign_not_in_malicious.txt')
# writeIntoFile(features_in_malicious_not_in_benign, 'features_in_malicious_not_in_benign.txt')
# writeIntoFile(features_common_in_benign_and_malicious, 'features_common_in_benign_and_malicious.txt')
