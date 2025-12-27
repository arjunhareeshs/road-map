import os
import json
from dotenv import load_dotenv

# Load environment variables first
load_dotenv()

from core.generator import generate_roadmap
from renderer.flowchart import render_flowchart, render_mermaid


def save_roadmap(data: dict, domain: str, output_dir: str = "output"):
    """Save roadmap to JSON file"""
    os.makedirs(output_dir, exist_ok=True)
    filename = f"{domain.lower().replace(' ', '_')}_roadmap.json"
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Saved to: {filepath}")
    return filepath


def main():
    print("=" * 60)
    print("🚀 LLM-Powered Roadmap Generator")
    print("=" * 60)
    print()
    
    # Get user input
    domain = input("📚 Enter Engineering Domain: ").strip()
    if not domain:
        print("❌ Domain cannot be empty!")
        return
    
    print("\nAvailable levels: Beginner | Intermediate | Advanced")
    level = input("📊 Enter Level: ").strip()
    if not level:
        level = "Beginner"
    
    print()
    
    try:
        # Generate roadmap
        roadmap_data = generate_roadmap(domain, level)
        
        # Render as tree
        output = render_flowchart(roadmap_data)
        print("\n" + output)
        
        # Save to file
        save_roadmap(roadmap_data, domain)
        
        # Ask if user wants Mermaid output
        mermaid = input("\n📊 Generate Mermaid diagram? (y/n): ").strip().lower()
        if mermaid == 'y':
            mermaid_output = render_mermaid(roadmap_data)
            print("\n" + mermaid_output)
            
            # Save mermaid to file
            os.makedirs("output", exist_ok=True)
            mermaid_file = f"output/{domain.lower().replace(' ', '_')}_roadmap.md"
            with open(mermaid_file, "w", encoding="utf-8") as f:
                f.write(f"# {domain} Roadmap ({level})\n\n")
                f.write(mermaid_output)
            print(f"💾 Mermaid saved to: {mermaid_file}")
        
    except json.JSONDecodeError as e:
        print(f"❌ Failed to parse LLM response as JSON: {e}")
    except ValueError as e:
        print(f"❌ Validation error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
