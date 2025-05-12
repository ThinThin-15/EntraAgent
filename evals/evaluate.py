from azure.ai.projects import AIProjectClient
from azure.ai.agents.models import Agent, ThreadRun, RunStatus, MessageRole
from azure.ai.projects.models import ConnectionType
# from azure.ai.projects.models import (
#     AgentEvaluationRequest,
#     InputDataset,
#     EvaluatorIds,
#     EvaluatorConfiguration,
#     AgentEvaluationSamplingConfiguration,
#     AgentEvaluationRedactionConfiguration,
# )
from azure.ai.agents.aio import AgentsClient
from azure.identity import DefaultAzureCredential
from azure.ai.evaluation import (
    #AIAgentConverter, 
    evaluate, FluencyEvaluator, ToolCallAccuracyEvaluator, IntentResolutionEvaluator, TaskAdherenceEvaluator,
    QAEvaluator, ContentSafetyEvaluator)

import os
import time
import json
from pathlib import Path
from dotenv import load_dotenv

def get_agent_client(agent_client) -> AgentsClient:
    return agent_client

def run_evaluation():
    """Demonstrate how to evaluate an AI agent using the Azure AI Project SDK"""
    current_dir = Path(__file__).parent
    eval_queries_path = current_dir / "eval-queries.json"
    eval_input_path = current_dir / f"eval-input.jsonl"
    eval_output_path = current_dir / f"eval-output.json"

    env_path = current_dir / "../src/.env"
    load_dotenv(dotenv_path=env_path)

    # Get AI project parameters from environment variables
    ai_project_resource_id = os.environ.get("AZURE_EXISTING_AIPROJECT_RESOURCE_ID")
    deployment_name = os.getenv("AZURE_AI_AGENT_DEPLOYMENT_NAME")
    parts = ai_project_resource_id.split("/")    
    proj_endpoint = f'https://{parts[8]}.services.ai.azure.com/api/projects/{parts[10]}'
    agent_id = "asst_2U73baIGjgCE6E7ec52JjcSU"#os.environ.get("AZURE_EXISTING_AGENT_ID") if os.environ.get("AZURE_EXISTING_AGENT_ID") else os.environ.get("AZURE_AI_AGENT_ID")

    # Initialize the AIProjectClient and related entities
    ai_project = AIProjectClient(
        credential=DefaultAzureCredential(exclude_shared_token_cache_credential=True),
        endpoint=proj_endpoint,
        api_version = "2025-05-01"            
    )
    # connections = ai_project.connections.list(
    #     connection_type=ConnectionType.AZURE_OPEN_AI, include_credentials=True
    # )
    # default_connection = connections[0]
    # model_config = default_connection.to_evaluator_model_config(
    #     deployment_name=deployment_name,
    #     api_version="",
    #     include_credentials=True,
    # )
    model_config = {
        "azure_deployment": deployment_name,
        "azure_endpoint": "https://aoai-qyrftgva6obps.cognitiveservices.azure.com/openai/deployments/gpt-4o-mini/chat/completions?api-version=2025-01-01-preview",
        "api_key": "<key>"
    }
    agent = ai_project.agents.get_agent(agent_id)
    agent_client = get_agent_client(ai_project.agents)
    #thread_data_converter = AIAgentConverter(ai_project)

    # Read data input file 
    with open(eval_queries_path, "r", encoding="utf-8") as f:
        test_data = json.load(f)
    
    # Execute the test data against the agent and prepare the evaluation input
    with open(eval_input_path, "w", encoding="utf-8") as f:        

        for row in test_data:
            # Create a new thread for each query to isolate conversations
            thread = agent_client.threads.create()
            
            # create the user query
            agent_client.messages.create(
                thread.id, role=MessageRole.USER, content=row.get("query")
            )

            # Run the agent and measure performance
            start_time = time.time()
            run = agent_client.runs.create_and_process(
                thread_id=thread.id, agent_id=agent.id
            )
            end_time = time.time()

            if run.status != RunStatus.COMPLETED:
                raise ValueError(run.last_error or "Run failed to complete")

            metrics = {
                "server-run-duration-in-seconds": (
                    run.completed_at - run.created_at
                ).total_seconds(),
                "client-run-duration-in-seconds": end_time - start_time,
                "completion-tokens": run.usage.completion_tokens,
                "prompt-tokens": run.usage.prompt_tokens,
                "ground-truth": row.get("ground-truth", '')
            }

            # agent_evaluation_request = AgentEvaluationRequest(
            #     run_id=run.id,
            #     thread_id=thread.id,
            #     evaluators={
            #         "violence": EvaluatorConfiguration(
            #             id=EvaluatorIds.VIOLENCE,
            #         )
            #     }
            # )

            # Get the last message from the assistant
            messages = agent_client.messages.list(
                thread.id, run_id=run.id
            )
            for msg in messages:
                if msg.text_messages:
                    last_text = msg.text_messages[-1]
                    print(f"{msg.role}: {last_text.text.value}")
            
            # Add thread data + operational metrics to the evaluation input
            #evaluation_data = thread_data_converter.prepare_evaluation_data(thread_ids=thread.id)

            if (last_text and last_text.text and last_text.text.value):
                eval_item = {
                    "query": row.get("query"),
                    "ground-truth": row.get("ground-truth", ''),
                    "response": last_text.text.value,
                    "metrics": metrics,
                }
                # eval_item = evaluation_data[0]
                # eval_item["metrics"] = metrics
                f.write(json.dumps(eval_item) + "\n")   
        

    # Now, run a sample set of evaluators using the evaluation input
    # See https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/develop/agent-evaluate-sdk
    # for the full list of evaluators availalbe
    tool_call_accuracy = ToolCallAccuracyEvaluator(model_config=model_config)
    intent_resolution = IntentResolutionEvaluator(model_config=model_config)
    task_adherence = TaskAdherenceEvaluator(model_config=model_config)
    #qa = QAEvaluator(model_config=model_config)
    #content_safety = ContentSafetyEvaluator(model_config=model_config)
    results = evaluate(
        data=eval_input_path,
        evaluators={
            #"tool_call_accuracy": tool_call_accuracy,
            "intent_resolution": intent_resolution,
            "task_adherence": task_adherence,
            "operational_metrics": OperationalMetricsEvaluator(),
        },
        output_path=eval_output_path, # raw evaluation results
        #azure_ai_project=ai_project.scope, # needed only if you want results uploaded to AI Foundry
    )

    # Print the evaluation results
    print_eval_results(results, eval_input_path, eval_output_path)
    
    return results

