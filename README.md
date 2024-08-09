# certificate-AWS

Certificate Generator is a Flask web application designed to create professional certificates based on user input. It allows users to specify various details such as the event, college information, certificate type, and design elements, then generates multiple standardized certificates in PDF format.

## Features

- **User-friendly Interface**: The application provides an intuitive interface for users to input certificate details and upload necessary files such as a CSV containing attendee information and images for logos and signatures.

- **Dynamic Certificate Generation**: Certificates are dynamically generated based on user-provided data, allowing for customization of certificate content, design, and layout.

- **Preview Functionality**: Users can preview the certificates before generating them, ensuring accuracy and satisfaction with the final output.

- **CSV Integration**: Supports uploading CSV files containing attendee data, which can be used to populate certificate fields such as name, course, college, and more.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Seminar-Room/Certificate_Generator.git
2. Install dependencies:
    ```bash
    pip install -r requirements.txt
3. Run the application:
    ```bash
    python wsgi.py

The application will be accessible at http://localhost:5000 by default.

Usage
1. The certificate generator is hosted on AWS EC2 instance, it can be accessed throught this URL:
    ```bash
    http://13.201.95.24/

2. Access the application through your web browser.

3. Fill out the certificate details form, including event, college, certificate type, date, and signature.

4. Upload a CSV file containing attendee information or manually input the details.

5. Upload images for the college logo and digital signatures.(png)

6. Preview the certificate to ensure correctness.

7. Generate the certificates, which will be available for download in PDF format in a zipfile.

## Dependencies
1. Flask: Web framework for Python.
2. pandas: Data manipulation and analysis library.
3. ReportLab: Library for generating PDF certificates.
4. Werkzeug: Utilities for WSGI (Web Server Gateway Interface) applications.