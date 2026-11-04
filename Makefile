.PHONY: test verify inventory preflight

test:
	python -m unittest discover -s tests -v

verify: test
	python -m verification.state_space
	python -m ops.preflight --check-inventory

inventory:
	python -m ops.preflight --check-inventory

# Exit 2 means integration is blocked. This target never starts services.
preflight:
	python -m ops.preflight
