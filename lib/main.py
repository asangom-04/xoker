from flask import Flask, render_template, abort, request

import json

app = Flask(__name__)

# Cargar la información de los libros desde el archivo JSON
with open('books.json') as f:
    books_data = json.load(f)


@app.route('/')
def home():
    return render_template('index.html', books=books_data)


@app.route('/libro/<isbn>')
def libro_detalle(isbn):
    # Buscar el libro por su ISBN
    book = next((book for book in books_data if book['isbn'] == isbn), None)
    if book is None:
        abort(404)

    return render_template('libro.html', book=book)


@app.route('/libro')
def libro_detalle_query():
    isbn = request.args.get('isbn')
    if isbn is None:
        abort(404)

    # Buscar el libro por su ISBN
    book = next((book for book in books_data if book['isbn'] == isbn), None)
    if book is None:
        abort(404)

    return render_template('libro.html', book=book)


@app.route('/categoria')
def categorias():
    # Obtener todas las categorías únicas de los libros
    categorias = set(category for book in books_data for category in book['categories'])

    return render_template('categorias.html', categorias=categorias)


@app.route('/categoria/<categoria>')
def libros_por_categoria(categoria):
    # Filtrar los libros por categoría
    libros_categoria = [book for book in books_data if categoria in book['categories']]

    return render_template('categoria.html', categoria=categoria, libros=libros_categoria)


if __name__ == '__main__':
    app.run(debug=True)
