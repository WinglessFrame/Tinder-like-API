# За базу используем официальный image питона
FROM python:3.8

# Отключаем буферизацию логов
ENV PYTHONUNBUFFERED 1

# Обновляем пакетный менеджер
RUN apt-get update -y && apt-get upgrade -y

# Ставим зависимости GDAL, PROJ
RUN apt-get install -y gdal-bin libgdal-dev
RUN apt-get install -y python3-gdal
RUN apt-get install -y binutils libproj-dev


# Копируем все файлы приложения в рабочую директорию в контейнере
COPY . .
WORKDIR .

RUN pip install -r requirements.txt
