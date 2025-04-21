.PHONY: generate-client

generate-client:
    openapi-generator-cli generate \
    -i openapi.yaml \
    -g python \
    -o ./client \
    --package-name schedule_client \
    --skip-validate-spec \
    --additional-properties=generateSourceCodeOnly=true,packageVersion=1.0.0

install-client:
    cd client && pip install -e .

clean:
    rm -rf ./client