import logging, os, string, random, traceback

restricted_symbols  = ["<", ">", ";", "=" ]

def is_safe_input(input_text):
    
    if len(input_text) > 50:
        return False, "Username length exceeds limit."
    
    if any(rs in input_text for rs in restricted_symbols):
        return False, "Invalid charectes in input"
    
    return True, "Valid Inputs"


def getUid(noOfCharecters=6):
    chars = string.ascii_letters + string.digits
    uid = ''.join(random.choice(chars) for n in range(noOfCharecters))
    return uid

def create_dirs(dirs):
    if type(dirs) == str:
        dirs = [dirs]

    for directory in dirs:
        if not os.path.isdir(directory):
            print(f"Creating dir {directory}")
            os.makedirs(directory)

def get_logger():
    print("Setting up logger.")
    log_format =logging.Formatter('%(asctime)s-%(process)d-[%(filename)s:%(lineno)s - %(funcName)s() ]-%(levelname)s-%(message)s')
    # log_format =logging.Formatter('%(asctime)s-%(process)d-%(levelname)s-%(message)s')
    logger = logging.getLogger() 
    logger.setLevel(logging.INFO)

    create_dirs("./logs/")

    if not logger.handlers:
        print("No handlers found. Creating fileHandler and consoleHandler.")
        # logging.basicConfig(
        #     format = "{asctime} - {levelname} - {message}",
        #     style="{",
        #     datefmt="%Y-%m-%d-%H:%M:%S.%3d"
        # )
        fileHandler = logging.FileHandler("./logs/app.log")
        fileHandler.setFormatter(log_format)
        logger.addHandler(fileHandler)

        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(log_format)
        logger.addHandler(consoleHandler)

    return logger


class Logger:
 
    __shared_instance = get_logger()
 
    @staticmethod
    def getInstance():
        """Static Access Method"""
        if not isinstance(Logger.__shared_instance, logging.RootLogger):
            Logger()
        return Logger.__shared_instance
 
    def __init__(self):
        """virtual private constructor"""
        if not isinstance(self.__shared_instance, logging.RootLogger):
            raise Exception("This class is a singleton class !")
        else:
            Logger.__shared_instance = self


class clogs:
    def __init__(self, logger = None):
        if not logger:
            try:
                logger = Logger.getInstance()
            except Exception as e:
                logger = logger
                print(traceback.print_exc())
        self.logger = logger
        self.log("Getting logger.")

    def log(self, message):
        if not self.logger:
            print(message)
            return
        
        self.logger.info(message)
    
    def error(self, message):
        if not self.logger:
            print(message)
            return

        self.logger.error(message)
    
    def debug(self, message):
        if not self.logger:
            print(message)
            return

        self.logger.debug(message)

# class Logger:
 
 
#     log_format =logging.Formatter('%(process)d-%(levelname)s-%(message)s')
#     logger = logging.getLogger() 
#     logger.setLevel(logging.INFO)
#     fileHandler = logging.FileHandler("./logs/app.log")
#     fileHandler.setFormatter(log_format)
#     logger.addHandler(fileHandler)
#     consoleHandler = logging.StreamHandler()
#     consoleHandler.setFormatter(log_format)
#     logger.addHandler(consoleHandler)

#     __shared_instance = logger

#     @staticmethod
#     def getInstance():
#         """Static Access Method"""
#         if not isinstance(Logger.__shared_instance, logging.RootLogger):
#             Logger()
#         return Logger.__shared_instance
 
#     def __init__(self):
#         """virtual private constructor"""
#         if not isinstance(self.__shared_instance, logging.RootLogger):
#             raise Exception("This class is a singleton class !")
#         else:
#             Logger.__shared_instance = self