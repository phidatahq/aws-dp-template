from pathlib import Path
from typing import List, Optional

from phidata.utils.env_var import env_var_is_true

#
# -*- Workspace settings
#
# Workspace name: used for naming cloud resources
ws_name: str = "dp001"
# Workspace git repo url: used to git-sync DAGs and Charts
ws_repo: str = "https://github.com/phidatahq/aws-dp-template.git"
# Path to the workspace directory
ws_dir_path: Path = Path(__file__).parent.resolve()
# Path to the root i.e. data platform directory
data_platform_dir_path: Path = ws_dir_path.parent

#
# -*- Apps enabled in the workspace
#
pg_dbs_enabled: bool = True
superset_enabled: bool = True
jupyter_enabled: bool = True
airflow_enabled: bool = True
traefik_enabled: bool = True
whoami_enabled: bool = True

#
# -*- Dev settings
#
dev_env = "dev"
# Key for naming dev resources
dev_key = f"{ws_name}-{dev_env}"

#
# -*- Production settings
#
prd_env = "prd"
# Key for naming prd resources
prd_key = f"{ws_name}-{prd_env}"
# Tags for prd resources
prd_tags = {
    "Env": prd_env,
    "Project": ws_name,
}
# Domain for the production platform
prd_domain = "dp001.xyz"

#
# -*- AWS settings
#
# Region to use for AWS resources
aws_region: str = "us-east-1"
# Availability Zone for EbsVolumes
aws_az_1a: str = "us-east-1a"
aws_az_1b: str = "us-east-1b"
# 2 public subnets. 1 in each AZ.
public_subnets: List[str] = ["subnet-x0x0", "subnet-x0x0"]
# 2 private subnets. 1 in each AZ.
private_subnets: List[str] = ["subnet-x0x0", "subnet-x0x0"]
# Security Groups
security_groups: Optional[List[str]] = None

#
# -*- Settings from environment variables. Set these in .env file.
#
# By default use_cache=True and `phi` skips creation if a resource with the same name is found.
# Set use_cache=False to force recreate resources even if they exist.
use_cache: bool = env_var_is_true("USE_CACHE", True)
