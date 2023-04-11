import os
import sys

from prefect.deployments import Deployment
from prefect.server.schemas.schedules import CronSchedule

sys.path.append(os.getcwd())
from flows.trading_flows import fetch_data_flow

deployment = Deployment.build_from_flow(
    flow=fetch_data_flow,
    name="data-source",
    schedule=(CronSchedule(cron="0 0 * * *", timezone="Europe/Dublin")),
    work_queue_name="worker-queue",
    work_pool_name="worker-pool",
)

deployment.apply()


# if we have to do manually
"""
prefect config set PREFECT_LOCAL_STORAGE_PATH="/home/shekhar/shekhar/test/AlgorithmicTrading"
prefect config set PREFECT_HOME="/home/shekhar/shekhar/test/AlgorithmicTrading"
"""
# prefect server start
# prefect work-pool create "worker-pool"
# prefect agent start -p "worker-pool"
# prefect deployment build -n fetch-data -p worker-pool -q worker-queue src/flows/trading_flows.py:fetch_data_flow
# prefect deployment apply fetch_data_flow-deployment.yaml
