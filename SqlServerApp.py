from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'SQL123',
    'database': 'sql5751083',
}

@app.route('/')
def home():
    return "welcomeee!"
    
@app.route('/schedule', methods=['GET'])
def get_schedule():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)

        query = """
        SELECT
            d.dayOfTheWeek,
            np.number_pair,
            c.NumberCabinet,
            t.FirstName,
            t.LastName,
            t.PatronymicName,
            ty.type_name,
            g.name_group
        FROM
            pair p
        JOIN day d ON p.id_day = d.id_day
        JOIN numberpair np ON p.id_numberPair = np.id_numberPair
        JOIN cabinet c ON p.id_cabinet = c.id_cabinet
        JOIN teachers t ON p.id_teacher = t.id_teacher
        JOIN `group` g ON p.id_group = g.id_group
        JOIN `type` ty ON p.id_type = ty.id_type
        WHERE d.id_day = 1;
        """
        cursor.execute(query, (day_id,))
        schedule = cursor.fetchall()

        cursor.close()
        connection.close()

        if not schedule:
            return jsonify({'message': 'No schedule found for this day'}), 404

        return jsonify(schedule)
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500


if __name__ == '__main__':
    app.run(debug=True)
