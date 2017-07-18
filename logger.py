import traceback

global debug_level
debug_level = 0
global info_level
info_level = 1
global warning_level
warning_level = 2
global error_level
error_level = 3

global log_level
log_level = debug_level

log_kind = ["debug", "info", "warning", "error"]

def log(level, text):
    if level >= log_level:
        stack = traceback.extract_stack()
        filename, line, name, sentence = stack[-2]
        print "["+log_kind[level]+"][@"+filename.split("\\")[-1]+":"+str(line)+":"+name+"]:"+text
