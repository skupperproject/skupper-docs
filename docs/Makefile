BUILD_DIR := build

CCUTIL_ENABLED := \
	$(shell which ccutil 1> /dev/null 2>&1 && echo yes || echo no)

BOOK_SOURCES := $(shell find . -maxdepth 2 -type f -name index.adoc)
# BOOK_SOURCES := $(filter-out ./docs/other/index.adoc,${BOOK_SOURCES})
BOOK_TARGETS := \
	${BOOK_SOURCES:%/index.adoc=${BUILD_DIR}/%/index.html} \
	${BOOK_SOURCES:%/index.adoc=${BUILD_DIR}/%/images}

IMAGE_SOURCES := $(shell find images -type f)
IMAGE_TARGETS := \
	${IMAGE_SOURCES:images/%=${BUILD_DIR}/images/%}

ifeq (${CCUTIL_ENABLED},yes)
CCUTIL_TARGETS := \
	${BOOK_SOURCES:%/index.adoc=${BUILD_DIR}/ccutil/%/index.html}
else
CCUTIL_TARGETS :=
endif


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
	@echo "file:${PWD}/${BUILD_DIR}/welcome/index.html"


.PHONY: clean
clean: ${BOOK_SOURCES:%/index.adoc=clean-%}
	rm -rf ${BUILD_DIR}


define BOOK_TEMPLATE =
$${BUILD_DIR}/${1}/index.html: $$(shell find -L ${1} -type f -name \*.adoc) partials/attributes.adoc
	@mkdir -p $${@D}
	asciidoctor ${1}/index.adoc -o $$@ --safe-mode safe --verbose ${BUILD_ATTRIBUTES}

$${BUILD_DIR}/${1}/images:
	@mkdir -p $${@D}
	@ln -s ../images $$@

$${BUILD_DIR}/ccutil/${1}/index.html:
	@mkdir -p $${BUILD_DIR}/ccutil
	cd ${1} && ccutil compile --lang en_US --main-file index.adoc
	mv ${1}/build/tmp/en-US/html-single $${@D}
	rm -rf ${1}/build

.PHONY: clean-${1}
clean-${1}:
	rm -rf ${1}/build ${1}/html
endef

$(foreach dir,${BOOK_SOURCES:%/index.adoc=%},$(eval $(call BOOK_TEMPLATE,${dir})))

${BUILD_DIR}/internal/%.html: internal/%.adoc common/attributes.adoc
	@mkdir -p ${@D}
	asciidoctor $< -o $@ --safe-mode safe --verbose

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

.PHONY: refresh-upstream-%
refresh-upstream-%: BRANCH := main
refresh-upstream-%:
	rm -rf upstreams/$* upstreams/$*.revision
	scripts/git-export "https://gitbox.apache.org/repos/asf/$*.git" ${BRANCH} upstreams/$*


.PHONY: refresh-github-upstream-%
refresh-github-upstream-%: BRANCH := main
refresh-github-upstream-%:
	rm -rf upstreams/$* upstreams/$*.revision
	scripts/git-export "git@github.com:skupperproject/$*.git" ${BRANCH} upstreams/$*
