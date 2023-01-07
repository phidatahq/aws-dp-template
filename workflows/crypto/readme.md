## Crypto workflows

### Test DAGs

```sh
# ssh into airflow-ws or airflow-worker
docker exec -it airflow-worker-container zsh

# List DAGs
airflow dags list

# List tasks
airflow tasks list -t crypto_prices

# Test tasks
airflow tasks test \
  crypto_prices \
  load_crypto_prices \
  2022-07-01

airflow tasks test \
  crypto_prices \
  drop_existing_prices \
  2022-07-01

# Test tasks for ds + hour
airflow tasks test \
  crypto_prices \
  load_crypto_prices \
  2022-07-01T01:05:00
```
