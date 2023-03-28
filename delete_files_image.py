import os

def delete():
    files_to_delete =['Youtube_comments.csv']
    for file in files_to_delete:
        os.remove(file)