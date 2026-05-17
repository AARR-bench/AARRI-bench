import os

def get_subdirectories(path):

  entries = os.listdir(path)
  
  subdirs = [entry for entry in entries 
              if os.path.isdir(os.path.join(path, entry))]
  return subdirs


target_directory = "./tasks" 

subdirectories = get_subdirectories(target_directory)


for subdir in subdirectories:
    print(f"  - {subdir}")
