import json
import numpy as np
import pandas as pd
from flask import Flask, request

app = Flask(__name__)

INIT_DATASET = "MOCK_DATA.json"


db_df = pd.read_json(INIT_DATASET)


@app.route("/reset", methods=['POST'])
def reload_df():
    """
    Reload the dataframe from the source file.
    :return: "OK" if OK.
    """
    global db_df

    db_df = pd.read_json(INIT_DATASET)

    print("Resetting.")

    return "OK"


@app.route('/read', methods=['GET'])
def read_all():
    """
    Read all queries specified by parameters. Params are:
        - sort_column (Optional), which is the column to sort by (ascending).
        - filtering (Optional), filter which results are selected.
            - column, which column are we querying?
            - operator, which operation (== only implemented!) to run against the specified value.
            - value, the value which has the operator applied on it to check against the "column" above!
        - pagination (Optional) - to only return a subset of the query.
            - offset
            - limit
    :return: A JSON string of the query as described above.
    """
    print(request.json)
    query_form = request.json
    query_df = db_df.copy(deep=True)

    # 1. Sort
    if 'sort_column' in query_form.keys():
        query_df = query_df.sort_values(by=query_form['sort_column'])

    # 2. Filter
    if 'filtering' in query_form.keys():
        operator = query_form['filtering']['operator']
        column = query_form['filtering']['column']
        value = query_form['filtering']['value']
        if operator == "==":
            query_df = query_df.loc[query_df[column] == value]

    # 3. Pagination
    if 'pagination' in query_form.keys():
        limit = query_form['pagination']['limit']
        offset = query_form['pagination']['offset']
        query_df = query_df[offset:offset + limit]

    return query_df.to_json()


@app.route('/delete', methods=['POST'])
def delete_record():
    """
    Delete a record by it's id.
    :return: "OK" if OK.
    """
    print(request.json)
    query_form = request.json

    db_df.drop(index=query_form['id'], inplace=True)

    return "OK"


@app.route('/update', methods=['POST'])
def update_record():
    """
     Update a record by it's id.

     Any value specified will overwrite an existing one in the datastore.
    :return: A JSON string of the updated record affected by the query.
    """
    print(request.json)
    query_form = request.json
    _id = query_form['id']

    db_df.loc[db_df.id == _id, query_form.keys()] = query_form.values()
    return db_df.loc[db_df.id == _id].to_json()


def append_age():
    """
    Add age to the dataset based on the date of birth column.

    This function was adapted from:
     - https://www.codegrepper.com/code-examples/python/calculating+age+from+date+of+birth+in+pandas
    :return: None
    """
    now = pd.Timestamp('now')
    db_df['dob'] = pd.to_datetime(db_df['date_of_birth'], format='%d/%m/%Y')  # 1
    db_df['dob'] = db_df['dob'].where(db_df['dob'] < now, db_df['dob'] - np.timedelta64(100, 'Y'))  # 2
    db_df['age'] = (now - db_df['dob']).astype('<m8[Y]')  # 3


@app.route('/average_by', methods=['POST'])
def get_average():
    """
    Get the median, mode and average of a target_column by each unique value another column.
        - category - A column name of which each unique value will have it's averages calculated.
        - target_column is the column to take averages of. If it's not a number, strange things may happen.
    :return: A json string as described from above.
    """
    query_form = request.json
    category = query_form['category']
    targ_column = query_form['target_column']

    # Handle if Age was asked for as only D.O.B was provided.
    append_age()
    unique_category = db_df[category].unique()

    output_results = {"category": dict()}

    for unique_category in unique_category:
        output_results['category'][unique_category] = {"mean": None, "mode": None, "median": None}

        mean = db_df.loc[db_df[category] == unique_category][targ_column].mean()
        median = db_df.loc[db_df[category] == unique_category][targ_column].median()
        mode = db_df.loc[db_df[category] == unique_category][targ_column].mode()

        output_results['category'][unique_category]['mean'] = mean
        output_results['category'][unique_category]['median'] = median
        output_results['category'][unique_category]['mode'] = list(mode)

    print(output_results)
    return json.dumps(output_results)


@app.route('/describe_column', methods=['POST'])
def get_stats():
    """
    Get the pandas description of the data in a column.
    :return:
    """
    query_form = request.json
    category = query_form['category']

    return db_df[category].describe().to_json()


if __name__ == '__main__':
    app.run(debug=True)
