FROM python:3.9-slim

WORKDIR /app

# Create and activate virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN python -m pip install --upgrade pip


COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Install python-dotenv package
RUN pip install python-dotenv

COPY . .

CMD [ "python", "-c", "from dotenv import load_dotenv; load_dotenv()" ]
CMD [ "python", "app.py" ]

