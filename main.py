from flask import Flask, request, jsonify
from datetime import datetime
import configuration_provider
import person

app = Flask(__name__)
loans = []


@app.route('/loan', methods=['POST'])
def apply():
    name = request.json.get('name')
    amount = request.json.get('amount')
    term = request.json.get('term')
    personal_id = request.json.get('personal_id')

    if person.Person.is_person_blacklisted(personal_id):
        return jsonify({'error': 'This person is blacklisted.'}), 400

    if person.Person.has_too_many_applications_in_last_24_hours(personal_id, loans):
        return jsonify({'error': 'The borrower has too many loan applications within the past 24 hours.'}), 400

    monthly_interest = configuration_provider.ConfigurationProvider.get_monthly_interest_rate()
    monthly_repayment_amount = person.Person.calculate_monthly_repayement_amount(amount, monthly_interest, term)
    repayment_amount = round(monthly_repayment_amount * term, 2)

    loan = {'name': name, 'personal_id': personal_id, 'amount': amount, 'term': term, 'date': datetime.now(),
            'monthly_interest': monthly_interest, 'repayment_amount': repayment_amount,
            'monthly_repayment_amount': monthly_repayment_amount}
    loans.append(loan)
    return jsonify({'message': 'Loan application submitted successfully!'}), 200


@app.route('/loan', methods=['GET'])
def get_loans_by_id():
    personal_id = request.args.get('personal-id')
    borrower_loans = []
    for loan in loans:
        if loan['personal_id'] == personal_id:
            borrower_loans.append(loan)

    if len(borrower_loans) == 0:
        return jsonify({'message': 'No loans were found.'}), 404
    return jsonify({'loans': borrower_loans}), 200


if __name__ == '__main__':
    app.run(debug=True)
