from  postgres:latest
COPY resources/rates_new.sql /docker-entrypoint-initdb.d/
COPY resources/rates.sql /docker-entrypoint-initdb.d/
EXPOSE 5432