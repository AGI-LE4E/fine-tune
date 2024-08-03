import os
import time
from dotenv import load_dotenv
from predibase import Predibase, FinetuningConfig, DeploymentConfig

load_dotenv()

api_token: str = os.getenv("PREDIBASE_API_TOKEN")
pb = Predibase(api_token=api_token)

dataset_name = "jeju_preprocessed"
csv_file_name = f"./jeju_datasets/{dataset_name}.csv"

if __name__ == '__main__':

    try:
        pb_dataset = pb.datasets.get(dataset_name)
        print(f"Dataset found: {pb_dataset}")
    except RuntimeError:
        print("Dataset not found")
        pb_dataset = pb.datasets.from_file(csv_file_name, name=dataset_name)
        print(f"Dataset created: {pb_dataset}")

    # Create an adapter repository
    repo_name = "jeju_lodgment_restaurant_recommender"
    repo = pb.repos.create(name=repo_name, description="LE4E jeju_lodgment_restaurant_recommender", exists_ok=True)
    print(repo)

    # Start a fine-tuning job, blocks until training is finished
    adapter = pb.adapters.create(
        config=FinetuningConfig(
            base_model="solar-1-mini-chat-240612",
            epochs=1, # default: 3
            rank=1, # default: 16
        ),
        dataset=pb_dataset, # Also accepts the dataset name as a string
        repo=repo,
        description="initial model with defaults"
    )
    print(adapter)
    adapter_id = adapter.repo + "/" + str(adapter.tag)
    print(adapter_id)