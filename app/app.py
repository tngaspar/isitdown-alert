from flask   import render_template, request, Flask, json
from jinja2  import TemplateNotFound
from datetime import date, timedelta
import sys

# all paths are relative to the project root directory
sys.path.append("..")
from utils.db import PostgresDB

def get_table_from_sql_file(sql_file_path: str):
    with open(sql_file_path, 'r') as file:
        sql_str = file.read()
    conn = PostgresDB()
    return conn.get_table_from_sql(sql_str)


app = Flask(__name__)

# App main route + generic routing
@app.route('/')
def index():
    # get counts
    counts = get_table_from_sql_file("../sql/DML/counts.pgsql")
    counts = list(counts[0])
    
    # get number of requests for last 7days
    num_last_7d_db = get_table_from_sql_file("../sql/DML/num_requests_last_7days.pgsql")
    num_last_7d_db = [list(elem) for elem in num_last_7d_db]
    
    # fill days with no records in db with 0s
    today = date.today()
    num_last_7d = [[date, 0, 0] for date in [today - timedelta(days=day) for day in range(7)]]
    for date_db, total_db, failed_db in num_last_7d_db:
        for i, elem in enumerate(num_last_7d):
            if elem[0] == date_db:
                num_last_7d[i][1] = total_db
                num_last_7d[i][2] = failed_db
    
    # convert datetime to string format, reverse list
    num_last_7d = [[str(elem[0]), elem[1], elem[2]] for elem in num_last_7d[::-1]]
    # transpose list
    num_last_7d = list(zip(*num_last_7d))

    # Scheduled checks section
    webpages = get_table_from_sql_file("../sql/DML/active_webpages_with_count.pgsql")
    print(webpages)

    return render_template('index.html', counts=counts, num_last_7d=num_last_7d, webpages=webpages)


@app.route('/history')
def history():
    history = get_table_from_sql_file("../sql/DML/last_history_table.pgsql")
    return render_template('history.html', history=history)

@app.route('/<path>')
def index_path(path):
    try:

        # Detect the current page
        segment = get_segment( request )

        # Serve the file (if exists) from app/templates/FILE.html
        return render_template( path, segment=segment )
    
    except TemplateNotFound:
        return render_template('page-404.html'), 404

# Helper - Extract current page name from request 
def get_segment( request ): 

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment    

    except:
        return None   


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)