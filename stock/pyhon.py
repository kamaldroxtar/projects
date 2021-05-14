from flask.helpers import url_for
from yahoo_fin import stock_info
from plyer import notification
from flask import Flask, redirect, url_for, request

app = Flask(__name__)


@app.route('/work/<brand>/<enternow>/<exitnow>')
def work(brand, enternow, exitnow):
    title = "Stock Alert!"
    while True:

        price = stock_info.get_live_price(brand)

        if price < float(enternow):
            message = "It's time to buy your stock. The current price is : " + \
                str(price)
            notification.notify(title=title,
                                message=message,
                                app_icon=None,
                                timeout=10,
                                toast=False)
            return message
        elif price > float(exitnow):
            message = "It's time to sell your stock. The current price is : " + \
                str(price)
            notification.notify(title=title,
                                message=message,
                                app_icon=None,
                                timeout=10,
                                toast=False)
            return message


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        symbol = request.form['Stock_name']
        entry = request.form['Entry_price']
        exit = request.form['Exit_price']
        return redirect(url_for('work', brand=symbol, enternow=entry, exitnow=exit))
    else:
        symbol = request.args.form['Stock_name']
        entry = request.args.form['Entry_price']
        exit = request.args.form['Exit_price']
        return redirect(url_for('work', brand=symbol, enternow=entry, exitnow=exit))


if __name__ == ('__main__'):
    app.run(debug=True)
