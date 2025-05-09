import asyncio
import logging

from langchaincore.utils.project_loader import load_and_split_project_files
from langchaincore.utils.project_analyzer import analyze_documents
from langchaincore.utils.report_generator import generate_html_report
from langchaincore.utils.utils import clone_repo, remove_directory

from langchaincore.loggers import LogLevels, configure_logging

async def run_pipeline(repo_url, analysis_type=None):
    try:
        repo_path = clone_repo(repo_url)
        docs = load_and_split_project_files(repo_path)

        logging.info(f" + Analyzing project{' with focus on ' + analysis_type if analysis_type else ''}...")
        analysis_results = await analyze_documents(docs, analysis_type)

        logging.info(" + Generating report...")
        generate_html_report(analysis_results, "report.html")
        
        remove_directory(repo_path)
    except Exception as e:
        logging.error(f" + Error in pipeline: {e}")

async def run_pipeline_cli(github_url: str, analysis_type: str = None):
    configure_logging(log_level=LogLevels.info)
    github_url = github_url
    
    analysis_choice = analysis_type
    
    analysis_map = {
        "1": None,
        "2": "security",
        "3": "performance",
        "4": "testing",
        "5": "documentation",
        "6": "scalability",
        "7": "comprehensive"
    }
    
    analysis_type = analysis_map.get(analysis_choice, None)
    
    try:
        await run_pipeline(github_url, analysis_type)
    except KeyboardInterrupt:
        logging.info(" - Pipeline execution interrupted by user.")
        
        
        
    # print("\nAvailable analysis types:")
    # print("1. Default (Overall structure, architecture, code quality, recommendations)")
    # print("2. Security (Vulnerabilities, authentication, data protection)")
    # print("3. Performance (Efficiency, memory usage, bottlenecks, optimization)")
    # print("4. Testing (Test coverage, quality, frameworks)")
    # print("5. Documentation (Code docs, API docs, guides)")
    # print("6. Scalability (Scaling patterns, database considerations)")
    # print("7. Comprehensive (Default + Security + Performance)")
    # input("Provide the GitHub repository URL: ")
    #  input("\nChoose analysis type (1-7) or press Enter for default: ")