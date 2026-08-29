.PHONY: doctor test lint serve build

doctor:
	python -m sciforge doctor

test:
	python -m pytest -q

serve:
	python -m sciforge serve --host 0.0.0.0 --port 8000

build:
	python -m build

clean:
	rm -rf build dist *.egg-info
