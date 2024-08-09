from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import  Paragraph, Frame,KeepInFrame
from reportlab.platypus import Spacer
from reportlab.lib.styles import  ParagraphStyle
from reportlab.pdfgen import canvas
from PIL import Image

import os
import zipfile


from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


def register_fonts():
    font_path1 = r"Standard_inputs/fonts/Poppins-Regular.ttf"
    pdfmetrics.registerFont(TTFont('Poppins-Regular', font_path1))

    font_path2 = r'Standard_inputs/fonts/Poppins-Bold.ttf'
    pdfmetrics.registerFont(TTFont('Poppins-Bold', font_path2))
    
register_fonts()


# Define the page size (letter size in landscape orientation)
page_width=297*mm 
page_height = 210*mm

#landscape_page_size = (page_width, page_height)
def image_resizer(image,w,h):
        #dimensions of the image area to be covered
        output_image_width=w 
        output_image_height=h
        #calculating aspect ratio of original image
        image_read=Image.open(image)
        input_image_width,input_image_height=image_read.size

        aspect_ratio= input_image_width/input_image_height

        if output_image_width /aspect_ratio > output_image_height:
            output_image_width=output_image_height*aspect_ratio
        else:
            output_image_height=output_image_width/aspect_ratio

        return output_image_width,output_image_height
     
