from llm.prompt import roadmap_prompt
from llm.client import call_llm
from core.validator import validate_roadmap


def generate_roadmap(domain: str, level: str) -> dict:
    """
    Generate a complete learning roadmap for a given domain and level.
    
    Args:
        domain: The engineering/learning domain (e.g., "Electronics Engineering")
        level: Target expertise level ("Beginner", "Intermediate", "Advanced")
    
    Returns:
        Validated roadmap dictionary
    """
    # Generate prompt
    prompt = roadmap_prompt(domain, level)
    
    # Call LLM
    print(f"🔄 Generating roadmap for '{domain}' at '{level}' level...")
    roadmap_json = call_llm(prompt)
    
    # Validate response
    validate_roadmap(roadmap_json)
    print("✅ Roadmap validated successfully!")
    
    return roadmap_json
