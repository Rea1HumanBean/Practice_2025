OPENAPI_GENERATOR_IMAGE := openapitools/openapi-generator-cli:v6.6.0
CLIENT_DIR := ./client
OPENAPI_SPEC := openapi.yaml
PACKAGE_NAME := schedule_client

.PHONY: generate-client install-client clean test help

generate-client:
	@echo "Generating Python client from OpenAPI spec..."
	docker run --rm \
		-v ${PWD}:/local \
		${OPENAPI_GENERATOR_IMAGE} generate \
		-i /local/${OPENAPI_SPEC} \
		-g python \
		-o /local/${CLIENT_DIR} \
		--package-name ${PACKAGE_NAME} \
		--skip-validate-spec \
		--additional-properties=generateSourceCodeOnly=true,packageVersion=1.0.0
	@echo "Client generated in ${CLIENT_DIR}"

install-client: generate-client
	@echo "Installing client package..."
	cd ${CLIENT_DIR} && pip install -e .
	@echo "Client installed in editable mode"

clean:
	@echo "Cleaning generated client..."
	rm -rf ${CLIENT_DIR}
	@echo "Clean complete"

include test/makefile

test: test-all
