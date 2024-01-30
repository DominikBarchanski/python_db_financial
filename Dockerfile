# Używamy obrazu Nginx jako punktu wyjścia
FROM nginx

# Kopiujemy nasz plik konfiguracyjny do katalogu /etc/nginx/conf.d/
COPY nginx /etc/nginx/conf.d/default.conf
