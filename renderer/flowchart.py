def render_flowchart(data: dict) -> str:
    """
    Render the hierarchical roadmap as an ASCII tree/flowchart.
    
    Args:
        data: Validated roadmap dictionary with phases
    
    Returns:
        Formatted string representation of the roadmap
    """
    lines = []
    total_weeks = data.get('total_weeks', 16)
    lines.append(f"🧭 {data['domain']} Roadmap ({data['level']}) - {total_weeks} Weeks")
    lines.append("=" * 70)
    lines.append("")
    
    for phase_idx, phase in enumerate(data["phases"]):
        # Phase header with weeks
        lines.append(f"📅 {phase['weeks']} | {phase['name']}")
        if phase.get('description'):
            lines.append(f"   └─ {phase['description']}")
        lines.append("")
        
        topics = phase.get("topics", [])
        for t_idx, topic in enumerate(topics):
            is_last_topic = t_idx == len(topics) - 1
            topic_prefix = "   └─" if is_last_topic else "   ├─"
            lines.append(f"{topic_prefix} 📚 {topic['name']}")
            
            subtopics = topic.get("subtopics", [])
            for s_idx, subtopic in enumerate(subtopics):
                is_last_subtopic = s_idx == len(subtopics) - 1
                sub_connector = "      " if is_last_topic else "   │  "
                sub_prefix = "└─" if is_last_subtopic else "├─"
                lines.append(f"{sub_connector}{sub_prefix} 📌 {subtopic['name']}")
                
                items = subtopic.get("items", [])
                for i_idx, item in enumerate(items):
                    is_last_item = i_idx == len(items) - 1
                    if is_last_topic:
                        item_connector = "         " if is_last_subtopic else "      │  "
                    else:
                        item_connector = "   │     " if is_last_subtopic else "   │  │  "
                    item_prefix = "└─" if is_last_item else "├─"
                    lines.append(f"{item_connector}{item_prefix} {item}")
        
        lines.append("")
        if phase_idx < len(data["phases"]) - 1:
            lines.append("         ⬇️")
            lines.append("")
    
    return "\n".join(lines)


def render_mermaid(data: dict) -> str:
    """
    Render the hierarchical roadmap as a Mermaid flowchart diagram.
    
    Args:
        data: Validated roadmap dictionary with phases
    
    Returns:
        Mermaid flowchart syntax string
    """
    lines = []
    lines.append("```mermaid")
    lines.append("flowchart TB")
    
    # Sanitize text for Mermaid
    def sanitize(text: str) -> str:
        return text.replace('"', "'").replace("[", "(").replace("]", ")").replace("<", "").replace(">", "")
    
    def make_id(text: str) -> str:
        return text.replace(" ", "_").replace("-", "_").replace("&", "and").replace("/", "_").replace("(", "").replace(")", "").replace(",", "").replace(".", "").replace(":", "")[:30]
    
    # Create root node
    domain = sanitize(data['domain'])
    level = sanitize(data['level'])
    total_weeks = data.get('total_weeks', 16)
    lines.append(f'    ROOT["{domain}<br/>{level} • {total_weeks} Weeks"]')
    lines.append(f'    style ROOT fill:#6366f1,stroke:#4f46e5,color:#fff')
    
    prev_phase_id = "ROOT"
    
    for phase_idx, phase in enumerate(data["phases"]):
        phase_id = f"P{phase_idx}_{make_id(phase['name'])}"
        phase_name = sanitize(phase['name'])
        weeks = sanitize(phase['weeks'])
        
        lines.append(f'    {phase_id}["{weeks}<br/>{phase_name}"]')
        lines.append(f'    style {phase_id} fill:#fbbf24,stroke:#f59e0b,color:#000')
        lines.append(f'    {prev_phase_id} --> {phase_id}')
        
        prev_phase_id = phase_id
        
        topics = phase.get("topics", [])
        for t_idx, topic in enumerate(topics):
            topic_id = f"{phase_id}_T{t_idx}_{make_id(topic['name'])}"
            topic_name = sanitize(topic['name'])
            
            lines.append(f'    {topic_id}["{topic_name}"]')
            lines.append(f'    style {topic_id} fill:#fef3c7,stroke:#fcd34d,color:#000')
            lines.append(f'    {phase_id} --> {topic_id}')
            
            subtopics = topic.get("subtopics", [])
            for s_idx, subtopic in enumerate(subtopics):
                subtopic_id = f"{topic_id}_S{s_idx}"
                subtopic_name = sanitize(subtopic['name'])
                
                lines.append(f'    {subtopic_id}["{subtopic_name}"]')
                lines.append(f'    {topic_id} --> {subtopic_id}')
                
                # Only show first 3 items to keep diagram manageable
                items = subtopic.get("items", [])[:3]
                for i_idx, item in enumerate(items):
                    item_id = f"{subtopic_id}_I{i_idx}"
                    item_name = sanitize(item)[:40]
                    
                    lines.append(f'    {item_id}["{item_name}"]')
                    lines.append(f'    {subtopic_id} --> {item_id}')
    
    lines.append("```")
    
    return "\n".join(lines)