# Create a custom canvas for drawing the certificate elements
class MyCanvas:
    def __init__(self, pdf_canvas):
        self.canvas = pdf_canvas
    
    def header(self,background_path):
        # Draw the background image (landscape)
        if background_path==None:
            background_path=r"Standard_inputs/SRblank_template.jpg"   
        self.canvas.drawImage(background_path, 0, 0, width=297*mm, height=210*mm)

    
    def add_certificate_title(self,cert_type):
        # Create a Frame for the text box
        frame_width = 160 * mm  # Adjust the width as needed
        frame_height = 40 * mm  # Adjust the height as needed
        frame_x = (page_width - frame_width) / 2
        frame_y = 142 * mm
        frame = Frame(frame_x, frame_y, frame_width, frame_height, showBoundary=0)  # Set showBoundary=1 for debugging

        #defining fonts and alignment
        bold_style1 = ParagraphStyle(
            "bold_Style1",
            fontSize=56,
            fontName="Poppins-Bold",  # You can change the font family as needed
            textColor=colors.HexColor("#613880"),
            leading=8*mm,
            alignment=1 # set alignment =1 for center alignment
        )
        bold_style2 = ParagraphStyle(
            "bold_Style2",
            fontSize=30,
            fontName="Poppins-Bold",  # You can change the font family as needed
            textColor=colors.HexColor("#a351ad"),
            leading=8*mm,
            alignment=1 # set alignment =1 for center alignment
        )
        #contents of the frame 
        paragraph=[
            Paragraph('CERTIFICATE',bold_style1),
            Spacer(1,40),
            Paragraph(f'Of {cert_type}',bold_style2)
                   ]
        # Create a KeepInFrame to hold the paragraph elements within the frame
        keep_in_frame = KeepInFrame(frame_width, frame_height,paragraph)
        # Build the story within the frame
        frame.addFromList([keep_in_frame], self.canvas)

    def add_srlogo(self):
        sr_logo =  r"Standard_inputs/srlogo.png"
        sr_logo_width,sr_logo_height= image_resizer(sr_logo,100,120)
        sr_logo_x= 245*mm
        sr_logo_y=135*mm
        self.canvas.drawImage(sr_logo, sr_logo_x, sr_logo_y,sr_logo_width, sr_logo_height)
      
    
    def add_cologo(self,cologo): # V
        cologo_width,cologo_height=image_resizer(cologo,100,100)
        #coordinates of the logo
        cologo_x= 25*mm
        cologo_y=140*mm
        self.canvas.drawImage(cologo, cologo_x, cologo_y,cologo_width, cologo_height)



    def add_completion_text(self,name,cert_code): 

        # Create a Frame for the text box
        frame_width = 160 * mm  # Adjust the width as needed
        frame_height = 30 * mm  # Adjust the height as needed
        frame_x = (page_width - frame_width) / 2
        frame_y = 100 * mm
        frame = Frame(frame_x, frame_y, frame_width, frame_height, showBoundary=0)  # Set showBoundary=1 for debugging

        #defining fonts and alignment
        bold_style1 = ParagraphStyle(
            "bold_Style1",
            fontSize=24,
            fontName="Poppins-Bold",  # You can change the font family as needed
            textColor=colors.black,
            leading=8*mm,
            alignment=1 # set alignment =1 for center alignment
        )
        regular_style1 = ParagraphStyle(
            "regular_Style1",
            fontSize=20,
            fontName="Poppins-Regular",  # You can change the font family as needed
            textColor=colors.black,
            leading=8*mm,
            alignment=1 # set alignment =1 for center alignment
        )

        def cert_type(cert_code):
            if cert_code == '1'or'2'or'3.2'or'4':
                h1=f"This certificate is proudly presented to"
                return h1
            if cert_code=='3.1'or'5.1'or'5.2':
                h2=f"This is to certify that"
                return h2
                  
                  
        #contents of the frame 
        paragraph=[
            Paragraph(cert_type(cert_code),regular_style1),
            Spacer(1,10),
            Paragraph(f'{name}',bold_style1)
                   ]
        # Create a KeepInFrame to hold the paragraph elements within the frame
        keep_in_frame = KeepInFrame(frame_width, frame_height,paragraph)
        # Build the story within the frame
        frame.addFromList([keep_in_frame], self.canvas)

        #drawing the line
        x1,y1= 75*mm,106*mm
        x2,y2= (x1 + 412),y1
        line_width=1 #thickness of the line
        line_color=colors.black
        self.canvas.setStrokeColor(line_color)
        self.canvas.setLineWidth(line_width)
        self.canvas.line(x1, y1, x2, y2)

    

    def add_course_details_percent(self, course, college, location,percentage,cert_code, start_date, end_date):
        # Create a Frame for the text box
        frame_width = 255 * mm  # Adjust the width as needed
        frame_height = 50 * mm  # Adjust the height as needed
        frame_x = (page_width -frame_width) /2
        frame_y = 52 * mm
        frame = Frame(frame_x, frame_y, frame_width, frame_height, showBoundary=0)  # Set showBoundary=1 for debugging

        #defining font 
        paragraph_style = ParagraphStyle(
            "CustomStyle",
            fontSize=18,
            fontName="Helvetica",  # You can change the font family as needed
            textColor=colors.black,
            leading=10*mm,  # Set the line spacing here
            alignment= 1 # set alignment =1 for center alignment
        )
        
        def cert_type(cert_code):
            if cert_code=='3.1':
                certificate_course_para1=f"who has successfully completed the <b>{course}</b> with a score of <b>{percentage}%</b> following the assessment conducted by <b>Seminarroom Education Private Limited</b> in association with <b>{college}</b>, {location}, from <b>{start_date} to {end_date}</b>."
                return certificate_course_para1
            
        
        paragraph=[Paragraph(cert_type(cert_code), paragraph_style)]
        
        # Create a KeepInFrame to hold the paragraph elements within the frame
        keep_in_frame = KeepInFrame(frame_width, frame_height,paragraph)
        # Build the story within the frame
        frame.addFromList([keep_in_frame], self.canvas)

    def add_course_details(self, course, college, location,cert_code, start_date, end_date):
            # Create a Frame for the text box
            frame_width = 255 * mm  # Adjust the width as needed
            frame_height = 52 * mm  # Adjust the height as needed
            frame_x = (page_width -frame_width) /2
            frame_y = 50 * mm
            frame = Frame(frame_x, frame_y, frame_width, frame_height, showBoundary=0)  # Set showBoundary=1 for debugging

            #defining font 
            paragraph_style = ParagraphStyle(
                "CustomStyle",
                fontSize=19,
                fontName="Helvetica",  # You can change the font family as needed
                textColor=colors.black,
                leading=10*mm,  # Set the line spacing here
                alignment= 1 # set alignment =1 for center alignment
            )
            
            def cert_type(cert_code):
                if cert_code=='1':
                    iip_para=f" a student of  <b>{college}</b>,{location},<br /> for participating in the <b>Industry Inspiration Program</b> conducted by <b>Seminarroom Education Private Limited</b> from  <b>{start_date} to {end_date}</b>."
                    return iip_para
                if cert_code=='2':
                    deek_para=f"a student of  <b>{college}</b>,{location}, for participating in India's largest online Induction Program '<b>Deeksharambh-2023</b>' conducted by <b>Seminarroom Education Private Limited</b> from  <b>{start_date} to {end_date}</b>."
                    return deek_para
                if cert_code=='3.2':
                    certificate_course_para2=f"for participating in the <b>{course}</b> conducted by <b>Seminarroom Education Private limited</b> in association with <b>{college}</b>, {location}, from <b>{start_date} to {end_date}</b>"
                    return certificate_course_para2
                if cert_code=='4':
                    SDP_para=f"a student of <b>{college}</b>, {location},for participating in the <b>Student Development Program</b> conducted by <b>Seminarroom Education Private Limited</b> on <b>{start_date}</b>."
                    return SDP_para
                if cert_code=='5.1':
                    FDP_para1=f"of <b>{college}</b>, {location}, has participated in the <b>Faculty Development Programme</b> on <b>{course}</b> conducted by <b>{college}</b>, {location}, in association with <b>Seminarroom Education Private Limited</b> on <b>{start_date}</b> "
                    return FDP_para1
                if cert_code=='5.2':
                    FDP_para2=f"of <b>{college}</b>, {location}, has participated in the Faculty Development Programme conducted by <b>{college}</b>, {location}, in association with <b>Seminarroom Education Private Limited</b> on <b>{start_date}</b> "
                    return FDP_para2
            
            
            paragraph=[Paragraph(cert_type(cert_code), paragraph_style)]
            
            # Create a KeepInFrame to hold the paragraph elements within the frame
            keep_in_frame = KeepInFrame(frame_width, frame_height,paragraph)
            # Build the story within the frame
            frame.addFromList([keep_in_frame], self.canvas)
        
    
    
    def add_sign_designation(self,x,sign,designation,college, location):
            # Create a Frame for the text box
            #name
            frame1_width = 60 * mm  # Adjust the width as needed
            frame1_height = 15 * mm  # Adjust the height as needed
            #designation
            frame2_width =80*mm
            frame2_height=25*mm

            '''frame_x is important for postioning of the entire signature set'''
            frame1_x = x #just adjust X coordinate to move the set of image , line and text all together
            frame1_y = 30 * mm
            frame2_x,frame2_y = frame1_x-10*mm,10*mm 
            frame1 = Frame(frame1_x, frame1_y, frame1_width, frame1_height, showBoundary=0)
            frame2 = Frame(frame2_x, frame2_y, frame2_width, frame2_height, showBoundary=0)

            # Create a ParagraphStyle for the text
            text_style = ParagraphStyle(
                "TextStyle",
                fontSize=13,
                fontName="Helvetica",
                textColor=colors.black,
                leading=5*mm,
                alignment=1
            )

            #frame1
            #adding designation into the frame
            paragraph=[Paragraph(f"{designation}",text_style)]
            # Create a KeepInFrame to hold the paragraph elements within the frame
            keep_in_frame = KeepInFrame(frame1_width, frame1_height,paragraph)
            # Build the story within the frame
            frame1.addFromList([keep_in_frame], self.canvas)

            #frame2
            #adding designation into the frame
            paragraph=[Paragraph(f"{college}, {location}",text_style)]
            # Create a KeepInFrame to hold the paragraph elements within the frame
            keep_in_frame = KeepInFrame(frame2_width, frame2_height,paragraph)
            # Build the story within the frame
            frame2.addFromList([keep_in_frame], self.canvas)

            #adding line
            x1,y1= frame1_x+(frame1_width- 105)/2 ,45*mm
            x2,y2= (x1 + 105),y1
            line_width=1 #thickness of the line
            line_color=colors.black
            self.canvas.setStrokeColor(line_color)
            self.canvas.setLineWidth(line_width)
            self.canvas.line(x1, y1, x2, y2)

            if sign!=None:
                #adding background subtracted digital signature
                DS_photo_width,DS_photo_height = image_resizer(sign,30*mm,10*mm)
                #coordinates of the logo
                DS_photo_x = frame1_x+(frame1_width - DS_photo_width) /2
                DS_photo_y= 46*mm
                self.canvas.drawImage(sign, DS_photo_x, DS_photo_y, DS_photo_width, DS_photo_height)


    def add_college_digital_signatures(self, digital_sign3, designation3,digital_sign1, designation1,
                               college, location):
            #adding designation,college,location into the frame
            if designation3!="":
                self.add_sign_designation(30*mm,digital_sign1,designation1, college, location)
                self.add_sign_designation(120*mm,digital_sign3,designation3, college, location)
            
            else:
                self.add_sign_designation(42*mm,digital_sign1,designation1, college, location)

    def add_SR_digital_signature(self, digital_sign2,designation2,designation3):
            frame1_width = 60 * mm  # Adjust the width as needed
            frame1_height = 15 * mm  # Adjust the height as needed
            #designation
            frame2_width =80*mm
            frame2_height=25*mm

            if designation3!="":
                x=210*mm
            else:
                x=190*mm           

            '''frame_x is important for postioning of the entire signature set'''
            frame1_x = x #just adjust X coordinate to move the set of image , line and text all together
            frame1_y = 30 * mm
            frame2_x,frame2_y = frame1_x-10*mm,10*mm 
            frame1 = Frame(frame1_x, frame1_y, frame1_width, frame1_height, showBoundary=0)
            frame2 = Frame(frame2_x, frame2_y, frame2_width, frame2_height, showBoundary=0)

            # Create a ParagraphStyle for the text
            text_style = ParagraphStyle(
                "TextStyle",
                fontSize=13,
                fontName="Helvetica",
                textColor=colors.black,
                leading=5*mm,
                alignment=1
            )
            
            #frame1
            #adding designation into the frame
            paragraph=[Paragraph(f"{designation2}",text_style)]
            # Create a KeepInFrame to hold the paragraph elements within the frame
            keep_in_frame = KeepInFrame(frame1_width, frame1_height,paragraph)
            # Build the story within the frame
            frame1.addFromList([keep_in_frame], self.canvas)

            inst="Seminarroom Pvt Ltd,<br/>Bengaluru"
            #frame2
            #adding designation into the frame
            paragraph=[Paragraph(f"{inst}",text_style)]
            # Create a KeepInFrame to hold the paragraph elements within the frame
            keep_in_frame = KeepInFrame(frame2_width, frame2_height,paragraph)
            # Build the story within the frame
            frame2.addFromList([keep_in_frame], self.canvas)

            #adding line
            x1,y1= frame1_x+(frame1_width- 105)/2 ,45*mm
            x2,y2= (x1 + 105),y1
            line_width=1 #thickness of the line
            line_color=colors.black
            self.canvas.setStrokeColor(line_color)
            self.canvas.setLineWidth(line_width)
            self.canvas.line(x1, y1, x2, y2)

            #adding background subtracted digital signature
            DS_photo_width,DS_photo_height = image_resizer(digital_sign2,30*mm,10*mm)
            #coordinates of the logo
            DS_photo_x = frame1_x+(frame1_width - DS_photo_width) /2
            DS_photo_y= 46*mm
            self.canvas.drawImage(digital_sign2, DS_photo_x, DS_photo_y, DS_photo_width, DS_photo_height)


