FROM python:3.10-bookworm
# Install poetry for dependecy management.
RUN pip install poetry
# Copy current directory as "/app"
COPY . /app
# Set poetry env variables, to create the venv inside the /app dir.
ENV PATH="/root/.local/bin:$PATH" \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1
# Install dependencies and the scoreboard module.
RUN cd /app && poetry install
# Activate the virtual environment.
ENV PATH=/app/.venv/bin:$PATH
# Run the example script.
WORKDIR /app
CMD python scripts/requirements_example.py