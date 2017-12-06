#import files we need
import ConfigParser, os, settings, cgi
import xml.etree.ElementTree as ET


### METADATA ###

#populate gamelist
gamelist =[]
def build_gamelist():
    current_md_romspath = get_config('metadata')['md_romspath']
    current_md_xmlpath = get_config('metadata')['md_xmlpath']
    global gamelist
    try:
		gamelist = get_gamelist(current_md_romspath, current_md_xmlpath)
    except:
		gamelist = []
		print('no games found')
    return gamelist


#build gamelist
def get_gamelist( roms_path, xml_path ):
    roms_path = roms_path
    xml_path = xml_path
    all_roms = []
    output = '\nStart building gamelist from systems:\n\n'
    try:
        system_folders = walk_dir( roms_path ) #get system folders
        try:
            for system in system_folders:
                system_roms = list_files( system, roms_path ) #check for files in system folder
                num_roms = len(system_roms) #check how many files found for this system
                output += system + '(' + str(num_roms) + ')\n'
                try:
                    get_tags_from_xml = parse_xml( roms_path+ "/" +system+ "/gamelist.xml", system ) #check for xml file and return all game tags
                    #print('xml found \n')
                except:
                    get_tags_from_xml = ''
                    #print('no xml found \n')
                try:
                    if len(system_roms) > 0:
                        for rom in system_roms:
                            no_match = {'xml_system': system, 'xml_row': '', 'tag_id': '', 'tag_source': '', 'tag_path': './' +rom, 'tag_xml': False, 'tag_name': '', 'tag_desc': '', 'tag_rating': '', 'tag_releasedate': '', 'tag_developer': '', 'tag_publisher': '', 'tag_genre': '', 'tag_players': '', 'tag_image': '', 'tag_video': ''}
                            match = next((item for item in get_tags_from_xml if item['tag_path'][2:] == rom), no_match) #check if file is in xml, else give basic tag info
                            all_roms.append(match) #append file in array
                except:
                    print('something went wrong with building romlist')
        except:
            print('no roms found')
    except:
        print('no system folders found')
    total_games_found = len(all_roms) #count total games found
    output += '\nFound '+ str(total_games_found) +' games\n'
    print( output )
    return all_roms



#get list of all folders in roms path
def walk_dir( path ):
    dirList = []
    dirList = os.listdir( path )
    newdirlist = []
    for d in dirList:
        d_path = path+"/"+d
        try:
            if os.path.islink(d_path) == False: #remove symlinks (i.e. Genesis is symlink and will give doubles)
                newdirlist.append(d)
        except:
            pass
    return sorted(newdirlist)

#get extensions from system
class get_ext(object):
    def __init__(self):
        self.types = settings.extensions

    def __call__(self, file_type):
        return self.types.get(file_type, [])
get_ext = get_ext()

#get gamefiles from system
def list_files( system, romspath ):
    allFiles = []
    extensions = get_ext( system )
    if os.path.isdir(romspath + "/" + system):
        for root, dirs, files in os.walk(romspath + "/" + system):
            for file in files:
                for ext in extensions:
                    if file.endswith('.'+ext):
                        #allFiles.append(cgi.escape(file))
                        allFiles.append(file)
            return sorted(allFiles)
    else:
        return False


#parse xml file
def parse_xml(xml_filename, system):
    tree = ET.parse(xml_filename)
    root = tree.getroot()
    allGameTags = []
    i = 0
    for game in root.findall('game'):
        i += 1
        gameTags = {}
        gameTags['xml_system'] = system
        gameTags['xml_row'] = i
        if game.get('id') != None: gameTags['tag_id'] = game.get('id')
        if game.get('source') != None: gameTags['tag_source'] = game.get('source')
        if game.find('path') != None:
            gameTags['tag_path'] = game.find('path').text
            gameTags['tag_xml'] = True
        if game.find('name') != None: gameTags['tag_name'] = game.find('name').text
        if game.find('desc') != None: gameTags['tag_desc'] = game.find('desc').text
        if game.find('rating') != None: gameTags['tag_rating'] = game.find('rating').text
        if game.find('releasedate') != None: gameTags['tag_releasedate'] = game.find('releasedate').text
        if game.find('developer') != None: gameTags['tag_developer'] = game.find('developer').text
        if game.find('publisher') != None: gameTags['tag_publisher'] = game.find('publisher').text
        if game.find('genre') != None: gameTags['tag_genre'] = game.find('genre').text
        if game.find('players') != None: gameTags['tag_players'] = game.find('players').text
        if game.find('image') != None: gameTags['tag_image'] = game.find('image').text
        if game.find('video') != None: gameTags['tag_video'] = game.find('video').text
        allGameTags.append(gameTags)
    return allGameTags


def write_xml ( system, game_tags):
    current_md_romspath = get_config('metadata')['md_romspath']
    current_md_xmlpath = get_config('metadata')['md_xmlpath']

    xml_filename = current_md_xmlpath+"/"+system+"/gamelist.xml"
    tree = ET.parse(xml_filename)
    root = tree.getroot()
    for game in root.findall('game'):
        if game.find('path').text == game_tags['tag_path']:
            if game.find('name') != None: game.find('name').text = (game_tags['tag_name'])
            if game.find('rating') != None: game.find('rating').text = (game_tags['tag_rating'])
            if game.find('releasedate') != None: game.find('releasedate').text = (game_tags['tag_releasedate'])
            if game.find('developer') != None: game.find('developer').text = (game_tags['tag_developer'])
            if game.find('publisher') != None: game.find('publisher').text = (game_tags['tag_publisher'])
            if game.find('genre') != None: game.find('genre').text = (game_tags['tag_genre'])
            if game.find('players') != None: game.find('players').text = (game_tags['tag_players'])
            if game.find('desc') != None: game.find('desc').text = (game_tags['tag_desc'])
            try:
                tree.write(xml_filename)
                print('\n----> xml updated')
                build_gamelist()
                print('----> refresh gamelist done\n')
            except:
                print('error: could not write '+game_tags['tag_name']+' to xml')



    return

### SETTINGS ###

#get options from config file
def get_config(section):
    config_file = settings.config_file
    Config = ConfigParser.RawConfigParser()
    Config.read(config_file)
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1


def write_config(options):
    config_file = settings.config_file
    Config = ConfigParser.RawConfigParser()
    Config.add_section('server')
    Config.add_section('metadata')
    print("open file '"+ config_file +"'")
    print("write lines:")
    for option in options:
        try:
            Config.set(option['section'], option['name'], option['value'])
            print("in section '"+option['section'] +"' -> "+ option['name'] +" = " +option['value'])
        except:
            pass
    with open(config_file, 'wb') as configfile:
        Config.write(configfile)
        configfile.close()
