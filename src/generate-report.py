import io
import os
import time
from datetime import date
import plotly.graph_objs as go
from flask import Flask, request, jsonify, send_file
from pyreportjasper import PyReportJasper

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'upload_folder')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


#TODO : put a try catch and remove the images if it goes wrong
@app.route('/api/v1/generate-report', methods=['POST'])
def generate_pdf_report():
  input_file = os.path.join('templates', 'reportTemplateTest.jrxml')
  output_file = os.path.join('ntsecReport')
  
  image_file = request.files['image']  
  chart_image_file = request.files['chart_image']
  
  image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_file.filename)
  chart_image_path = os.path.join(app.config['UPLOAD_FOLDER'], chart_image_file.filename)

  image_file.save(image_path)
  chart_image_file.save(chart_image_path)

  data = request.form.to_dict()
  report_params = { 
  'image': image_path,
  'title': data['title'],
  'author': data['author'],
  'content': data['content'],
  'chartimage': chart_image_path,
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
  os.remove(chart_image_path)

  return response, 201

  
if __name__ == "__main__":
  app.run(debug=True)
  
def create_chart(request):
  
  data = request.json
  x_values = data['x_values']
  y_values = data['y_values']
  line_chart = go.Figure(data=go.Scatter(x=x_values, y=y_values, mode='lines'))
  
  line_chart.update_layout(title='Avaliação de vendas')
  
  img_bytes = line_chart.to_image(format="png")
  
  return send_file(io.BytesIO(img_bytes),
                      mimetype='image/png',
                    ), 201
