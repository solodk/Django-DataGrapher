import matplotlib.pyplot as plt
from io import BytesIO
import base64

from .models import Table

def generate_plot(table_id, x, y, plot_type):
    table = Table.objects.get(id=table_id)
    data = table.content['results']

    x_vals = [float(row[x]) for row in data]
    y_vals = [float(row[y]) for row in data]

    plt.figure()

    if plot_type == 'line':
        plt.plot(x_vals, y_vals)
    elif plot_type == 'bar':
        plt.bar(x_vals, y_vals)
    elif plot_type == 'pie':
        plt.pie(y_vals, labels=x, autopct='%1.1f%%')
    elif plot_type == 'hist':
        plt.hist(x_vals, bins='auto', alpha=0.7, rwidth=0.85)
    elif plot_type == 'scatter':
        plt.scatter(x_vals, y_vals)
    elif plot_type == 'area':
        plt.fill_between(x_vals, y_vals, alpha=0.5)
    elif plot_type == 'bubble':
        plt.scatter(x_vals, y_vals, s=y*10, alpha=0.5)
    elif plot_type == 'box':
        plt.boxplot(y_vals)

    # Save the plot to a BytesIO object
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')
    plt.close()

    # Rewind the BytesIO object to the beginning
    image_stream.seek(0)

    # Encode the image as base64 for embedding in HTML
    encoded_image = base64.b64encode(image_stream.read()).decode('utf-8')

    return f"data:image/png;base64,{encoded_image}"