FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libasound2-dev \
    libx11-6 \
    libxext6 \
    libxrandr2 \
    libxtst6 \
    && rm -rf /var/lib/apt/lists/*

# CMAKE arguments for llama-cpp-python CPU acceleration
ENV CMAKE_ARGS="-DLLAMA_BLAS=ON -DLLAMA_BLAS_VENDOR=OpenBLAS"

COPY pyproject.toml .
RUN --mount=type=cache,target=/root/.cache \
    pip install --extra-index-url https://download.pytorch.org/whl/cpu -e .

COPY ./src ./src

CMD ["screenscribe"]