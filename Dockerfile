
# FROM mambaorg/micromamba:1-focal-cuda-11.7.1
FROM --platform=linux/arm64 mambaorg/micromamba
WORKDIR /app
COPY . .

RUN micromamba env create --file conda_environment.yml

# RUN micromamba activate housing
ARG MAMBA_DOCKERFILE_ACTIVATE=1

EXPOSE 5050
# The code to run when container is started:
ENTRYPOINT ["micromamba", "run", "-n", "housing", "gunicorn", "model_app:app", "--bind", "0.0.0.0:5050 "]







