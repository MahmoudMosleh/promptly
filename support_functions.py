
import logging
import pandas as pd
import numpy as np
import json

# Create a custom logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def process_dataframe_columns(dataframe, columns):
    logger.info("Start process dataframe")
    for col in columns:
        try:
            print(col)
            data_type = columns[col]["type"]
            if data_type == "datetime":
                error_type = columns[col]["error"]
                dataframe[col] = pd.to_datetime(dataframe[col], errors=error_type)
            elif data_type == "Int64":
                dataframe[col].astype(pd.Int64Dtype())
            elif data_type == "func":
                process_func = columns[col]["process"]   
                if process_func:
                    dataframe = process_func(dataframe)
        except Exception as e:
            logger.error("Fail to process column {} due to {}".format(col, e)) 
            raise           
    logger.info("Finish process dataframe")
    return dataframe



def value_choice_extractor(dictionary):
    for key in dictionary.keys():
        try:
            if key == 'value':
                return dictionary['value']
            for key in dictionary.keys():
                if key == 'choice':
                    return dictionary['choice']
                return pd.NA
        except Exception as e:
            logger.error("Fail to process key {} due to {}".format(key, e))     
            raise


def answer_column_process(dataframe):
    logger.info("Start process answer_column")
    try:
        dataframe.loc[:, 'answers'] = dataframe.loc[:, 'answers'].apply(lambda val: json.loads(val) if isinstance(val, str) else val)
        df_answers = pd.json_normalize(dataframe['answers'])
        df_answers = df_answers.applymap(lambda answer: answer if not isinstance(answer, list)
                                                            else pd.NA if len(answer) == 0
                                                            else value_choice_extractor(answer[0]) if len(answer) == 1
                                                            else ', '.join([str(value_choice_extractor(dictionary)) for dictionary in answer]))
        df_answers = df_answers.dropna(axis=1, how='all')     
        #print("here-#########3-", df_answers.head(2))       
        dataframe = dataframe.drop("answers", axis=1)
        dataframe = dataframe.join(df_answers)                                            
        dataframe = dataframe.loc[dataframe["event_date"] > "2019-06-01", :]
        #print("after anser column-#########3-", dataframe.dtypes)       
        
    except Exception as e:
        logger.error("Fail to process answer_column due to".format(e)) 
        raise
    logger.info("Finish process answer_columne")
    return dataframe


def is_assessment_fully_completed_column_process(dataframe):
    logger.info("Start process column is_assessment_fully_completed_column_process")
    try:
        is_assessment_fully_completed = []
        for val in dataframe["completed_at"]:
            if pd.isna(val):
                is_assessment_fully_completed.append(False)
            else:
                is_assessment_fully_completed.append(True)
        dataframe["is_assessment_fully_completed"] = is_assessment_fully_completed
        dataframe = dataframe.loc[dataframe["is_assessment_fully_completed"] == True, :]
        dataframe = dataframe.drop(columns="is_assessment_fully_completed")
    except Exception as e:
        logger.error("Fail to process answer key column due to".format(e)) 
        raise
    logger.info("Finish process column is_assessment_fully_completed_column_process")
    return dataframe
