from flask import Flask,request,render_template
import numpy as np 
import pickle 

# create flask app
app = Flask(__name__)


# to handle input
genders_to_int ={
    'YES:1',
    'NO:0'
}

married_to_int ={
   'YES:1',
   'NO:0'
} 

eduaction_to_int ={
    'GRADUATED':1,
    'NOT GRADUATED':0
}

dependents_to_int ={
    '0':0,
    '1':1,
    '2':2,
    '3+':3
}

self_employment_to_int ={
    'YES:1',
    'NO:0'
}

# basic routing
@app.route('/',methods=['GET','POST'])
def loan_application():

    if request.method =="GET":
       return render_template('loan_application.html')
    
    else:
        genders_type= request.form['genders_type']
        marital_status= request.form['marital_status']
        dependents= request.form['dependents']
        eduaction_status= request.form['education_status']
        applicantIncome= float(request.form['applicantIncome'])
        coapplicantIncome= float(request.form['coapplicantIncome'])
        loan_amnt =float(request.form['loan_amnt'])
        term_d= int(request.form['term_d'])
        credit_history = int(request.form['credit_history'])
        property_area = request.form['property_area']
    
        x=np.ones(21)
        x[0]=1
        x[1]=loan_amnt
        x[2]=0
        x[3]=1
        x[4]=0
        x[5]=1
        x[6]=1
        x[7]=0
        x[8]=0
        x[9]=0
        x[10]=1
        x[11]=0
        x[12]=0
        x[13]=1
        x[14]=0
        x[15]=1
        x[16]=0
        x[17]=applicantIncome+coapplicantIncome
        x[18]=applicantIncome+coapplicantIncome
        x[19]=loan_amnt/term_d
        x[20]=(applicantIncome+coapplicantIncome)-loan_amnt/term_d

        with open('models/logistic_model.pkl','rb') as f:
            lrm=pickle.load(f)
            pred=lrm.predict([x])[0]

            if pred ==1:
                result="LOAN APPROVED"
            else:
                result="LOAN REJECTED"

        return render_template('loan_application.html',res=result)





#route with variable
@app.route('/success/<int:score>',methods=['GET'])
def success(score):
    return f'you got {score}'

#route to load form
@app.route('/form',methods=['GET','POST'])
def form():
    if request.method == 'GET':
        return render_template('form.html')
    else:
        maths=int(request.form['Maths'])
        science=int(request.form['Science'])
        avg=maths+science
        
        return render_template('form.html',score=avg)
    
 
    

if __name__=="__main__":
    app.run(debug=True)


