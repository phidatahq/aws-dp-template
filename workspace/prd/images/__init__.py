from phidata.infra.docker.resource.image import DockerImage

from workspace.settings import ws_settings

#
# -*- Production container images
#

prd_images = []
# Production image tag
image_tag = "prd"

# -*- Airflow image
prd_airflow_image = DockerImage(
    name=f"{ws_settings.image_repo}/airflow-{ws_settings.image_suffix}",
    tag=image_tag,
    path=str(ws_settings.ws_dir_path.parent),
    dockerfile="workspace/prd/images/airflow.Dockerfile",
    pull=ws_settings.pull_docker_images,
    push_image=ws_settings.push_docker_images,
    skip_docker_cache=ws_settings.skip_docker_cache,
    use_cache=ws_settings.use_cache,
)

if ws_settings.prd_airflow_enabled and ws_settings.build_images:
    prd_images.append(prd_airflow_image)

# -*- Jupyter image
prd_jupyter_image = DockerImage(
    name=f"{ws_settings.image_repo}/jupyter-{ws_settings.image_suffix}",
    tag=image_tag,
    path=str(ws_settings.ws_dir_path.parent),
    dockerfile="workspace/prd/images/jupyter.Dockerfile",
    pull=ws_settings.pull_docker_images,
    push_image=ws_settings.push_docker_images,
    skip_docker_cache=ws_settings.skip_docker_cache,
    use_cache=ws_settings.use_cache,
)

if ws_settings.prd_jupyter_enabled and ws_settings.build_images:
    prd_images.append(prd_jupyter_image)

# -*- Superset image
prd_superset_image = DockerImage(
    name=f"{ws_settings.image_repo}/superset-{ws_settings.image_suffix}",
    tag=image_tag,
    path=str(ws_settings.ws_dir_path.parent),
    dockerfile="workspace/prd/images/superset.Dockerfile",
    pull=ws_settings.pull_docker_images,
    push_image=ws_settings.push_docker_images,
    skip_docker_cache=ws_settings.skip_docker_cache,
    use_cache=ws_settings.use_cache,
)

if ws_settings.prd_superset_enabled and ws_settings.build_images:
    prd_images.append(prd_superset_image)
