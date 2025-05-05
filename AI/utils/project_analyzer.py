import os
import logging
import asyncio
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI


load_dotenv()

async def analyze_step(content, focus_area, llm):
    prompt = PromptTemplate(
        input_variables=["project_content"],
        template=f"""
        You are a Python expert. Analyze the following project content with a focus on **{focus_area}**.

        --- START OF PROJECT CONTENT ---
        {{project_content}}
        --- END OF PROJECT CONTENT ---

        Respond with concise, structured insights on the topic and code examples.
        """
    )
    chain = prompt | llm
    try:
        result = await chain.ainvoke({"project_content": content[:15000]})
        return result.content if hasattr(result, "content") else str(result)
    except Exception as e:
        logging.error(f"Error during analysis of '{focus_area}': {e}")
        return f"Error during analysis: {e}"


async def analyze_documents(documents, analysis_focus=None) -> str:
    joined_content = "\n\n".join([doc.page_content for doc in documents])

    llm = ChatOpenAI(
        model="openai/gpt-4.1-nano",
        base_url="https://models.github.ai/inference",
        api_key=os.getenv("GITHUB_API_KEY"),
        temperature=1,
        timeout=120,
    )

    # Default analysis steps
    default_steps = [
        "Overall structure",
        "Architecture strengths and weaknesses",
        "Code quality and maintainability",
        "Recommendations with code examples",
    ]
    
    # Additional specialized analysis options
    specialized_steps = {
        "security": [
            "Security vulnerabilities",
            "Authentication and authorization",
            "Data protection",
            "Input validation and sanitization"
        ],
        "performance": [
            "Computational efficiency",
            "Memory usage",
            "Bottlenecks",
            "Optimization opportunities"
        ],
        "testing": [
            "Test coverage",
            "Test quality",
            "Testing frameworks",
            "Mocking strategies"
        ],
        "documentation": [
            "Code documentation",
            "API documentation",
            "User guides",
            "Project setup instructions"
        ],
        "scalability": [
            "Horizontal scaling potential",
            "Vertical scaling limits",
            "Database scaling considerations",
            "Architectural scalability patterns"
        ]
    }
    
    # Determine which steps to use based on analysis_focus
    steps = default_steps
    if analysis_focus and analysis_focus in specialized_steps:
        steps = specialized_steps[analysis_focus]
    elif analysis_focus == "comprehensive":
        # For comprehensive analysis, include default steps plus selected specialized ones
        steps = default_steps + specialized_steps["security"] + specialized_steps["performance"]
    
    semaphore = asyncio.Semaphore(2)  # Limit concurrent requests

    async def analyze_and_log(step):
        async with semaphore:
            logging.info(f" [-] Starting analysis: {step}")
            result = await analyze_step(joined_content, step, llm)
            logging.info(f" [x] Finished analysis: {step}")
            section = f"## {step}\n{result}\n"
            return section

    partial_results = await asyncio.gather(*[analyze_and_log(step) for step in steps])
    
    analysis_results = []
    for step, result in zip(steps, partial_results):
        analysis_results.append((step, result))
    return analysis_results
    