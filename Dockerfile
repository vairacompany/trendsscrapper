# Imagem base com Python
FROM python:3.8-slim

# Instalar dependências do sistema necessárias para o Chrome e o ChromeDriver
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget unzip gnupg xvfb libxi6 libgconf-2-4 libnss3 fonts-liberation \
    libappindicator3-1 libxss1 libasound2 libatk-bridge2.0-0 libgbm-dev \
    libu2f-udev libvulkan1 && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Baixar e instalar o Chrome for Testing
RUN wget -q "https://storage.googleapis.com/chrome-for-testing-public/131.0.6778.85/linux64/chrome-linux64.zip" && \
    unzip chrome-linux64.zip && \
    mv chrome-linux64 /usr/local/google-chrome && \
    ln -s /usr/local/google-chrome/chrome /usr/bin/google-chrome && \
    chmod +x /usr/bin/google-chrome && \
    rm chrome-linux64.zip

# Baixar e instalar o ChromeDriver correspondente
RUN wget -q "https://storage.googleapis.com/chrome-for-testing-public/131.0.6778.85/linux64/chromedriver-linux64.zip" && \
    unzip chromedriver-linux64.zip && \
    mv chromedriver-linux64/chromedriver /usr/local/bin/ && \
    chmod +x /usr/local/bin/chromedriver && \
    rm -rf chromedriver-linux64.zip chromedriver-linux64

# Criar um diretório temporário para evitar problemas de memória compartilhada
RUN mkdir -p /tmp/.X11-unix && chmod 1777 /tmp/.X11-unix

# Configurar diretório de trabalho
WORKDIR /app

# Copiar o arquivo requirements.txt
COPY requirements.txt /app/requirements.txt

# Instalar as dependências do Python
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copiar o código-fonte
COPY src/ /app/src/

# Configurar porta como variável de ambiente
ENV PORT=5000

# Expor a porta usada pelo Flask
EXPOSE 5000

# Comando para rodar o servidor Flask
CMD ["python3", "src/main.py"]
