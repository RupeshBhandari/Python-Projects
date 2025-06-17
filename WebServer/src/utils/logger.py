import logging
import os
from datetime import datetime
from pathlib import Path

class Logger:
    """
    A centralized logging system for the web server project.
    Handles logging configuration and provides methods for different log levels.
    """
    
    _loggers = {}  # Store logger instances by name
    
    def __init__(self, name='web_server', log_level=logging.INFO):
        """
        Initialize a new logger or return an existing one with the given name.
        
        Args:
            name (str): Name of the logger
            log_level (int): Logging level (default: logging.INFO)
        """
        # Create logs directory if it doesn't exist
        logs_dir = Path('logs')
        logs_dir.mkdir(exist_ok=True)
        
        # Use existing logger if already created
        if name in Logger._loggers:
            self.logger = Logger._loggers[name]
            return
            
        # Create new logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)
        
        # Clear existing handlers to avoid duplicates
        if self.logger.handlers:
            self.logger.handlers.clear()
        
        # Create log filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_filename = f"logs/{name}_{timestamp}.log"
        
        # Create file handler
        file_handler = logging.FileHandler(log_filename)
        file_handler.setLevel(log_level)
        
        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        
        # Create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add handlers to logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        
        # Store logger in class dict
        Logger._loggers[name] = self.logger
    
    def debug(self, message):
        """Log debug message"""
        self.logger.debug(message)
    
    def info(self, message):
        """Log info message"""
        self.logger.info(message)
    
    def warning(self, message):
        """Log warning message"""
        self.logger.warning(message)
    
    def error(self, message):
        """Log error message"""
        self.logger.error(message)
    
    def critical(self, message):
        """Log critical message"""
        self.logger.critical(message)
    
    @staticmethod
    def get_logger(name='web_server'):
        """Get an existing logger or create a new one"""
        return Logger(name).logger