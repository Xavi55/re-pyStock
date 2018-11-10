from flask import Flask, render_template, jsonify
from flask import request as body

import stock

app = Flask(__name__)
@app.route('/')
def index():
	return render_template('stock.html')

@app.route('/api/getStock')
def get():
    n = body.args['stock']
    print '\nLoading',n,'\n'
    x = stock.stock(n)
    
    nums = x.getPrices()
    fin = x.getFin()
    return jsonify({
        'n':x.getName(),
        'p':nums[0],
        'diff':nums[1],
        'op':nums[2],
        'cap':fin[0],
        'eps':fin[1],
        'pe':fin[2],
        'de':fin[3],
        'pb':fin[4]
        })
@app.route('/api/fetchP')
def fetchP():    
    n = body.args['stock']
    x = stock.stock(n)
    nums = x.getPrices()
    return jsonify({
        'n':n,
        'p':nums[0],
        'diff':nums[1]
        })
if __name__=="__main__":
    Flask.run(app,debug=False)