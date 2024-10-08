#Data Preprocessing Pipeline

# In order to enhance the quality, consistency, and analytical usefulness of raw data, data preprocessing entails altering and transforming it.
# A data preparation pipeline is an automated, methodical process that integrates several preprocessing stages into a seamless workflow. 
# For data professionals, it acts as a road map, assisting them with the conversions and computations required to clean up and get ready data for analysis.

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.impute import KNNImputer

def data_preprocessing_pipeline(data):

    #Identify numeric and categorical features
    numeric_features = data.select_dtypes(include=['float', 'int']).columns
    categorical_features = data.select_dtypes(include=['object']).columns

    #Handle missing values in numeric features using the KNN technique
    data[numeric_features] = handle_missing_values(data[numeric_features])

    #Handle missing values in categorical features using mode value.
    data[categorical_features] = data[categorical_features].fillna(data[categorical_features].mode().iloc[0])

    #Alternative; missing values in categorical features replaced with value "unknown".
    #data[categorical_features] = data[categorical_features].fillna('Unknown')

    #Detect and handle outliers in numeric features using IQR
    for feature in numeric_features:
        Q1 = data[feature].quantile(0.25)
        Q3 = data[feature].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - (1.5 * IQR)
        upper_bound = Q3 + (1.5 * IQR)
        data[feature] = np.where((data[feature] < lower_bound) | (data[feature] > upper_bound),
                                data[feature].mean(), data[feature])

    # Normalize numeric features 
    #Using Standardization (Z-score Normalization) method; (Transforms features to have a mean of 0 and a standard deviation of 1.)
    scaler = StandardScaler()
    data[numeric_features] = scaler.fit_transform(data[numeric_features])  

    return data

#Use KNN Imputer to impute missing values based on the values of other features.
def handle_missing_values(data):
    imputer = KNNImputer()
    data_imputed = pd.DataFrame(imputer.fit_transform(data), columns=data.columns)
    return data_imputed

#use IQR to handle outliers
def handle_outliers_iqr(data, threshold=1.5):
    Q1 = data.quantile(0.25)
    Q3 = data.quantile(0.75)
    IQR = Q3 - Q1

    lower_bound = Q1 - (threshold * IQR)
    upper_bound = Q3 + (threshold * IQR)

    return data[~((data < lower_bound) | (data > upper_bound)).any(axis=1)]

#Test the pipeline
data = pd.read_csv("data.csv")

print("Original Data:")
print(data)

cleaned_data = data_preprocessing_pipeline(data) 

print("Preprocessed Data:")
print(cleaned_data)
