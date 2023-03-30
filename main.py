from flask import Flask, request, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

blacklist = ['10000000000', '10000000001', '10000000002']
loans = []


def isBlacklisted(id):
    return id in blacklist


def tooManyApplications(id):
    now = datetime.now()
    applications = 0
    for loan in loans:
        if loan['borrower_id'] == id and now - loan['date'] <= timedelta(days=1):
            applications += 1
    return applications >= 3


@app.route('/loan', methods=['POST'])
def applyForLoan():
    name = request.json.get('name')
    id = request.json.get('id')
    amount = request.json.get('amount')
    term = request.json.get('term')

    if isBlacklisted(id):
        return jsonify({'error': 'This ID is blacklisted.'}), 400

    if tooManyApplications(id):
        return jsonify({'error': 'The borrower has too many loan applications within the past 24 hours.'}), 400

    loan = {'borrower_name': name, 'borrower_id': id, 'amount': amount, 'term': term, 'date': datetime.now()}
    loans.append(loan)
    print(loans)
    return jsonify({'message': 'Loan application submitted successfully!'}), 200


@app.route('/loan/<id>', methods=['GET'])
def getLoansById(id):
    borrower_loans = []
    for loan in loans:
        if loan['borrower_id'] == id:
            borrower_loans.append(loan)

    if len(borrower_loans) == 0:
        return jsonify({'message': 'No loans were found for the given ID.'}), 404
    return jsonify({'loans': borrower_loans}), 200


if __name__ == '__main__':
    app.run(debug=True)
