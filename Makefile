LINT_TARGETS := $(shell find . -name "*.py" \
                    -not -path "*/.venv/*" \
                    -not -path "*/notebooks/*" \
                  )


WITH_PIPENV := pipenv run

download:
	kaggle datasets download -p input/yugioh-cards --unzip ioexception/yugioh-cards
	kaggle datasets download -p input/yugioh-decks --unzip ioexception/yugioh-decks

fmt:
	$(WITH_PIPENV) isort . --apply
	$(WITH_PIPENV) black --target-version py36 $(LINT_TARGETS)

lint:
	$(WITH_PIPENV) isort . --check-only
	$(WITH_PIPENV) black --check $(LINT_TARGETS)