class OperationalMetricsEvaluator:
    """Propagate operational metrics to the final evaluation results"""
    def __init__(self):
        pass
    def __call__(self, *, metrics: dict, **kwargs):
        return metrics


def print_eval_results(results, input_path, output_path):
    """Print the evaluation results in a formatted table"""    
    metrics = results.get("metrics", {})

    # Get the maximum length for formatting
    key_len = max(len(key) for key in metrics.keys()) + 5
    value_len = 20
    full_len = key_len + value_len + 5
    
    # Format the header
    print("\n" + "=" * full_len)
    print("Evaluation Results".center(full_len))
    print("=" * full_len)
    
    # Print each metric
    print(f"{'Metric':<{key_len}} | {'Value'}")
    print("-" * (key_len) + "-+-" + "-" * value_len)
    
    for key, value in metrics.items():
        if isinstance(value, float):
            formatted_value = f"{value:.2f}"
        else:
            formatted_value = str(value)
        
        print(f"{key:<{key_len}} | {formatted_value}")
    
    print("=" * full_len + "\n")

    # Print additional information
    print(f"Evaluation input: {input_path}")
    print(f"Evaluation output: {output_path}")
    if results.get("studio_url") is not None:
        print(f"AI Foundry URL: {results['studio_url']}")

    print("\n" + "=" * full_len + "\n")


if __name__ == "__main__":
    try:
        run_evaluation()
    except Exception as e:
        print(f"Error during evaluation: {e}")

