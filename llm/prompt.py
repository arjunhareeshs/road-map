def roadmap_prompt(domain: str, level: str) -> str:
    return f"""Generate a learning roadmap JSON for "{domain}" at "{level}" level.

Output ONLY valid JSON (no markdown, no extra text):

{{"domain":"{domain}","level":"{level}","total_weeks":12,"phases":[
{{"name":"Foundations","weeks":"Week 1-3","description":"Core basics","topics":[
{{"name":"Topic1","subtopics":[{{"name":"Sub1","items":["item1","item2"]}}]}}
]}},
{{"name":"Core Concepts","weeks":"Week 4-6","description":"Main skills","topics":[...]}},
{{"name":"Intermediate","weeks":"Week 7-9","description":"Deeper learning","topics":[...]}},
{{"name":"Advanced","weeks":"Week 10-11","description":"Expert skills","topics":[...]}},
{{"name":"Projects","weeks":"Week 12","description":"Apply skills","topics":[...]}}
]}}

Rules:
- 5 phases with weeks
- 2-3 topics per phase
- 2-3 subtopics per topic  
- 2-4 items per subtopic
- Be concise, use short names
"""
- Industry-relevant, current tools and technologies
- Clear learning progression from basics to advanced
- Include practical projects and hands-on exercises
"""

