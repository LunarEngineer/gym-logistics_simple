FROM cs7642
RUN pip install python-igraph
COPY . /gym-logistics-simple
WORKDIR /gym-logistics-simple
RUN useradd -d /gym-logistics-simple cs7642 \
    && chown 1000:1000 /gym-logistics-simple -R \
    && chmod -R 777 /gym-logistics-simple

USER cs7642
ENTRYPOINT ["/bin/bash"]