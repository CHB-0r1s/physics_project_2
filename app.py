from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    vectors = [
        [100, 100, 200, 200],  # Пример вектора: (100, 100) -> (200, 200)
        [300, 300, 400, 500],  # Еще один пример: (300, 300) -> (400, 500)
        # Добавьте здесь другие ваши векторы в нужном формате
    ]

    return render_template('index.html', vectors=vectors)


if __name__ == '__main__':
    app.run(debug=True)
