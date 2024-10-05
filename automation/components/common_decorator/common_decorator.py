from netmiko import NetmikoTimeoutException, NetmikoBaseException, NetmikoAuthenticationException
from paramiko import  AuthenticationException, SSHException
from concurrent.futures import CancelledError,TimeoutError,BrokenExecutor
from assets.text_file import Text_File
from assets.text_style import Text_Style


def NetmikoException_Handler(method: any):
    """
    Handles all Netmiko and Paramiko exceptions.

    Arguments:
        method (function): The class method to wrap with exception handling.

    Returns:
        Any: The result of the method, or False if an exception occurs.
    """
    def wrapper(*args, **kwargs):
        try:
            return method(*args, **kwargs)
        except NetmikoTimeoutException:
            Text_Style.common_text(
                primary_text=Text_File.exception_text["Netmiko_Timeout_Exception"],
                secondary_text=__name__
            )
            return False
        except NetmikoBaseException:
            Text_Style.common_text(
                primary_text=Text_File.exception_text["Netmiko_Base_Exception"],
                secondary_text=__name__
            )
            return False
        except NetmikoAuthenticationException:
            Text_Style.common_text(
                primary_text=Text_File.exception_text["Netmiko_Authentication_exception"],
                secondary_text=__name__
            )
            return False
        except SSHException:
            Text_Style.common_text(
                primary_text=Text_File.exception_text["ssh_exception"],
                secondary_text=__name__
            )
            return False
        except AuthenticationException:
            Text_Style.common_text(
                primary_text=Text_File.exception_text["paramiko_auth_exception"],
                secondary_text=__name__
            )
            return False
        except TypeError:
            Text_Style.common_text(
                primary_text=Text_File.exception_text["Type_error"],
                secondary_text=__name__
            )
            return False
        except IOError as ioerror:
            Text_Style.ExceptionTextFormatter(primary_text=Text_File.exception_text["IOerror"],secondary_text=ioerror)
            
        except Exception as e:
            # Catch any other unexpected exceptions
            Text_Style.common_text(
                primary_text=Text_File.exception_text["general_exception"],
                secondary_text=str(e)
            )
            return False
        

    return wrapper

def Regular_Exception_Handler(method: any):
    """
    A decorator for handling common exceptions that may occur during the execution 
    of a wrapped method. 

    This decorator catches specific exceptions and processes them by calling a 
    common text display method from the `Text_Style` class, passing relevant 
    exception messages.

    Args:
        method (callable): The function to be decorated and wrapped with exception 
                           handling logic.

    Returns:
        callable: The wrapper function that includes the exception handling logic.

    Exceptions Handled:
        - ValueError: Caught when a function receives an argument of the right type 
          but inappropriate value.
        - TypeError: Caught when an operation or function is applied to an object 
          of inappropriate type.
        - ModuleNotFoundError: Caught when an imported module cannot be found.

    Usage:
        @Regular_Exception_Handler
        def my_function(arg):
            # Function logic here
            pass

    Notes:
        The decorator returns False if any of the specified exceptions are caught, 
        which can be used by the calling code to determine if the function 
        executed successfully.
    """
    def wrapper(*args, **kwargs):
        try:
            return method(*args, **kwargs)
        except ValueError as valuerror:
            Text_Style.ExceptionTextFormatter(primary_text=Text_File.exception_text["value_error"], secondary_text=valuerror)
            return False
        except TypeError as typoerror:
            Text_Style.ExceptionTextFormatter(primary_text=Text_File.exception_text["Type_error"], secondary_text=typoerror)
            return False
        except ModuleNotFoundError as moduleerror:
            Text_Style.ExceptionTextFormatter(primary_text=Text_File.exception_text["Module_error"], secondary_text=moduleerror)
            return False
        except IOError as ioerror:
            Text_Style.ExceptionTextFormatter(primary_text=Text_File.exception_text["IOerror"],secondary_text=ioerror)
        except FileExistsError as filerror:
            Text_Style.ExceptionTextFormatter(primary_text=Text_File.exception_text["file_not_found"],secondary_text=filerror)
    return wrapper

def ThreadPoolExeceptionHandler(method):
    def wrapper(*args,**kwargs):
        try:
            return method(*args,**kwargs)
        except CancelledError as cancelled:
            Text_Style.ExceptionTextFormatter(primary_text=Text_File.threadpool_module_exception_text["Cancelled_Error"],secondary_text=cancelled)
            return False
        except TimeoutError as timeout:
            Text_Style.ExceptionTextFormatter(primary_text=Text_File.threadpool_module_exception_text["TimeoutError"],secondary_text=timeout)
            return False
        except BrokenExecutor as broken:
            Text_Style.ExceptionTextFormatter(primary_text=Text_File.threadpool_module_exception_text["BrokenExecutor"],secondary_text=broken)
            return False
        except ValueError as value:
            Text_Style.ExceptionTextFormatter(primary_text=Text_File.threadpool_module_exception_text["ValueError"],secondary_text=value)
            return False
        except IOError as ioerror:
            Text_Style.ExceptionTextFormatter(primary_text=Text_File.exception_text["IOerror"],secondary_text=ioerror)

    return wrapper
        
           

