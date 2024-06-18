from flask import Flask, request, send_file
import io
import plotly.graph_objs as go

app = Flask(__name__)


@app.route('/api/v1/generate-chart', methods=['POST'])
def generate_image_chart():
    
    data = request.json
    x_values = data['x_values']
    y_values = data['y_values']
    
    line_chart = go.Figure(data=go.Scatter(x=x_values, y=y_values, mode='lines'))
    
    line_chart.update_layout(title='Avaliação de vendas')
    
    img_bytes = line_chart.to_image(format="png")

    return send_file(io.BytesIO(img_bytes),
                      mimetype='image/png',
                    ), 201


if __name__ == "__main__":
  app.run(debug=True)