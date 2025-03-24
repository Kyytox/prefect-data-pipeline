# Templates for Data Pipelines

Templates for data pipelines projects using, with some open-sources tools

Inspiration from project: **[local-data-stack](https://github.com/l-mds/local-data-stack/tree/main)**

## Prerequisites

- [Python](https://www.python.org/downloads/) >= 3.9

- [pixi](https://pixi.sh/dev/)

```bash
curl -fsSL https://pixi.sh/install.sh | bash
```

- [cookiecutter](https://github.com/cookiecutter/cookiecutter)

```bash
# pipx is strongly recommended.
pip install pipx
pipx install cookiecutter

# If pipx is not an option,
# you can install cookiecutter in your Python user directory.
python -m pip install --user cookiecutter
```

## Usage

Get the templates:

```bash
git clone https://github.com/Kyytox/archi-data-pipeline.git
```

Create a new project using script:

```bash
python archi-data-pipeline/init_project.py
```

Go to the project directory:

```bash
cd <project_name>
```

Install the dependencies:

```bash
pixi install
```

Activate the virtual environment:

```bash
pixi shell
```

Launch Prefect:

```bash
prefect server start
```

Launch Pipeline:

```bash
python main.py
```
