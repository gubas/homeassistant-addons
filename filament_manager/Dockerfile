ARG BUILD_FROM
FROM $BUILD_FROM

# Install dependencies en une seule couche
RUN apk add --no-cache python3 py3-pip && \
    rm -rf /var/cache/apk/*

WORKDIR /app

# Copy et install en une seule couche pour réduire la taille
COPY requirements.txt .
RUN pip3 install --break-system-packages --no-cache-dir -r requirements.txt && \
    rm -rf ~/.cache/pip

# Copy application
COPY app/ /app/
COPY run.sh /
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]