#certificate generator
def certificate_generator(df_college,background_path,cologo,certificate_type,cert_code,
                          college_name,location,start_date,end_date,
                          digital_sign1,designation1,digital_sign2,designation2,digital_sign3,designation3):
   
    # Create a temporary folder to store generated certificates
    temp_folder = f"{college_name}_{df_college['Course'].iloc[0]}_certificates"
    os.makedirs(temp_folder, exist_ok=True)

    for index, row in df_college.iterrows():
        # Create a new PDF instance for each student using MyCertificate class
        pdf_canvas = canvas.Canvas(os.path.join(temp_folder, f"{row['Sl.No']}_{row['Name']}_{row['Course']}_{row['College']}_Certificate.pdf"), pagesize=landscape(A4))
        pdf = MyCanvas(pdf_canvas)

        pdf.header(background_path)
            
            #type of certificates:completion,participation,awar,merit
        pdf.add_certificate_title(certificate_type)

            #adding college logo
        pdf.add_cologo(cologo)

            #adding seminar room logo
        pdf.add_srlogo()
            
            #adding student name
        pdf.add_completion_text(row['Name'],cert_code)
            
            #adding content course, college, location,percentage,cert_code, start_date, end_date
        if cert_code=="3.1" and 'Percentage' in df_college.columns:
            pdf.add_course_details_percent(row['Course'], row['College'],location,row['Percentage'],cert_code,start_date,end_date)
        else:
            pdf.add_course_details(row['Course'], row['College'],location,cert_code,start_date,end_date)
    
         #adding digital sign and  designation of college stakeholder
        pdf.add_college_digital_signatures( digital_sign3, designation3,digital_sign1, designation1,row['College'], location)

        #adding digital sign and designation of seminarroom rep/SME
        pdf.add_SR_digital_signature(digital_sign2,designation2,designation3)

        pdf_canvas.save()

 # Create a ZIP file containing all certificates
    gen=f'Flask_generated'
    zip_filename = os.path.abspath(os.path.join(gen, f'{temp_folder}.zip'))
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for root, _, files in os.walk(temp_folder):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, temp_folder))

    return zip_filename


