<h1>
Download folder categorizer
</h1>
Olafur Johannsson - olafurjoh@ru.is

<hr />
<h2>
Description:
</h2>

<p>
By default this script searches through folders and files to try and extract the season/episode info from it(since some shows only have <em>000.avi</em> in them)

You can run the script without any parameters except the <em>-p</em>, which specifies the folder in which the downloaded files are.

You can also skip reading from the config file and send in <em>-n</em> argument followed by a string to search for a specific value(supports comma separated values, ex: <em>top gear, top.gear</em>)
</p>

<p>
It reads all valid extensions from the 'config.json'(.avi, .mp4, etc)
</p>

<p>
When you send in the <em>-n</em> argument, it will try and get the key from <em>config.json</em>(<em>top.gear</em> and <em>top gear</em> has key <em>Top Gear</em>), if it doesn't find a key, 
it will create a key as <em>Top.gear</em> (the <em>-n</em> arg capitalized)
</p>

<p>
For more fine-grained results you can strip whitespace from string before searching, using <em>-rw</em>, for example if you want to search for "house", but don't want any "house of cards" results
</p>
You can let the script try and delete all directories that were moved that don't have any shows in them any more using <em>-d</em>
<p>
<strong>
After running the script, you are prompted to view the results, after viewing the results you are prompted again asking if you want to edit any of the
results, removing any values you deem necessary, using comma-separated indices.(i.e. you got some values you were not expecting)
</strong>
</p>

<p>
<strong>
NOTE: When viewing results, first we show the index, then the old path, then the path where the show would go after accepting the results.
</strong>
</p>
<hr />
<h2>
Usage:
</h2>
<p>
	cleanup.py [-h] [-p PATH] [-s SHOWS_FOLDER] [-n NAME] [-rw] [-d]
</p>

EXAMPLES:
	note: (examples are all relative the the downloaded folder Hjaltmaster gave us)
	<dl>
	
	<dt>
	Running default using <em>config.json</em>:
	</dt>
	<dd>
	python cleanup.py -p "downloads"
</dd>
<br />

<dt>
	Searching for a specific value
	</dt>
	<dd>
	python cleanup.py -p "downloads" -n "klovn"
</dd>
<br />

<dt>
	Searching for a specific comma separated value
	</dt>
	<dd>
	python cleanup.py -p "downloads" -n "desperate housewives, dexter"
</dd>
<br />

<dt>
 Searching for a string and specifying a custom shows folder, <em>TV Shows</em>
</dt>
<dd>
python cleanup.py -p "downloads" -s "TV Shows" -n "the big bang theory" <br />
</dd>
<br />

	<dt>
	Searching for a specific string and stripping whitespace(since <em>house</em> can return <em>house of cards</em>):
	</dt>
	<dd>
	
	python cleanup.py -p "downloads" -n "house" -rw
</dd>
	<br />
	
	
	<dt>
	Searching for a specific string and deleting all modern family directores if they have no files(.avi, .mp4, .mkv, etc) in the folder left:
	</dt>
	<dd>
	python cleanup.py -p "downloads" -n "modern family" -d
	<br><strong>This can add the ovearhead of a few seconds because it has to go through each folder iteratively to check if it contains no tv shows before deleting</strong>
	</dd>
	<br />
	<dt>
	Searching for comma separated values that are present in <em>config.json</em>
	</dt>
	
	<dd>
	python cleanup.py -p "downloads" -n <em>top gear, top.gear, top_gear</em><br /> 
	<strong>Warning: Sending in comma-separated values such as "dragons.den, dragons_den" will create a folder Dragons.den and Dragons_den, since they are not specified in <em>config.json</em> - but for <em>Top Gear</em>, only one folder 
	will be created because it extracts they key from the values(where top_gear, top.gear, top gear are the values, and <em>Top Gear</em> is key)</strong>
</dd>
<br />
	
	</dl>
	
	<hr />
	
	<h2>
	Arguments:
</h2>
  
  <ul>
  <li>
  -p PATH, --path PATH  The path of the downloads folder(i.e. "C:\Users\User\Downloads")

  </li>
  <li>
  -s SHOWS_FOLDER, --shows_folder SHOWS_FOLDER
                        The path to put all the TV shows in(i.e. "E:\Shows"

  </li>
  <li>
  -n NAME, --name NAME  Send in if you only want to look for a specific string, i.e "dexter", or "top gear, top.gear" (it supports comma separated values)
  
</li>
  <li>
  -rw, --rm_ws          Removes whitespace from string, can be useful when you want to search for "house" 
			and not get any results from "House of Cards", since some House episode are in the format of "House.S03" or "House S03"
			then the regex check cannot differentiate between those values
</li>			

			<li>
  -d, --delete          Try to delete the directories we moved if they have no shows left
</li>
</ul>
<hr />
<h2>
Packages:
</h2>
<ul>
<li>
	util.py: Reusable utility functions
</li>
	<li>
	categorizer.py: The class that handles all the moving/creating/searching of shows
	</li>
	<li>
	cleanup.py: The script that takes in parameters and prompts the user
	</li>
	</ul>
	
<hr />
<h2>
External dependancies:
</h2>
<p>
	colorama: https://pypi.python.org/pypi/colorama
</p>
