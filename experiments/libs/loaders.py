import os
import pandas as pd
import arff
import numpy as np

from functools import reduce


_FRAUD_PATH = 'fraud_detection', 'credit_card_fraud_kaggle', 'creditcard.csv'
_IOT_PATH = 'iot', 'sensor_stream_berkeley', 'sensor.arff'
_AIRLINE_PATH = 'airline', 'airline_14col.data'


def _get_datapath():
    try:
        datapath = os.environ['MOUNT_POINT']
    except KeyError:
        print("MOUNT_POINT not found in environment. Defaulting to /fileshare")
        datapath = '/fileshare'
    return datapath


def load_fraud():
    """ Loads the credit card fraud data

    The datasets contains transactions made by credit cards in September 2013 by european cardholders.
    This dataset presents transactions that occurred in two days, where we have 492 frauds out of 284,807 transactions.
    The dataset is highly unbalanced, the positive class (frauds) account for 0.172% of all transactions.
    It contains only numerical input variables which are the result of a PCA transformation.

    Unfortunately, due to confidentiality issues, we cannot provide the original features and more background information about
    the data.
    Features V1, V2, ... V28 are the principal components obtained with PCA, the only features which have not been transformed
    with PCA are 'Time' and 'Amount'. Feature 'Time' contains the seconds elapsed between each transaction and the first
    transaction in the dataset.
    The feature 'Amount' is the transaction Amount, this feature can be used for example-dependant cost-senstive learning. 
    Feature 'Class' is the response variable and it takes value 1 in case of fraud and 0 otherwise.
    Given the class imbalance ratio, we recommend measuring the accuracy using the Area Under the Precision-Recall Curve
    (AUPRC).
    Confusion matrix accuracy is not meaningful for unbalanced classification.

    The dataset has been collected and analysed during a research collaboration of Worldline and the Machine Learning Group
    (http://mlg.ulb.ac.be) of ULB (Universite Libre de Bruxelles) on big data mining and fraud detection. More details 
    on current  and past projects on related topics are available on http://mlg.ulb.ac.be/BruFence 
    and http://mlg.ulb.ac.be/ARTML
    Please cite: Andrea Dal Pozzolo, Olivier Caelen, Reid A. Johnson and Gianluca Bontempi. Calibrating Probability with
    Undersampling for Unbalanced Classification. In Symposium on Computational Intelligence and Data Mining (CIDM), IEEE, 2015

    Returns
    -------
    pandas DataFrame

    """
    return pd.read_csv(reduce(os.path.join, _FRAUD_PATH, _get_datapath()))


def load_iot():
    """ Loads iot data

    Sensor stream contains information (temperature, humidity, light, and sensor voltage) collected from 54 sensors deployed
    in Intel Berkeley Research Lab. The whole stream contains consecutive information recorded over a 2 months
    period (1 reading per 1-3 minutes). I used the sensor ID as the class label, so the learning task of the stream is
    to correctly identify the sensor ID (1 out of 54 sensors) purely based on the sensor data and the corresponding recording
    time.

    While the data stream flow over time, so does the concepts underlying the stream. For example, the lighting during
    the working hours is generally stronger than the night, and the temperature of specific sensors (conference room)
    may regularly rise during the meetings.

    Returns
    -------
    pandas DataFrame
    """
    dataset = arff.load(open(reduce(os.path.join, _IOT_PATH, _get_datapath())))
    columns = [i[0] for i in dataset['attributes']]
    return pd.DataFrame(dataset['data'], columns=columns)


def load_airline():
    """ Loads airline data
    The dataset consists of a large amount of records, containing flight arrival and departure details for all the 
    commercial flights within the USA, from October 1987 to April 2008. Its size is around 116 million records and 
    5.76 GB of memory.
    There are 13 attributes, each represented in a separate column: Year (1987-2008), Month (1-12), Day of Month (1-31), 
    Day of Week (1:Monday - 7:Sunday), CRS Departure Time (local time as hhmm), CRS Arrival Time (local time as hhmm), 
    Unique Carrier, Flight Number, Actual Elapsed Time (in min), Origin, Destination, Distance (in miles), and Diverted
    (1=yes, 0=no). 
    The target attribute is Arrival Delay, it is a positive or negative value measured in minutes. 
    Link to the source: http://kt.ijs.si/elena_ikonomovska/data.html

    Returns
    -------
    pandas DataFrame
    """ 
    cols = ['Year', 'Month', 'DayofMonth', 'DayofWeek', 'CRSDepTime', 'CRSArrTime', 'UniqueCarrier', 'FlightNum', 'ActualElapsedTime', 'Origin', 'Dest', 'Distance', 'Diverted', 'ArrDelay']
    return pd.read_csv(reduce(os.path.join, _AIRLINE_PATH, _get_datapath()), names=cols)
                      