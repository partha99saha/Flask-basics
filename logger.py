import logging
import os


# Create a directory for logs if it doesn't exist
LOG_DIR = "logger"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Configure logging to write logs to the directory
log_file = os.path.join(LOG_DIR, "app.log")

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler = logging.FileHandler(log_file)
file_handler.setFormatter(formatter)
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.DEBUG)


# Logger Example
# app.logger.debug('This is a debug message')
# app.logger.info('This is an info message')
# app.logger.warning('This is a warning message')
# app.logger.error('This is an error message')
# app.logger.critical('This is a critical message')
