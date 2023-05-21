from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    selected_genres = request.form.getlist('genre')
    selected_categories = request.form.getlist('category')
    selected_century = request.form.get('century')
    selected_country = request.form.get('country')

    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()

    query = '''
        SELECT * FROM books
        WHERE genre IN ({}) OR category IN ({})
    '''.format(','.join('?' * len(selected_genres)), ','.join('?' * len(selected_categories)))
    parameters = selected_genres + selected_categories

    if selected_century != 'Any':
        query += ' AND century = ?'
        parameters.append(selected_century)

    if selected_country != 'Any':
        query += ' AND country = ?'
        parameters.append(selected_country)

    cursor.execute(query, parameters)
    rows = cursor.fetchall()

    recommended_books = []
    unique_titles = set()  # Для отслеживания уникальных названий книг

    for row in rows:
        title = row[1]
        if title not in unique_titles:  # Проверка уникальности названия книги
            book = {
                'title': title,
                'genre': row[2],
                'category': row[3],
                'century': row[4],
                'country': row[5]
            }
            recommended_books.append(book)
            unique_titles.add(title)

    conn.close()

    if len(recommended_books) == 0:
        return render_template('no_books.html')

    return render_template('recommend.html', books=recommended_books)

if __name__ == '__main__':
    app.run(debug=True)
