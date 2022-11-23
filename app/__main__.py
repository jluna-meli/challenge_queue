from dotenv import load_dotenv
from app import create_app

app = create_app()
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    load_dotenv()
    app.run(debug=True, port="8000", host="0.0.0.0")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
