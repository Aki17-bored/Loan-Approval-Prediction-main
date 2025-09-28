from flask import Flask, request, render_template
import joblib
import numpy as np

app = Flask(__name__)

model  = joblib.load('Prediction Model')

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/contact')
def contact():
    return render_template("Contact.html")


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method ==  'POST':
        gender = request.form['gender']
        married = request.form['married']
        dependents = request.form['dependents']
        education = request.form['education']
        employed = request.form['employed']
        credit = float(request.form['credit'])
        area = request.form['area']
        ApplicantIncome = float(request.form['ApplicantIncome'])
        CoapplicantIncome = float(request.form['CoapplicantIncome'])
        LoanAmount = float(request.form['LoanAmount'])
        Loan_Amount_Term = float(request.form['Loan_Amount_Term'])

        # gender
        male = 1 if gender == "Male" else 0
        
        # married
        married_yes = 1 if married == "Yes" else 0

        # dependents
        dependents_1 = 1 if dependents=='1' else 0
        dependents_2 = 1 if dependents=='2' else 0
        dependents_3 = 1 if dependents=='3+' else 0

        # education
        not_graduate = 1 if education=="Not Graduate" else 0

        # employed
        employed_yes = 1 if employed=="Yes" else 0

        # property area
        semiurban = 1 if area=="Semiurban" else 0
        urban = 1 if area=="Urban" else 0

        # log transformations
        ApplicantIncomelog = np.log(ApplicantIncome)
        totalincomelog = np.log(ApplicantIncome+CoapplicantIncome)
        LoanAmountlog = np.log(LoanAmount)
        Loan_Amount_Termlog = np.log(Loan_Amount_Term)

        prediction = model.predict([[credit, ApplicantIncomelog,LoanAmountlog, Loan_Amount_Termlog, totalincomelog, male, married_yes, dependents_1, dependents_2, dependents_3, not_graduate, employed_yes,semiurban, urban ]])

        if(prediction=="N"):
            prediction="Sorry, You are not Eligible to avail loan services"
        else:
            prediction="Congratulations, You Can avail loan services"

        return render_template("prediction.html", prediction_text="{}".format(prediction))
    else:
        return render_template("prediction.html")


if __name__ == "__main__":
    app.run(debug=True , host='0.0.0.0')