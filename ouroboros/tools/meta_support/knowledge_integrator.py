from ouroboros.memory import knowledge

def integrate_knowledge(query: str) -> str:
    """
    Retrieve and synthesize relevant knowledge from the knowledge base.
    """
    topics = [
        "meta-architecture",
        "meta-api-access",
        "inventory-schema"
    ]
    
    results = []
    for topic in topics:
        try:
            content = knowledge.read(topic)
            if query.lower() in content.lower():
                results.append(f"\n\n# {topic}\n{content}")
        except Exception as e:
            results.append(f"\n[Ошибка чтения темы {topic}: {str(e)}]")
            
    if not results:
        return "Соответствующая информация не найдена в базе знаний."
        
    return "\n\n".join(results)
