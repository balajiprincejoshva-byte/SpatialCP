FROM python:3.10-slim

WORKDIR /app

# Install dependencies for pdfkit if we want to generate pdf later (optional, currently focusing on HTML but good to have)
RUN apt-get update && apt-get install -y wkhtmltopdf && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]
