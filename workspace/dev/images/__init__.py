from phidata.infra.docker.resource.image import DockerImage

from workspace.settings import (
    airflow_enabled,
    data_platform_dir_path,
    jupyter_enabled,
    superset_enabled,
    use_cache,
)

#
# -*- Dev container images
#

dev_images = []

# -*- Settings
image_tag = "dev"
image_repo = "phidata"  # Set your image repo
image_suffix = "starter-aws-snowflake-ds"  # Set your image name suffix
skip_docker_cache = False  # Skip docker cache when building images
pull_docker_images = False  # Force pull images during FROM
push_docker_images = True  # Push images to repo after building

# -*- Airflow image
dev_airflow_image = DockerImage(
    name=f"{image_repo}/airflow-{image_suffix}",
    tag=image_tag,
    path=str(data_platform_dir_path),
    dockerfile="workspace/dev/images/airflow.Dockerfile",
    print_build_log=True,
    pull=pull_docker_images,
    push_image=push_docker_images,
    skip_docker_cache=skip_docker_cache,
    # use_cache=False will recreate the image every time you run `phi ws up`
    # eg: `CACHE=f phi ws up`
    use_cache=use_cache,
)

if airflow_enabled:
    dev_images.append(dev_airflow_image)

# -*- Jupyter image
dev_jupyter_image = DockerImage(
    name=f"{image_repo}/jupyter-{image_suffix}",
    tag=image_tag,
    path=str(data_platform_dir_path),
    dockerfile="workspace/dev/images/jupyter.Dockerfile",
    print_build_log=True,
    pull=pull_docker_images,
    push_image=push_docker_images,
    skip_docker_cache=skip_docker_cache,
    use_cache=use_cache,
)

if jupyter_enabled:
    dev_images.append(dev_jupyter_image)

# -*- Superset image
dev_superset_image = DockerImage(
    name=f"{image_repo}/superset-{image_suffix}",
    tag=image_tag,
    path=str(data_platform_dir_path),
    dockerfile="workspace/dev/images/superset.Dockerfile",
    print_build_log=True,
    pull=pull_docker_images,
    push_image=push_docker_images,
    skip_docker_cache=skip_docker_cache,
    use_cache=use_cache,
)

# if superset_enabled:
#     dev_images.append(dev_superset_image)
