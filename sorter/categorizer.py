import json, os, fnmatch, re, shutil
from util import *

class Categorizer():
    '''
    Object that handles categorizing your download folder.
    '''

    shows_folder = 'Shows'

    # ctor
    def __init__(self, path, s_folder=None, rm_ws=False, custom_name=None):

        '''
        path: Location of downloads folder
        s_folder: Location of where to output the shows
        rm_ws: Remove whitespace when searching in string
        custom_name: Search for a custom name
        '''
        
        try:
            if path:
                self.path = path
                self.remove_whitespace = rm_ws
                self.custom_name = custom_name

                if s_folder:
                    self.shows_folder = s_folder
                    
                # load data from config file
                with open('config.json') as file:
                    data = json.loads(file.read())
                    self.extensions = data['Extensions']
                    self.shows = data['Shows']
                
            else:
                print("Path or config_path are invalid")
        except Exception as err:
            print("Error in categorizer.init: %s" % err)


    # get basic info on all files given a directory through ctor
    def files_info(self):
        '''
        Function that returns all files from self.path that is initialized in the ctor, it returns the root folder,
        file name, extension of file, full path of file and also if it's a file placed inside the root folder.
        '''
        
        # filter out invalid extensions from a set of files
        filtr = lambda files, ext: fnmatch.filter(files, ext)

        # yield the directories when requested
        for root, subdir, files in os.walk(self.path):
            for ext in self.extensions:
                for file in filtr(files, ext):
                    yield (root, file, ext[1:], os.path.join(root, file), os.path.split(root)[1] == self.path)



    # private function that returns season/episode info from an input(could be directory and/or filename) - it's a bit ugly and could be refactored but enough for now
    def __show_meta__(self, file_name, directory_name=None, ext=None):
        '''
        Extract season/episode info from a file name or directory name
        '''
        # lower everything since all our regex depends on lowercase characters
        file, directory, season, episode = file_name.lower(), directory_name.lower() if directory_name else None, None, None
        file = "".join(file.split())

        # first check for double eps (S00E00-E00)
        match = re.search('s\d{1,2}e\d{1,2}.e\d{1,2}', file)
        if match:
            match = match.group().replace('-', '').split('e')
            season, episode = match[0].replace('s', ''), "{0}-{1}".format(match[1], match[2])
            season = season[1] if season.startswith("0") else season
            if season and episode:
                return (season, episode)

        # else check for s00e00, .000. or 00x00
        match = re.search('((s|.)\d{1,2}e\d{1,2})|(\.\d{3}\.)|(\d{1,2}x\d{2})', file)

        # found our match in the filename
        if match:
            # remove non-numeric
            match = "".join([m for m in match.group() if m.isdigit()])
            season, episode = match[:-2] if not match.startswith("0") else match[1], match[-2:]


        # no match, try to find season from directory name
        elif directory:
            sm, em = re.search('(season \d{1,2})', directory), re.search('\d{1,2}(\.| |\.%s)' % os.path.splitext(file_name)[1], file_name)

            if sm:
                season = "".join([x for x in sm.group() if x.isdigit()])
            if em:
                episode = "".join(em.group().split())

        # some shows are in the form 000.avi(and nothing else), so we want to make sure we get those(should be refactored to the other .000. regex check)
        elif ext:
            match = re.search('(\d{3}%s)' % ext, file_name)
            if match:
                match = match.group().replace(ext, "")
                season, episode = match[0], match[-2:]
            
        return (season, episode)


    # the data we use to create our target files/folders(only specific for shows)
    def data_shows(self):
        '''
        This function returns all our shows with matches depending on inputted parameters in ctor
        This function uses __show_meta__ and files_info to iterate the files and get the appropriate season/ep info
        '''
        # user can send in custom key/values to get shows from
        key_values = {(x, y) for x in self.shows.keys() for y in self.shows[x]}
        
        output = list()

        # user is looking for a custom name
        if self.custom_name:
            key_values = set()
            
            # get correct key
            for x in self.custom_name.split(","):
                x = x.strip()
                key = "".join([k for k, value in self.shows.items() if x in value])
                
                # create a tuple with a key(if we couldn't find any key in config.json and differential values
                if not key:
                    key = x.capitalize()

                # create some key values to search
                if key in self.shows.keys():
                    for f in [x for x in self.shows[key]]:
                        v = (key, f)
                        if v not in key_values:
                            key_values.add(v)
                else:
                    v = (key, x)
                    
                key_values.add(v)

        
        # iterate the files we found that have a valid extension and are listed in our config
        for m in self.files_info():
            (root_folder, file_name, file_ext, full_path, is_root) = m

            for key, value in key_values:
                # find through file name
                if find(value, file_name.lower() if not self.remove_whitespace else "".join(file_name.split())):
                    
                    # try to get season/episode info
                    (s, e) = self.__show_meta__(file_name, ext=file_ext)
                    
                    if s and e:
                        # new paths
                        season_path = os.path.join(self.shows_folder, key, "Season {0}".format(s)) # our path to our season
                        episode_path = os.path.join(season_path, "Episode {0}{1}".format(e, file_ext))

                        output.append((season_path, episode_path, full_path, is_root))

                # find through folder name
                elif find(value, root_folder.lower() if not self.remove_whitespace else "".join(root_folder.split())) :
                    (s, e) = self.__show_meta__(file_name, directory_name=root_folder)
                    
                    # we got the season/episode name from the folder name
                    if s and e:
                        season_path = os.path.join(self.shows_folder, key, "Season {0}".format(s)) # our path to our season
                        episode_path = os.path.join(season_path, "Episode {0}{1}".format(e, file_ext))
                        
                        output.append((season_path, episode_path, full_path, is_root))
                    else:
                        
                        # try to get season name(can't get episode name so we just place it in an appropriate folder without changing the name of the file
                        ((season, _), new_folder_path) = self.__show_meta__('', directory_name=full_path), os.path.join(self.shows_folder, key)

                        # we can extract season
                        if season:
                            new_folder_path = os.path.join(new_folder_path, "Season {0}".format(season))
                            new_file_path = os.path.join(new_folder_path, file_name)

                        # couldn't extract season, so we just use the folder name it's in, since we know it's not a root folder
                        elif not is_root:
                            new_folder_path = os.path.join(new_folder_path, os.path.basename(os.path.split(full_path)[0]))
                            new_file_path = os.path.join(new_folder_path, file_name)

                        # it's not a root folder, so we just place it in the show folder, but not with any season(i.e. in the root of the appropriate show)
                        else:
                            new_file_path = os.path.join(new_folder_path, file_name)
                        
                        output.append((new_folder_path, new_file_path, full_path, is_root))

        return set(output)


    
    def count_files(self, path):
        '''
        Counts all files with our legal extensions in a given directory
        '''
        c = 0
        for root, dir, files in os.walk(path):
            for ext in self.extensions:
                for file in fnmatch.filter(files, ext):
                    c += 1
        return c


    # create appropriate files/folders and try to delete files if there are no shows in them
    def create(self, data, delete_if_exists=True):
        '''
        Function that takes in a 3-way tuple of: Path, path of file and old path of file and if it's root directory
        If it's a root directory we don't delete the file(since that can delete the whole downloads folder)
        It creates a directory for the path, copies the file and delete the old path if the parameter 'delete_old_paths' is True
        '''
        try:
            for d in data:
                (path, file, old_path, is_root) = d
                
                # create directory if it doesn't exist
                create_dir(path)
                
                # copy file, remove if it already exists
                if not copy_file(old_path, file):
                    print("Couldn't copy file {0}, it already exists!".format(file))

            if delete_if_exists:
                for p in data:
                    path, is_root = os.path.split(p[2])[0], p[3]
                    
                    # if path contains no files and is not root download folder, we delete it
                    if self.count_files(path) == 0 and not is_root:
                        shutil.rmtree(path, ignore_errors=True)
            
        except Exception as err:
            print("Error in categorizer.create: %s" % err)




