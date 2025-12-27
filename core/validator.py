def validate_roadmap(data: dict) -> bool:
    """
    Validate the new hierarchical roadmap structure with phases and weeks.
    Raises ValueError if validation fails.
    Returns True if valid.
    """
    # Check top-level keys
    if "domain" not in data:
        raise ValueError("Missing 'domain' field in response")
    
    if "level" not in data:
        raise ValueError("Missing 'level' field in response")
    
    if "phases" not in data:
        raise ValueError("Missing 'phases' field in response")
    
    phases = data.get("phases", [])
    
    if not isinstance(phases, list) or len(phases) == 0:
        raise ValueError("'phases' must be a non-empty list")
    
    # Validate each phase
    for i, phase in enumerate(phases):
        if not isinstance(phase, dict):
            raise ValueError(f"Phase {i+1} must be a dictionary")
        
        if "name" not in phase:
            raise ValueError(f"Phase {i+1} missing 'name' field")
        
        if "weeks" not in phase:
            raise ValueError(f"Phase {i+1} missing 'weeks' field")
        
        if "topics" not in phase:
            raise ValueError(f"Phase {i+1} missing 'topics' field")
        
        topics = phase.get("topics", [])
        if not isinstance(topics, list) or len(topics) == 0:
            raise ValueError(f"Phase '{phase['name']}' must have at least one topic")
        
        # Validate each topic
        for j, topic in enumerate(topics):
            if not isinstance(topic, dict):
                raise ValueError(f"Topic {j+1} in phase '{phase['name']}' must be a dictionary")
            
            if "name" not in topic:
                raise ValueError(f"Topic {j+1} in phase '{phase['name']}' missing 'name' field")
            
            if "subtopics" not in topic:
                raise ValueError(f"Topic '{topic['name']}' missing 'subtopics' field")
            
            subtopics = topic.get("subtopics", [])
            if not isinstance(subtopics, list) or len(subtopics) == 0:
                raise ValueError(f"Topic '{topic['name']}' must have at least one subtopic")
            
            # Validate each subtopic
            for k, subtopic in enumerate(subtopics):
                if not isinstance(subtopic, dict):
                    raise ValueError(f"Subtopic {k+1} in topic '{topic['name']}' must be a dictionary")
                
                if "name" not in subtopic:
                    raise ValueError(f"Subtopic {k+1} in topic '{topic['name']}' missing 'name' field")
                
                if "items" not in subtopic:
                    raise ValueError(f"Subtopic '{subtopic['name']}' missing 'items' field")
                
                items = subtopic.get("items", [])
                if not isinstance(items, list) or len(items) == 0:
                    raise ValueError(f"Subtopic '{subtopic['name']}' must have at least one item")
    
    return True
