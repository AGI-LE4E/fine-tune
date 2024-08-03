import os
import time
from dotenv import load_dotenv
from predibase import Predibase, FinetuningConfig, DeploymentConfig

load_dotenv()

api_token: str = os.getenv("PREDIBASE_API_TOKEN")
adapter_id: str = os.getenv("ADAPTER_ID")
pb = Predibase(api_token=api_token)

if __name__ == "__main__":
    # Get adapter, blocking call if training is still in progress
    adapter = pb.adapters.get(adapter_id)
    print(adapter)

    input_prompt="""
    <|im_start|>system\n주어지는 데이터는 제주도 위치 및 숙박업명에 대한 데이터 입니다.\n주어진 숙박업명 데이터를 보고 근처 맛집 리스트를 말해주세요<|im_end|>
    <|im_start|>제주도 숙박업명 및 위치\n숙박업명: HOTEL LEO - 주소: 제주특별자치도 제주시 삼무로 14<|im_end|>
    """

    lorax_client = pb.deployments.client("solar-1-mini-chat-240612")
    print(lorax_client.generate(input_prompt, adapter_id=adapter_id, max_new_tokens=1000).generated_text)
