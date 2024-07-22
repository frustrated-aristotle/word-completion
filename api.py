from flask import Flask, request, jsonify
import pyodbc

app = Flask(__name__)

# Configuration from appsettings.json
# Replace the connection string with your actual SQL Server connection string
connection_string = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-UBS1OB4;DATABASE=wordnet_db;Trusted_Connection=yes;"

def get_db_connection():
    return pyodbc.connect(connection_string)

@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    query = request.args.get('query', '')

    if not query:
        return jsonify([])

    conn = get_db_connection()
    cursor = conn.cursor()

    # SQL query to search for words containing the query
    sql_query = "SELECT word FROM words WHERE word LIKE ?"
    cursor.execute(sql_query, ('%' + query + '%',))
    results = cursor.fetchall()

    conn.close()

    # Convert results to a list of strings
    words = [row.word for row in results]

    return jsonify(words)

if __name__ == '__main__':
    app.run(debug=True)
