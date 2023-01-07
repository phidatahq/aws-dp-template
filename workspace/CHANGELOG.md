## Data Platform Changelog

### Jan 5th 2023

1. Enable Superset Public Role
2. Enable Github Authentication - differentiate between admin & users based on team.
3. Use Rds as database
4. Use Elasticache as cache
5. Build custom image (ECR) using github actions
6. Fix connectivity issues using cross-zone load balancing
7. Add 3 jupyterlab notebooks
8. Run new DAGs
9. Run Airflow & Jupyter dev locally

Steps:

1. Clone: https://github.com/phidatahq/starter-aws-snowflake-ds.git
2. Update workspace.
3. Create new AWS resources: `phi ws up --env prd --config aws`
4. Update database security group to allow traffic from port.
5. Update cache security group to allow traffic from port.
6. Create IAM user `github-actions` with permission: AmazonEC2ContainerRegistryPowerUser.
7. Update Github secrets.
8. Create new ECR repo for custom images.
9. Create new ECR images using github actions.
10. Update database + cache creds in airflow secrets.
11. Update database + cache creds in superset secrets.
12. Create Github Oauth App.
13. Update Github client creds in airflow secrets.
14. Update Github client creds in superset secrets.
15. Create new k8s resources: `phi ws up --env prd --config k8s`
16. Delete unused EBS volumes.
17. Delete airflow/superset database/redis running on k8s.
18. Install docker desktop.
19. Run `phi ws up --env dev`.
