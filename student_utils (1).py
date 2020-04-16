import pandas as pd
import numpy as np
import os
import tensorflow as tf
import string

####### STUDENTS FILL THIS OUT ######
#Question 3
def reduce_dimension_ndc(df, ndc_df):
    '''
    df: pandas dataframe, input dataset
    ndc_df: pandas dataframe, drug code dataset used for mapping in generic names
    return:
        df: pandas dataframe, output dataframe with joined generic drug name
    '''
    medList = []
    for i in string.ascii_lowercase:
        medList.append(i)
        
    med_dict = {}
    for medicine_id, name in enumerate(ndc_df.iloc[:,2].unique()):
        med_dict[name] = medList[medicine_id]
        
    ls = []
    for i in ndc_df.iloc[:,2]:
        ls.append(med_dict[i])
    ndc_df.insert(1, column="generic_drug_name", value = np.array(ls))
    
    df = df.merge(ndc_df.iloc[:, 0:2], left_on='ndc_code', right_on='NDC_Code').drop('NDC_Code', axis=1)
    
    return df

#Question 4
def select_first_encounter(df):
    '''
    df: pandas dataframe, dataframe with all encounters
    return:
        - first_encounter_df: pandas dataframe, dataframe with only the first encounter for a given patient
    '''
    first_encounter_df = df
    first_encounter_df.sort_values(by='encounter_id', inplace = True)
    first_encounter_df.drop_duplicates(subset ="patient_nbr", 
                         keep = 'first', inplace = True)
    
    return first_encounter_df


#Question 6
def patient_dataset_splitter(df, patient_key='patient_nbr'):
    '''
    df: pandas dataframe, input dataset that will be split
    patient_key: string, column that is the patient id

    return:
     - train: pandas dataframe,
     - validation: pandas dataframe,
     - test: pandas dataframe,
    '''
    processed_df_copy = df
    train = processed_df_copy.sample(frac=0.60, random_state=33)
    remaining_df = processed_df_copy.drop(train.index)
    
    test = remaining_df.sample(frac=0.50, random_state=33)
    validation = remaining_df.drop(test.index, axis=0)
    
    return train, validation, test

#Question 7

def create_tf_categorical_feature_cols(categorical_col_list,
                              vocab_dir='./diabetes_vocab/'):
    '''
    categorical_col_list: list, categorical field list that will be transformed with TF feature column
    vocab_dir: string, the path where the vocabulary text files are located
    return:
        output_tf_list: list of TF feature columns
    '''

    output_tf_list = []
    for c in categorical_col_list:
        vocab_file_path = os.path.join(vocab_dir,  c + "_vocab.txt")
        '''
        Which TF function allows you to read from a text file and create a categorical feature
        You can use a pattern like this below...
        tf_categorical_feature_column = tf.feature_column.......

        '''
        tf_cat_col = tf.feature_column.categorical_column_with_vocabulary_file(
        key = c, vocabulary_file = vocab_file_path, vocabulary_size=None, dtype=tf.dtypes.string,
        default_value=None, num_oov_buckets=0
        )
        dim = tf_cat_col[2]       
        
        output_tf_list.append(tf.feature_column.embedding_column(tf_cat_col, dimension=dim))
    return output_tf_list

#Question 8

def create_tf_numeric_feature(df, col, MEAN, STD, default_value=0):
    '''
    col: string, input numerical column name
    MEAN: the mean for the column in the training data
    STD: the standard deviation for the column in the training data
    default_value: the value that will be used for imputing the field

    return:
        tf_numeric_feature: tf feature column representation of the input field
    '''
    #print(col, MEAN, STD)
    mean, std = MEAN, STD
    def normalize_column(col):
        return (col - mean)/std
        
    normalize_numeric_with_zscore = normalize_column
    
    tf_numeric_feature = tf.feature_column.numeric_column(
        col, shape=(1,), default_value=None, dtype=tf.dtypes.float32, \
        normalizer_fn= normalize_numeric_with_zscore)
    
    
    return tf_numeric_feature

#Question 9
def get_mean_std_from_preds(diabetes_yhat):
    '''
    diabetes_yhat: TF Probability prediction object
    '''
    
    m = diabetes_yhat.mean()
    s = diabetes_yhat.stddev()
    return m, s

# Question 10
def get_student_binary_prediction(df, col,col_dev):
    '''
    df: pandas dataframe prediction output dataframe
    col: str,  probability mean prediction field
    return:
        student_binary_prediction: pandas dataframe converting input to flattened numpy array and binary labels
    '''
    student_binary_prediction = []
    
    actual_arr = df.iloc[:,1].astype(float).to_numpy()
    
    lower_limit = (df['pred_mean'].astype(float) - df.pred_std.astype(float)).to_numpy()
    
    upper_limit = (df['pred_mean'].astype(float) + df.pred_std.astype(float)).to_numpy()
    
    for i in range(len(actual_arr)):
        #print(lower_limit[i])
        in_range = lower_limit[i] <= actual_arr[i] <= upper_limit[i] # in np.arange(lower_limit[i], upper_limit[i])
        student_binary_prediction.append(in_range)
        
    np.array(student_binary_prediction, dtype=bool)
    return student_binary_prediction
