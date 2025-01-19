from website import create_app

app = create_app()

if __name__ == '__main__':
    app.secret_key='12345'
    app.run(debug=True)