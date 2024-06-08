import os
import time
from flask import Flask, request, jsonify, send_file
from pyreportjasper import PyReportJasper

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'upload_folder')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/api/v1/create', methods=['POST'])
def create_report():
  input_file = os.path.join('reportTemplateTest.jrxml')
  output_file = os.path.join('pdfTeste')
  
  data = request.form.to_dict()
  
  if 'image' not in request.files:
        return jsonify({"error": "Image not found in the request, revise your data and try again"}), 400
  image_file = request.files['image']
  image_file.save(image_path)
  image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_file.filename)

  report_params = { 
  'title': data['title'],
  'author': data['author'],
  'content': data['content'],
  'image': image_path
  }

  pyreport = PyReportJasper()
  pyreport.config(
      input_file,
      output_file,
      output_formats=["pdf"],
      db_connection={},
      parameters=report_params
  )
  pyreport.process_report()
  
  time.sleep(5)
  
  response = send_file(output_file + '.pdf')
  os.remove(image_path)
  return response, 201

  
if __name__ == "__main__":
  app.run(debug=False)
  
