PKG:=teesh

test:
	uv run unittest-ft -vrs $(PKG).tests
	uv run ty check

lint:
	uv run ruff check
	uv run ufmt check $(PKG)

format:
	python -m ufmt format $(PKG)

clean:
	rm -rf .mypy_cache build dist html *.egg-info

distclean: clean
	rm -rf .venv
