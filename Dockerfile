FROM python:3.12-alpine

RUN apk add --no-cache \
    texlive \
    texlive-xetex \
    texmf-dist-latexextra \
    msttcorefonts-installer \
    fontconfig \
    && update-ms-fonts \
    && fc-cache -f

WORKDIR /app

RUN pip install poetry
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

COPY . .

RUN mkdir -p output

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]