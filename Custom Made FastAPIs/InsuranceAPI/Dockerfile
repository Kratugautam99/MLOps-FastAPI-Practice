FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
EXPOSE 8501

RUN echo '#!/bin/bash\n\
echo "Starting services..."\n\
# Start FastAPI (remove --reload in production)\n\
uvicorn InsuranceAPI_V2:app --host 0.0.0.0 --port 8000 &\n\
# Start Streamlit\n\
streamlit run InsuranceUI_V2.py --server.port 8501 --server.address 0.0.0.0 &\n\
# Wait for processes\n\
wait -n\n\
exit $?' > /app/start_services.sh

RUN chmod +x /app/start_services.sh

CMD ["/app/start_services.sh"]