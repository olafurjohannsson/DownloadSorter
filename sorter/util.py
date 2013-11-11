import os, re, shutil

def find(value, name):
    '''
    Find an exact substr inside a string.
    '''
    return re.findall(r'\b(%s)\b' % value, name.lower())

def copy_file(old_dst, new_dst):
    '''
    Copy file from destination to a new destination
    if it does not exist already, return True if success.
    '''
    try:
        if not os.path.isfile(new_dst):
            shutil.move(old_dst, new_dst)
            return True
        
    except Exception as err:
        print("Error in copy_file: %s" %err)    

def create_dir(path):
    '''
    Create directory if it does not exist already,
    return True if success in creating.
    '''
    try:
        if not os.path.exists(path):
            os.makedirs(path)
            return True
        
    except Exception as err:
        print("Error in create_dir: %s" %err)
