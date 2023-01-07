from phidata.app.group import AppGroup
from phidata.app.jupyter import ImagePullPolicy, JupyterLab
from phidata.infra.aws.resource.group import AwsResourceGroup, EbsVolume

from workspace.prd.aws_resources import (
    topology_spread_key,
    topology_spread_max_skew,
    topology_spread_when_unsatisfiable,
    workers_ng_label,
)
from workspace.prd.images import prd_jupyter_image
from workspace.settings import (
    aws_az_1a,
    jupyter_enabled,
    prd_key,
    prd_tags,
    use_cache,
    ws_dir_path,
)

# -*- Settings
user_name: str = "user1"
# Prevents deletion of aws resources when running `phi ws down`
aws_skip_delete: bool = False

#
# -*- AWS resources
#
# -*- EbsVolumes
# EbsVolume for jupyter
prd_jupyter_ebs_volume = EbsVolume(
    name=f"jupyter-{user_name}-{prd_key}",
    size=16,
    availability_zone=aws_az_1a,
    tags=prd_tags,
    skip_delete=aws_skip_delete,
)

prd_jupyter_aws_resources = AwsResourceGroup(
    name=f"jupyterlab-{user_name}",
    enabled=jupyter_enabled,
    volumes=[prd_jupyter_ebs_volume],
)

#
# -*- Kubernetes resources
#
# JupyterLab
prd_jupyter = JupyterLab(
    name=f"jupyterlab-{user_name}",
    image_name=prd_jupyter_image.name,
    image_tag=prd_jupyter_image.tag,
    mount_ebs_volume=True,
    ebs_volume=prd_jupyter_ebs_volume,
    # mounted when creating the image
    jupyter_config_file="/usr/local/jupyter/jupyter_lab_config.py",
    # Read env variables from env/prd_jupyter_env.yml
    env_file=ws_dir_path.joinpath("env/prd_jupyter_env.yml"),
    # Read secrets from secrets/prd_jupyter_secrets.yml
    secrets_file=ws_dir_path.joinpath("secrets/prd_jupyter_secrets.yml"),
    image_pull_policy=ImagePullPolicy.ALWAYS,
    use_cache=use_cache,
    pod_node_selector=workers_ng_label,
    topology_spread_key=topology_spread_key,
    topology_spread_max_skew=topology_spread_max_skew,
    topology_spread_when_unsatisfiable=topology_spread_when_unsatisfiable,
)

prd_jupyter_apps = AppGroup(
    name=f"jupyterlab-{user_name}",
    enabled=jupyter_enabled,
    apps=[prd_jupyter],
)
