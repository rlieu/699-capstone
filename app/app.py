from flask import Flask, render_template, request
import pickle 

app = Flask(__name__)
# model = pickle.load(open('classification_model.pkl','rb')) #read mode

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/predict", methods=['GET','POST'])
def predict():
    if request.method == 'POST':
        data = request.get_data()
        print(data)
        #get prediction
        # input_cols = [data.values()]
        # prediction = model.predict(input_cols)
        # output = round(prediction[0], 2)
        # return render_template("index.html", prediction_text='Your predicted annual Healthcare Expense is $ {}'.format(output))
    
if __name__ == "__main__":
    app.run(debug=True)