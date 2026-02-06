# btsdatapy

## License

MIT License - see [LICENSE](./LICENSE) file for details.

## Development

This project uses [uv](https://docs.astral.sh/uv/), [ruff](https://docs.astral.sh/ruff/), [mypy](https://mypy.readthedocs.io/en/stable/), and [pytest](https://docs.pytest.org/en/stable/) for development.

Common development commands have been implemented with make for convenience.

```bash
make install # uv sync && uv run pre-commit install

make build # uv build

make pre-commit # uv run pre-commit run --all-files

make unit-tests # uv run pytest --cov=src/btsdatapy --cov-report=html
```
