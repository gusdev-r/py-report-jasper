import os


UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'upload_folder')
print(UPLOAD_FOLDER)

def print_test():
  UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'upload_folder')
  print(UPLOAD_FOLDER)
  
print_test()