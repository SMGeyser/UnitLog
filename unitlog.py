from learningflask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)  # Allows index.html to make fetch requests to this Python server

# MySQL database credentials
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'YOUR_PASSWORD',
    'database': 'unitlogdatabase'
}

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    # Read query parameter passed from #property-select in index.html
    property_filter = request.args.get('property')

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)  # Returns rows as Python dictionaries

    sql = "SELECT * FROM tasks"
    params = []

    # Handle dropdown values ("urgent", "737", "709", "lodge") from index.html
    if property_filter == 'urgent':
        sql += " WHERE is_urgent = 1"
    elif property_filter:
        sql += " WHERE property_id = %s"
        params.append(property_filter)

    cursor.execute(sql, params)
    tasks = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(tasks)

if __name__ == '__main__':
    app.run(port=5000, debug=True)