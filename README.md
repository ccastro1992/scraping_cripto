# 🪙 CryptoScraper Web App

Este proyecto es una aplicación web desarrollada con **Flask** que realiza **scraping continuo** del sitio [Investing.com - Criptomonedas](https://es.investing.com/crypto/currencies). Implementa un proceso **ETL** (Extracción, Transformación y Carga) para recopilar los precios en tiempo real de distintas criptomonedas, almacenarlos en una base de datos **SQLite**, y mostrarlos en una interfaz web amigable.

## 🚀 Características

- Scraping periódico de precios de criptomonedas desde Investing.com
- Proceso ETL automatizado:
  - **Extracción:** scraping con requests y BeautifulSoup
  - **Transformación:** limpieza y normalización de los datos
  - **Carga:** almacenamiento en base de datos SQLite
- Aplicación web con Flask:
  - Visualización en tiempo real de precios de criptomonedas
  - Interfaz simple y responsiva
- Base de datos local persistente
- Preparado para ejecución como servicio o en background

## 🛠️ Tecnologías Utilizadas

- Python 3.x
- Flask
- BeautifulSoup4
- Requests
- SQLite
- APScheduler (o similar) para tareas programadas
