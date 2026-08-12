import sys
from networksecurity.logging import logger

class NetworkSecurityException(Exception):
    def __init__(self, error_message, error_details: sys):
        super().__init__(str(error_message))

        self.error_message = error_message
        _, _, exc_tb = error_details.exc_info()

        self.lineno = exc_tb.tb_lineno
        self.filename = exc_tb.tb_frame.f_code.co_filename

    def __str__(self):
        return (
            f"Error occurred in python script "
            f"[{self.filename}] "
            f"line number [{self.lineno}] "
            f"error message [{self.error_message}]"
        )