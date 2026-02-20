import logging
import sys
from datetime import datetime

def setup_logger(name: str, log_file: str = None, level: str = None):
    """
    Function to set up a logger with specified name and configuration.

    Args:
        name: Name of the logger
        log_file: Optional file to log to
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    if level is None:
        # Import config here to avoid circular import during module loading
        from src.utils.config import Config
        level = Config.LOG_LEVEL

    # Convert string level to logging constant
    log_level = getattr(logging, level.upper(), logging.INFO)

    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    # Prevent adding multiple handlers to the same logger
    if logger.handlers:
        return logger

    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)

    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(formatter)

    # Add console handler to logger
    logger.addHandler(console_handler)

    # Optionally add file handler
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger

def log_agent_action(agent_name: str, action: str, details: dict = None):
    """
    Log an action performed by an agent with appropriate context.

    Args:
        agent_name: Name of the agent performing the action
        action: Description of the action
        details: Additional details about the action (optional)
    """
    logger = setup_logger(f"agent.{agent_name}")
    log_msg = f"Agent {agent_name} performing action: {action}"
    if details:
        log_msg += f" | Details: {details}"

    logger.info(log_msg)

def log_query_processing(query_id: str, user_id: str, status: str, details: dict = None):
    """
    Log query processing events with appropriate context.

    Args:
        query_id: ID of the query being processed
        user_id: ID of the user making the query
        status: Current status of the query
        details: Additional details about the processing (optional)
    """
    logger = setup_logger("query.processing")
    log_msg = f"Query {query_id} for user {user_id} - Status: {status}"
    if details:
        log_msg += f" | Details: {details}"

    logger.info(log_msg)

def log_document_processing(doc_id: str, action: str, status: str, details: dict = None):
    """
    Log document processing events with appropriate context.

    Args:
        doc_id: ID of the document being processed
        action: Action being performed on the document
        status: Current status of the processing
        details: Additional details about the processing (optional)
    """
    logger = setup_logger("document.processing")
    log_msg = f"Document {doc_id} - Action: {action}, Status: {status}"
    if details:
        log_msg += f" | Details: {details}"

    logger.info(log_msg)