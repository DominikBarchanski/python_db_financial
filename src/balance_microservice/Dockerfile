
FROM python:3.10

# Ustaw katalog roboczy w kontenerze
WORKDIR /app

# Skopiuj plik zależności Pythona (np. requirements.txt) i pliki źródłowe
COPY requirements.txt .

# Zainstaluj zależności Pythona
RUN pip install -r requirements.txt
# Skopiuj pozostałe pliki źródłowe do katalogu roboczego
COPY . .
ENV PYTHONPATH=/app/src/user_micro:/app/src/user_microservice
# Expose port, na którym będzie działać serwis
EXPOSE 8000

# Uruchom aplikację FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
