BUILD_DIR := build

# Find all .adoc files instead of just index.adoc
BOOK_SOURCES := $(shell find . -maxdepth 2 -type f -name '*.adoc')
BOOK_TARGETS := \
	$(patsubst %.adoc,${BUILD_DIR}/%.html,$(BOOK_SOURCES)) \
	${BOOK_SOURCES:%.adoc=${BUILD_DIR}/%/images}

IMAGE_SOURCES := $(shell find images -type f)
IMAGE_TARGETS := \
	${IMAGE_SOURCES:images/%=${BUILD_DIR}/images/%}

BUILD_ATTRIBUTES := $(shell sed 's/^/-a /' .build-attributes)

.PHONY: default
default: build

.PHONY: help
help:
	@echo "[default]           Equivalent to 'make build'"
	@echo "build               Generate asciidoctor output (faster)"
	@echo "clean               Removes ${BUILD_DIR}/ and other build artifacts"

.PHONY: build
build: ${BOOK_TARGETS} ${IMAGE_TARGETS} ${EXTRA_TARGETS}
	@echo "See the output in your browser at:"
	@echo "file:${PWD}/${BUILD_DIR}/index.html"

.PHONY: clean
clean:
	rm -rf ${BUILD_DIR}

# Modified rule to handle all .adoc files
${BUILD_DIR}/%.html: %.adoc
	@mkdir -p ${@D}
	asciidoctor $< -o $@ --safe-mode safe --verbose ${BUILD_ATTRIBUTES}

${BUILD_DIR}/%/images:
	@mkdir -p ${@D}
	@ln -s ../../images $@

${BUILD_DIR}/images/%.png: images/%.png
	@mkdir -p ${@D}
	@cp $< $@

${BUILD_DIR}/images/%.svg: images/%.svg
	@mkdir -p ${@D}
	@cp $< $@

${BUILD_DIR}/docs:
	@ln -s . $@

.PHONY: ${BUILD_DIR}/index.html
${BUILD_DIR}/index.html: scripts/redirect-to-welcome.html
	cp $< $@