#certificate generator
def certificate_preview(df_college,background_path,cologo,certificate_type,cert_code,
                        college_name,location,start_date,end_date,
                        digital_sign1,designation1,digital_sign2,designation2,digital_sign3,designation3):
        
        # Create a temporary folder to store generated certificates
        temp_folder = f'Preview_{college_name}'
        os.makedirs(temp_folder, exist_ok=True)

        pdf_file_path = os.path.abspath(os.path.join(temp_folder, f"Preview_{df_college['Sl.No'].iloc[0]}_{df_college['Name'].iloc[0]}_{df_college['College'].iloc[0]}_Certificate.pdf"))

        # Create a new PDF instance for each student using MyCertificate class
        pdf_canvas = canvas.Canvas(pdf_file_path, pagesize=landscape(A4))
        pdf = MyCanvas(pdf_canvas)

        pdf.header(background_path)
            
            #type of certificates:completion,participation,awar,merit
        pdf.add_certificate_title(certificate_type)

            #adding college logo
        pdf.add_cologo(cologo)

            #adding seminar room logo
        pdf.add_srlogo()
            
            #adding student name
        pdf.add_completion_text(df_college['Name'].iloc[0],cert_code)
            
            #adding content course, college, location,percentage,cert_code, start_date, end_date
        if cert_code=="3.1" and 'Percentage' in df_college.columns:
            pdf.add_course_details_percent(df_college['Course'].iloc[0], df_college['College'].iloc[0],location,df_college['Percentage'].iloc[0],cert_code,start_date,end_date)
        else:
            pdf.add_course_details(df_college['Course'].iloc[0], df_college['College'].iloc[0],location,cert_code,start_date,end_date)
    
        #adding digital sign and  designation of college stakeholders
        pdf.add_college_digital_signatures( digital_sign3, designation3,digital_sign1, designation1,df_college['College'].iloc[0], location)

        #adding digital sign and designation of seminarroom rep/SME
        pdf.add_SR_digital_signature(digital_sign2,designation2,designation3)

        pdf_canvas.save()

        return pdf_file_path

# Delete the temporary directory when you're done with the certificates
def delete_temporary_directory(temp_dir):
    import shutil
    shutil.rmtree(temp_dir, ignore_errors=True)
