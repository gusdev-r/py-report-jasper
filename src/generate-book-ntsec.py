import os
import time
import datetime
from flask import Flask, request, send_file
from pyreportjasper import PyReportJasper
import plotly.graph_objects as go

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'upload_folder')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/api/v1/generate-group', methods=['POST'])
def generate_pdf_report():
  # try:
    input_file = os.path.join('templates', 'Empty_Book.jrxml')
    output_file = os.path.join('group-book')
    resource_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'lib')
    resource_dir1 = os.path.join(os.path.abspath(__file__), 'lib')
    
    print(resource_dir)
    print(resource_dir1)
    
    data = request.form.to_dict()
    # data = request.json
    
    image_file = request.files['logoImage']  
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_file.filename)
    image_file.save(image_path)
    
    creation_date = datetime.datetime.now()
    creation_date_str = creation_date.strftime('%d/%m/%Y')
    print(creation_date_str)

    report_params = { 
      'content': data['content'],
      'author': data['author'],
      'content2': data['content2'],
      'title': data['title'],
      'logoImage': image_path
    }
    pyreport = PyReportJasper()
    pyreport.config(
        input_file,
        output_file,
        output_formats=["pdf"],
        db_connection={},
        parameters=report_params,
        # resource=resource_dir
    )
    pyreport.process_report()
    time.sleep(3)

    remove_files_in_directory(app.config['UPLOAD_FOLDER'])
    return send_file(output_file + '.pdf'), 201
    # return 'test worked', 200
    
  # except Exception as e:
  #   remove_files_in_directory(app.config['UPLOAD_FOLDER'])
  #   error_message = { 
  #     "status": "error",
  #     "message": "Ocorreu um erro na tentativa de criar o relatório, revise seus dados caso haja algum parâmtro informado.", 
  #     "parameter": f"{e}"
  #     }
  #   return error_message, 500



def remove_files_in_directory(directory):
  if not os.path.isdir(directory):
    print('This directory does not exists.')
  
  files = os.listdir(directory)

  for file in files:
    file_found = os.path.join(directory, file)
    try:
      os.remove(file_found)
    except Exception as e:
      print(f'Was not possible to remove the file: {e}')


if __name__ == "__main__":
  app.run(debug=True)


  