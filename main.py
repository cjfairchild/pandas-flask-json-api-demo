import pandas as pd
from flask import Flask, request

app = Flask(__name__)

INIT_DATASET = "MOCK_DATA.json"

db_df = pd.read_json(INIT_DATASET)


@app.route('/read', methods=['GET'])
def read_all():
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
    print(request.json)
    query_form = request.json

    db_df.drop(index=query_form['id'], inplace=True)

    return "OK"


if __name__ == '__main__':
    app.run(debug=True)