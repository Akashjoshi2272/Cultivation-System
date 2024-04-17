import pickle
import numpy as np



global N,P,K,Ph
N,P,K,Ph=0,0,0,0

from flask import Flask, render_template, request, redirect,url_for
app = Flask(__name__,static_url_path='/static')

@app.route('/')
def home():
    global N,P,K,Ph
    N,P,K,Ph=0,0,0,0
    return render_template('Home_2.html')

@app.route('/map')
def map():
    return render_template('index.html')

@app.route('/back_home')
def back_home():
    global N,P,K,Ph
    N,P,K,Ph=0,0,0,0
    return redirect(url_for('home'))


@app.route('/Predict')
def prediction():
    return render_template('Index2.html')

@app.route('/back')
def back():
    return redirect(url_for('prediction'))

@app.route('/process_marker_data', methods=['POST'])
def process_marker_data():
    marker_data = request.json
    # Process the marker data as needed
    # print('Marker data received:', marker_data)
    global N,P,K,Ph
    N=marker_data['N(kg/h)']
    P=marker_data['P(kg/h)']
    K=marker_data['K(kg/h)']
    Ph=marker_data['PH']
    # You can now process the marker data in Python
    # For example, you can save it to a database or perform any other operations
    return 'Marker data processed successfully'


@app.route('/PredictMap')
def prediction_map():
    return render_template('Index1.html',N=N,P=P,K=K,Ph=Ph)

@app.route('/form', methods=["POST"])
def brain():
    try:
        global N,P,K,Ph
        if N!=0 and P!=0 and K!=0 and Ph!=0:
            pass
        else:
            N=float(request.form['Nitrogen'])
            P=float(request.form['Phosphorus'])
            K=float(request.form['Potassium'])
            Ph=float(request.form['ph'])
    except:
        return render_template('error.html')
    Temperature=float(request.form['Temperature'])
    Humidity=float(request.form['Humidity'])
    Rainfall=float(request.form['Rainfall'])
    classifier=str(request.form['classifier'])

    values=[N,P,K,Temperature,Humidity,Ph,Rainfall]
    
    if Ph>0 and Ph<=14 and Temperature<100 and Humidity>0:
        # model = pickle.load(open(r'C:\Users\kusha\Project2\Crop-Recommendation-system--main\Crop recommendation system\RFC.sav', 'rb'))
        if classifier=="RFC":
            model = pickle.load(open(r"cropRFC.sav", 'rb'))
        elif classifier=="DTC":
            model = pickle.load(open(r"cropDTC.sav", 'rb'))
        elif classifier=="GNB":
            model = pickle.load(open(r"cropGaussianNB.sav", 'rb'))
        elif classifier=="LOGREG":
            model = pickle.load(open(r"cropLogReg.sav", 'rb'))
        else:
            pass
        # Predict probabilities for each class label
        probabilities = model.predict_proba([values])

        # Get the indices of sorted probabilities in descending order
        sorted_indices = np.argsort(probabilities, axis=1)[:, ::-1]

        # Extract the top two classes and their probabilities
        top_classes = sorted_indices[:, :2]
        top_probabilities = np.take_along_axis(probabilities, sorted_indices, axis=1)[:, :2]

        # Evaluate model performance
        y_pred = model.predict([values])
        top_labels = model.classes_[top_classes]

        # print(f"Instance:")
        # print(f"  Most likely label: {top_labels[0, 0]}, Probability: {top_probabilities[0, 0]:.4f}")
        # print(f"  Second most likely label: {top_labels[0, 1]}, Probability: {top_probabilities[0, 1]:.4f}")

        fert1,fert2="",""
        crop1="Preference 1: "+str(top_labels[0, 0]).capitalize()
        crop2="Preference 2: "+str(top_labels[0, 1]).capitalize()
        #FERTILIZER1
        if top_labels[0,0]=="rice":
            fert1="Urea, Ammonium sulfate, Single Superphosphate (SSP)"
        elif top_labels[0,0]=="banana":
            fert1="Organic fertilizers, Micronutrient fertilizers"
        elif top_labels[0,0]=="blackpepper":
            fert1="Organic Manures, Magnesium Sulphate (Epsom Salt),Micronutrient Fertilizers"
        elif top_labels[0,0]=="arecanut":
            fert1="Urea, Foliar fertilizers"            
        else:
            fert1="Organic Manures"

        #FERTILIZER2
        if top_labels[0,1]=="rice":
            fert2="Urea, Ammonium sulfate, Single Superphosphate (SSP)"
        elif top_labels[0,1]=="banana":
            fert2="Organic fertilizers, Micronutrient fertilizers"
        elif top_labels[0,1]=="blackpepper":
            fert2="Organic Manures, Magnesium Sulphate (Epsom Salt),Micronutrient Fertilizers"
        elif top_labels[0,1]=="arecanut":
            fert2="Urea, Foliar fertilizers"
        else:
            fert2="Organic Manures"
        # arr = [values]
        # acc = model.predict(arr)
        #print(acc)
        return render_template('prediction2.html', prediction2=str(crop1),prediction1=str(crop2),fert1=fert1,fert2=fert2)
    else:
        return render_template('error.html')

if __name__ == '__main__':
    app.run(debug=True)















