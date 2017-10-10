# -*- coding: utf-8 -*-
"""
Contributors:
    - Louis Rémus
"""
import logging.config
import os

log_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                             'logger.ini')
logging.config.fileConfig(log_file_path, disable_existing_loggers=False)


def log_args(func):
    """
    Decorator to print function call details - parameters names and effective values
    Args:
        func (function):

    Returns:
        Decorated function
    """
    logger = logging.getLogger(__name__)

    def wrapper(*func_args, **func_kwargs):
        """
        Wrapper of our decorator
        Args:
            *func_args (tuple):
            **func_kwargs (dict):

        Returns:
            decorated function
        """
        # Get the arguments' names
        arg_names = func.__code__.co_varnames
        params = [('args', dict(zip(arg_names, func_args))),
                  ('kwargs', func_kwargs)]
        # Do not forget the default arguments
        # Values
        defaults = func.__defaults__ or ()
        # Their names (ordered)
        default_names = set(arg_names) - set(params[0][1].keys()) - set(params[1][1].keys())
        # Map them to their names
        defaults_mapped = dict(zip(default_names, defaults))
        # Add them to the list of parameters to print
        params.append(('defaults', defaults_mapped))
        # Log our parameters
        logger.debug('{} ({})'.format(func.__name__, ', '.join('%s = %r' % p for p in params)))
        # Return our function execution
        return func(*func_args, **func_kwargs)

    return wrapper


# Example function
@log_args
def awesome_function(a, b, c=1, d='Edouard', e='est pd'):
    print(a + b + c)
    print('{} {}'.format(d, e))

# For test purposes
if __name__ == '__main__':
    awesome_function(1, b=3)
