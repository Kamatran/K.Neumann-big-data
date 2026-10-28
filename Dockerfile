FROM python:3.11-slim
# Versions pinned deliberately: the memory peaks the experiment is calibrated
# against depend on how pyarrow converts Arrow tables to pandas. Do not bump
# these mid-semester without re-running MEASUREMENTS.md.
RUN pip install --no-cache-dir pandas==3.0.5 pyarrow==25.0.1
WORKDIR /src
