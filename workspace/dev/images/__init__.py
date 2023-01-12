from phidata.docker.resource.image import DockerImage

from workspace.settings import ws_settings

#
# -*- Dev container images
#

dev_images = []
# Development image tag
image_tag = "dev"

# -*- Airflow image
dev_airflow_image = DockerImage(
    name=f"{ws_settings.image_repo}/airflow-{ws_settings.image_suffix}",
    tag=image_tag,
    path=str(ws_settings.ws_dir.parent),
    dockerfile="workspace/dev/images/airflow.Dockerfile",
    pull=ws_settings.pull_docker_images,
    push_image=ws_settings.push_docker_images,
    skip_docker_cache=ws_settings.skip_docker_cache,
    use_cache=ws_settings.use_cache,
)

if ws_settings.dev_airflow_enabled and ws_settings.build_images:
    dev_images.append(dev_airflow_image)

# -*- Jupyter image
dev_jupyter_image = DockerImage(
    name=f"{ws_settings.image_repo}/jupyter-{ws_settings.image_suffix}",
    tag=image_tag,
    path=str(ws_settings.ws_dir.parent),
    dockerfile="workspace/dev/images/jupyter.Dockerfile",
    pull=ws_settings.pull_docker_images,
    push_image=ws_settings.push_docker_images,
    skip_docker_cache=ws_settings.skip_docker_cache,
    use_cache=ws_settings.use_cache,
)

if ws_settings.dev_jupyter_enabled and ws_settings.build_images:
    dev_images.append(dev_jupyter_image)

# -*- Superset image
dev_superset_image = DockerImage(
    name=f"{ws_settings.image_repo}/superset-{ws_settings.image_suffix}",
    tag=image_tag,
    path=str(ws_settings.ws_dir.parent),
    dockerfile="workspace/dev/images/superset.Dockerfile",
    pull=ws_settings.pull_docker_images,
    push_image=ws_settings.push_docker_images,
    skip_docker_cache=ws_settings.skip_docker_cache,
    use_cache=ws_settings.use_cache,
)

if ws_settings.dev_superset_enabled and ws_settings.build_images:
    dev_images.append(dev_superset_image)
