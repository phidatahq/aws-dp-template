from phidata.infra.docker.config import DockerConfig

from workspace.prd.images import prd_images
from workspace.settings import prd_env, ws_name

#
# -*- Define production Docker resources using the DockerConfig
#
prd_docker_config = DockerConfig(
    env=prd_env,
    network=ws_name,
    # uncomment the following line to build local images
    images=prd_images,
)
