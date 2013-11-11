import argparse, os
from categorizer import Categorizer
from colorama import Fore, init, Back

init()

parser = argparse.ArgumentParser(description='Categorize your download folder')

# Required argument, tells the script where  the download folder is located on disk
parser.add_argument('-p', '--path', help='The path of the downloads folder')

# where to put the shows
parser.add_argument('-s', '--shows_folder', help='The path to put all the TV shows in')

# custom name to search for
parser.add_argument('-n', '--name', help='Send in if you only want to look for example "house", or "top gear, top.gear"')


'''
    These args don't need any parameters
'''

# use whitespace
parser.add_argument('-rw', '--rm_ws', action='store_true', help='Removes whitespace from string, can be useful when you want to search for "house" and not get any results from "House of Cards")')

# delete directories if they have no files
parser.add_argument('-d', '--delete', action='store_true', help='Try to delete the directories we moved if they have no shows left')


quit_chars = ["q", "quit", "exit"]


def prompt(data, root):
    length = len(data)
    if length == 0:
        print("No files found!")
        exit(1)
    else:
        i = input("{0} files will be moved, do you want to see the list? (y/n) --> ".format(len(data))).lower()
        if i == "y" or i == "yes":
            print("\n")
            for i, d in enumerate(data):
                print("Index: {3}{0}{4} - {3}{1}{4} --> {3}{2}{4}".format(i, d[2].replace(root, ""), d[1], Fore.GREEN, Fore.RESET))
                if length < 100: # only print newline if it's under a specific value, because it can fill the screen
                    print("\n")
        return i


# add param to delete if exists
def main():
    try:
        args = parser.parse_args()
        path, shows_folder, rm_ws, custom_name, delete = (args.path, args.shows_folder, args.rm_ws, args.name, args.delete)

        if not path:
            print(Fore.RED + "\nPath has to be specified!\n" + Fore.RESET)
            parser.print_help()
        elif not os.path.exists(path):
            print("Path doesn't exist!")
        else:

            # create object
            c = Categorizer(path, s_folder=shows_folder, rm_ws=rm_ws, custom_name=custom_name)
            
            # get data and sort it so it's easier for the user to look at
            data = sorted(c.data_shows(), key=lambda x: (x[1], x[2]))
            p = prompt(data, path)
            
            # prompt user so he can see what he is doing
            while p != "n":
                f = input("Do you want to edit the list? (y/n) --> ").lower()
                if f == "y" or f == "yes":
                    l = input("Enter in comma separated indices you want to remove --> ")

                    nums = l.split(',')
                    
                    if not all(map(lambda x: x.isdigit(), nums)):
                        print("Values have to be valid numerical characters")
                    else:
                        # remove by index
                        data = [d for i, d in enumerate(data) if i not in [int(k) for k in nums]]
                    
                p = prompt(data, path)
                
                if p in quit_chars:
                    exit(1)
                
            if p in quit_chars:
                exit(1)
            
            print("Creating data. . .")
            if delete:
                c.create(data)
            else:
                c.create(data, delete_if_exists=False)
            print("Complete!")    
                
    except Exception as err:
        print("Error in cleanup.main: %s" % err)


if __name__ == '__main__':
    main()







