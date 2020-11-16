# -*- coding: utf-8 -*-
"""
Created on Sun Nov 15 00:20:02 2020

@author: 28dan
"""
import base64
import pandas as pd
import io

def parse_contents(contents, filename, date):
    """
    Here we read file upload in 'bulk upload'

    Parameters
    ----------
    contents : File, expected csv or xlsx
        File content with data from houses to calculate the appraisal.
    filename : String
        Name of the upload file.
    date : Datetime
        Date of file last modification.

    Returns
    -------
    df: DataFrame
        DataFrame with content of upload file.

    """
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename or 'xlsx' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return 'There was an error, please upload a csv or xlsx file.'
    return df