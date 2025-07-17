# Create work-pool
prefect work-pool create "main-work-pool" --type process

# Create deployment
prefect deploy --prefect-file prefect/prefect.yaml --all

# Start worker
prefect worker start --pool "main-work-pool"
