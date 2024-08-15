FROM postgres:13

# Install Python and necessary libraries
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    pip3 install pandas sqlalchemy psycopg2-binary

# Create a directory for the scripts
# RUN mkdir /scripts

# Copy the initialization scripts into container
COPY scripts/init.sql /docker-entrypoint-initdb.d/
COPY scripts/load_data_to_postgres.py /scripts/

# Set the working directory
WORKDIR /scripts

# Run the load script
CMD ["python3", "load_data_to_postgres.py"]
