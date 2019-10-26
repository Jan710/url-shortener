from flask import Flask, request, render_template, redirect
import csv
import shortuuid

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


def write_to_csv(data, new_data):
    with open('database.csv', mode='a', newline='') as database:
        url = data["url"]
        csv_writer = csv.writer(database, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([url, new_data])


def get_url(url):
    with open("database.csv", "r") as f:
        reader = csv.reader(f)
        for line_num, content in enumerate(reader):
            if content[1] == url:
                return redirect(content[0])
        else:
            return 'done'


@app.route('/short', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        try:
            data = request.form.to_dict()
            new_data = shortuuid.ShortUUID().random(length=4)
            write_to_csv(data, new_data)
            return render_template('index.html', old_url=data["url"], new_url='127.0.0.1:5000/' + new_data)
        except:
            return 'did not save to database'
    else:
        return 'something went wrong'


@app.route('/<url>')
def test(url):
    return get_url(url)
