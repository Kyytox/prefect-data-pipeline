# Prefect
from prefect import task
from prefect.variables import Variable
from prefect.artifacts import create_table_artifact


@task(
    name="update_data_artifact",
    description="Update data artifact",
    task_run_name="update-data-artifact",
)
def upd_data_artifact(info, data):
    """
    Update Artifact

    - Retrieve the artifact from the Prefect Variable
    - Add data to the artifact
        - Save the artifact back to the Prefect Variable

    Args:
        info: information
        data: data to add
    """

    # get varoaible
    data_artifact = Variable.get("data_artifact", default=[])

    # add data
    data_artifact.append({"info": info, "data": data})

    # save variable
    Variable.set("data_artifact", data_artifact, overwrite=True)


@task(
    name="save_artifact",
    description="Save artifact in Prefect",
    task_run_name="save-artifact-{key_name}",
)
def save_artifact(key_name: str):
    """
    Save artifact in Prefect for the Flow

    - Retrieve the artifact from the Prefect Variable
    - save the artifact with the data
    - Reset the Prefect Variable for the next run

    Args:
        key: key of artifact (name of the artifact)
    """

    # get data
    data_artifact = Variable.get("data_artifact", default=[])

    # create data
    create_table_artifact(
        key=key_name,
        table=data_artifact,
    )

    # reset variable
    Variable.set("data_artifact", [], overwrite=True)
