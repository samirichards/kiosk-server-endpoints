from flask import Flask, request

app = Flask(__name__)


@app.route('/feedback', methods=['POST'])
def handle_feedback():
    location_id = request.form['location_id']
    feedback = request.form['feedback']

    #Initial stuff, just get it working for now, need to add API keys and stuff

    return 'Success'

@app.route('/test')
def handle_test():
    f = open("test.txt", "a")
    f.write("test endpoint reached")
    f.close()
    return 'Success'


if __name__ == '__main__':
    app.run()