FROM python:3.10.6-stretch

RUN mkdir -p /price-pred-api
WORKDIR /price-pred-api

# Upgrade pip with no cache
RUN pip install --no-cache-dir -U pip

# Copy application requirements file to the created working directory
COPY requirements.txt .

# Install application dependencies from the requirements file
RUN pip install -r requirements.txt

# Copy every file in the source folder to the created working directory
COPY  ./app /price-pred-api

EXPOSE 8000

# Run the python application
CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--reload"]