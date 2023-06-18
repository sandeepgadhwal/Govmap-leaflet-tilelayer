from flask import Flask, request, redirect
app = Flask(__name__)

@app.route('/')
def hello():
	return "Hello World!"

@app.route('/layers/<string:layer>/<string:level>/<string:row>/<string:col>')
def proxy(layer, level, row, col):
	col, ext = col.split('.')
	level = level[1:].zfill(2)
	row = format(int(row[1:]), 'x').zfill(8)
	col = format(int(col[1:]), 'x').zfill(8)
	url = f"https://cdn.govmap.gov.il/{layer}/L{level}/R{row}/C{col}.{ext}"
	return redirect(url, code=302)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8000)