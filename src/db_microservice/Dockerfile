# Użyj oficjalnego obrazu PostgreSQL
FROM postgres:latest

# Ustaw użytkownika i hasło dla bazy danych
ENV POSTGRES_USER=user
ENV POSTGRES_PASSWORD=password
ENV POSTGRES_DB=mydatabase

# Skopiuj plik inicjalizacyjny do kontenera (jeśli jest potrzebny)
COPY create.sql /docker-entrypoint-initdb.d/

# Opcjonalnie: Zdefiniuj porty (domyślnie PostgreSQL działa na porcie 5432)
EXPOSE 5432
