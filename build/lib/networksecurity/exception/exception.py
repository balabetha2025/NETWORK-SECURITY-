import sys 
import logging
from networksecurity.logging.logger import logger
class NetworkSecurityException(Exception):
    def __init__(self, error_message:Exception, error_detail:sys):
        super().__init__(error_message)
        self.error_message = self.get_detailed_error_message(error_message=error_message, error_detail=error_detail)

    def get_detailed_error_message(self, error_message:Exception, error_detail:sys)-> str:
        _,_,exc_tb = error_detail.exc_info()
        line_number = exc_tb.tb_lineno
        file_name = exc_tb.tb_frame.f_code.co_filename
        detailed_error_message = f"Error occured in script: {file_name} at line number: {line_number} error message: {error_message}"
        return detailed_error_message

    def __str__(self):
        return "error occured in python script name [{0}] line number [{1}] error message [{2}]".format(self.error_message.split("script: ")[1].split(" at line")[0], self.error_message.split("line number: ")[1].split(" error message: ")[0], self.error_message.split("error message: ")[1])
        self.file_name,self.lineneno,str(self.error_message)

    def __repr__(self):
         return f"{self.__class__.__name__}({self.error_message!r})"
