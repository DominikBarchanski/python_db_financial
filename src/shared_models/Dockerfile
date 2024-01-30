# Użyj oficjalnego obrazu Python
FROM python:3.10

# Ustal katalog roboczy
WORKDIR /app

# Skopiuj plik zależności (requirements.txt) do kontenera
COPY requirements.txt .

# Zainstaluj zależności
RUN pip install -r requirements.txt

# Skopiuj kod źródłowy do kontenera
COPY . .

CMD ["python", "main.py"]
# Uruchom serwis
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
