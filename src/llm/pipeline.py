from langchain_core.tracers.langchain import get_client
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from langchain.prompts import PromptTemplate
from langchain.llms import HuggingFacePipeline
from langchain.chains import LLMChain
import torch


def set_up_pipeline(modelPath):
    """
    Configure la pipeline pour utiliser le modèle et le tokenizer.
    """
    tokenizer = AutoTokenizer.from_pretrained(modelPath)
    model = AutoModelForCausalLM.from_pretrained(modelPath)

    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)

    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=10,
        eos_token_id=tokenizer.eos_token_id,
        temperature=0.2,  # Faible température pour réduire l'aléatoire
        top_k=50,  # Restreindre à 50 tokens les plus probables
        top_p=0.9,  # Sélection cumulative des tokens probables
    )

    local_llm = HuggingFacePipeline(pipeline=pipe)
    return local_llm, tokenizer, pipe
