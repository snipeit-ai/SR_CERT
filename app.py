import os
from flask import Flask, request, render_template, send_file, flash
from werkzeug.utils import secure_filename
import pandas as pd


#import test_RL
import test_versions

app = Flask(__name__, template_folder='templates')


# Define the folder where uploaded files will be stored
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'Flask_generated')
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])
    
# Define the allowed extensions for file uploads
app.config['ALLOWED_EXTENSIONS'] = {'csv', 'jpg', 'jpeg', 'png'}

def file_checker(var):
      if var in request.files:
            file = request.files[var]
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                temp_path=os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(temp_path)
                return temp_path 

# Function to check if a file has an allowed extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route("/", methods=['GET','POST'])
def loadPage():
    if request.method == 'POST':
        # Handle form submission here

        # Get form data
        cert_code= request.form['query7']
        college_name = request.form['query1']
        location = request.form['query2']
        cert_type=request.form['query3']
        start_date = request.form['startDate']
        end_date = request.form['endDate']
        designation1 = request.form['query4']
        designation2 =request.form['query6']
        designation3 =request.form['query5']
        

        # Check if the College Logo Image ,Digital Signature Image is provided
        college_logo=file_checker('college_logo')
        digital_signature1 = file_checker('digital_signature1')
        digital_signature2 = file_checker('digital_signature2')
        digital_signature3 = file_checker('digital_signature3')
        background_path=file_checker('Template')

        threshold=0
        # Check if the CSV file is provided
        if 'csv_file' in request.files:
            csv_file = request.files['csv_file']
            if csv_file and allowed_file(csv_file.filename):
                #converting the input file to dataframe
                df=pd.read_csv(csv_file)
                # Format the dataframe 
                if 'Attendance(1/0)' in df.columns:
                    df=df[df['Attendance(1/0)']>threshold]   
                df=df.set_index('Sl.No')
                # Keep only the specified columns
                if 'Percentage' in df.columns:
                    df = df[[ 'Name', 'Course', 'College', 'Percentage']] 
                    
                else:
                    df = df[[ 'Name', 'Course', 'College']]
            

        # Check if the selected college exists in the DataFrame
        if college_name in df['College'].values:
        
            # Filter the DataFrame for the specified college
            df_college = df[df['College'] == college_name]
            df_college = df_college.reset_index()
            # Create certificate object with all required parameters
            zip_filename = test_versions.certificate_generator(df_college,background_path, college_logo, cert_type, cert_code, 
                                                               college_name, location, start_date, end_date, 
                                                               digital_signature1, designation1,digital_signature2, designation2,digital_signature3, designation3)
            # Return the zip file to the user
            response = send_file(zip_filename, as_attachment=True)
            #deleting the directory used for preview
            test_versions.delete_temporary_directory(f'Preview_{college_name}')
            test_versions.delete_temporary_directory( f"{college_name}_{df_college['Course'].iloc[0]}_certificates")
            test_versions.delete_temporary_directory("Flask_generated")       
            return response
            
        else:
            flash("The selected College does not match the input data")

        
    return render_template('index.html')

@app.route("/preview", methods=['GET','POST'])
def previewPage():

 
    if request.method == 'POST' or request.method=='GET':
        # Get form data
        cert_code= request.form['query7']
        college_name = request.form['query1']
        location = request.form['query2']
        cert_type=request.form['query3']
        start_date = request.form['startDate']
        end_date = request.form['endDate']
        designation1 = request.form['query4']
        designation2 =request.form['query6']
        designation3 =request.form['query5']

        # Check if the College Logo Image ,Digital Signature Image is provided
        college_logo=file_checker('college_logo')
        digital_signature1 = file_checker('digital_signature1')
        digital_signature2 = file_checker('digital_signature2')
        digital_signature3 = file_checker('digital_signature3')
        background_path=file_checker('Template')

         # Check if the CSV file is provided
        threshold=0
        if 'csv_file' in request.files:
            csv_file = request.files['csv_file']
            if csv_file and allowed_file(csv_file.filename):
                #converting the input file to dataframe
                df=pd.read_csv(csv_file)
                if 'Attendance(1/0)' in df.columns:
                    df=df[df['Attendance(1/0)']>=threshold]   
                df=df.set_index('Sl.No')
                # Keep only the specified columns
                if 'Percentage' in df.columns:
                    df = df[[ 'Name', 'Course', 'College', 'Percentage']] 
                    
                else:
                    df = df[[ 'Name', 'Course', 'College']]


        # Check if the selected college exists in the DataFrame
    if college_name in df['College'].values:
         # Filter the DataFrame for the specified college
        df_college = df[df['College'] == college_name]
        df_college = df_college.reset_index()
        # Create certificate object with all required parameters
        # Generate the certificate and save it to a temporary file
        certificate_data = test_versions.certificate_preview(df_college,background_path, college_logo, cert_type, cert_code, 
                                                            college_name, location, start_date, end_date, 
                                                            digital_signature1, designation1,digital_signature2, designation2,digital_signature3, designation3)

        # Return the certificate data as a response (use 'as_attachment=False' to display it in the browser)
        return send_file(certificate_data, as_attachment=False)
    else:
        # Handle GET request or other cases where the method is not 'POST'
        return render_template('preview.html')
            



