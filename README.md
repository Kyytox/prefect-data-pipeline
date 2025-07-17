# Prefect Templates for Data Pipelines

Templates for data pipelines projects using some open-sources tools

</br>

![](/assets/prefect_data_pipeline_img_archi.png "Titre de l'image")


## Prerequisites

- [Python](https://www.python.org/downloads/) >= 3.9

- [pixi](https://pixi.sh/dev/)

```bash
curl -fsSL https://pixi.sh/install.sh | bash
```

</br>

- [cookiecutter](https://github.com/cookiecutter/cookiecutter)

```bash
# pipx is strongly recommended.
pip install pipx
pipx install cookiecutter

# If pipx is not an option,
# you can install cookiecutter in your Python user directory.
python -m pip install --user cookiecutter
```

</br>
</br>

## Usage

Get the templates:

```bash
git clone https://github.com/Kyytox/archi-data-pipeline.git
```

Create a new project using script:

```bash
python prefect-data-pipeline/init_project.py 
```

Go to the project directory:

```bash
cd <project_name>
```


Setup the project:

```bash
bash setup/setup.sh
```

Launch Prefect:

```bash
prefect server start
```

Launch Pipeline:

```bash
# In a new terminal
cd <project_name> && pixi shell
sh prefect/deploy.sh
```

> [!WARNING]  
> The Pipeline running every minute.

> [!NOTE]
> For **Template_2** : You can see the final result in data/processed/rockets_launches_stats.parquet file.
> 
> For **Template_3** : You can see the final result in Postgres database in mart_rocket_launches_by_country table.