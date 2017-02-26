import time
import sys, traceback 

print("==== Sync IMDB Top Movies ====")
time.sleep(5)
try:
    print("Loading IMDB Top Movies.....")
    exec(open("./get_imdb_250.py", encoding = 'utf8').read())
except:
    print("Sync IMDB Top Movies Error Occurs!")
    exc_type, exc_value, exc_traceback = sys.exc_info()
    print("*** print_tb:")
    traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
    print("*** print_exception:")
    traceback.print_exception(exc_type, exc_value, exc_traceback, limit=2, file=sys.stdout)
    print("*** print_exc:")
    traceback.print_exc(limit=2, file=sys.stdout)
    print("*** format_exc, first and last line:")
    formatted_lines = traceback.format_exc().splitlines()
    print(formatted_lines[0])
    print(formatted_lines[-1])
    print("*** format_exception:")
    print(repr(traceback.format_exception(exc_type, exc_value, exc_traceback)))
    print("*** extract_tb:")
    print(repr(traceback.extract_tb(exc_traceback)))
    print("*** format_tb:")
    print(repr(traceback.format_tb(exc_traceback)))
    print("*** tb_lineno:", exc_traceback.tb_lineno)    
    sys.exit(1)

print("")
print("==== Sync Douban Top Movies ====")
time.sleep(5)

try:
    print("Loading Douban Top Movies.....")
    exec(open("./get_douban_250.py", encoding = 'utf8').read())
except:
    print("Sync Douban Top Movies Error Occurs!")
    traceback.print_exc(file=sys.stdout)
    sys.exit(1)

print("")
print("==== Sync Rotten Tomatoes Top Movies ====")
time.sleep(5)
try:
    print("Loading Tomatoes Top Movies.....")
    exec(open("./get_tomatoes_100.py", encoding = 'utf8').read())
except:
    print("Sync Rotten Tomatoes Top Movies Error Occurs!")
    sys.exit(1)