#import files we need
from flask import Flask, render_template, request, send_from_directory
import functions, settings, scrape_tgdb
from datetime import datetime

app = Flask(__name__)

# get path for files
current_md_romspath = functions.get_config('metadata')['md_romspath']
current_md_xmlpath = functions.get_config('metadata')['md_xmlpath']

#build gamelist at start
functions.build_gamelist()

#refresh gamelist
def update_gamelist():
	global gamelist
	from functions import gamelist




###setup url routes###
@app.route('/metadata', methods=['GET'])
def data():
	update_gamelist()
	get_system = request.args.get('system') if request.args.get('system') else None
	get_game = int(request.args.get('game')) if request.args.get('game') else None
	error = ''
	gamefiles = []
	gameinfo = []
	d = ''
	g = ''
	try:
		systemfolders = functions.walk_dir(current_md_romspath)
		system_array = []
		for item in systemfolders:
			files = functions.list_files( item, current_md_romspath )
			num_files = len(files)
			system_array.append({'name': item, 'num_files': num_files})
	except:
		error = 'could not find romspath in config file, either wrong config file or wrong value!'
	try:
		for game in gamelist:
			if game['xml_system'] == get_system:
				gamefiles.append(game)
	except:
		print('something went wrong with building gamelist')
	if get_game != None:
		try:
			gameinfo = next((g for g in gamelist if g['xml_row'] == get_game and g['xml_system'] == get_system), None)
			d = gameinfo['tag_releasedate']
			try:
				if len(d) > 10:
					t = datetime.strptime(d, "%Y%m%dT%H%M%S")
					gameinfo['tag_releasedate'] = t.strftime("%Y-%m-%d")
				else:
					pass
			except:
				print('something wrong with datetime?')
		except:
			error = 'somthing went wrong with getting game info'

	return render_template(
	'data.html',
	title='Afterscrape - Metadata',
	shorttitle='data',
	error=error,
	get_system=get_system,
	get_game=get_game,
	system_array=system_array,
	gamefiles=gamefiles,
	gameinfo=gameinfo
	)

#home
@app.route('/')
def index():
	return render_template('index.html', title='Afterscrape', shorttitle='home')


#get image/video source
@app.route('/images/<imagepath>', methods=['GET'])
def get_image(imagepath):
	system = request.args.get('system')
    	return send_from_directory(current_md_romspath+"/"+system+"/images/", imagepath)

#edit game
@app.route('/edit', methods=['GET'])
def edit_game():
	update_gamelist()
	get_game = int(request.args.get('game')) if request.args.get('game') else None
	get_system = request.args.get('system') if request.args.get('system') else None
	gameinfo = ''
	if get_game != None:
		try:
			gameinfo = next((item for item in gamelist if item['xml_row'] == get_game and item['xml_system'] == get_system), None)
			d = gameinfo['tag_releasedate']
			if len(d) > 8:
				d = datetime.strptime(d, "%Y%m%dT%H%M%S")
				gameinfo['tag_releasedate'] = d.strftime("%Y-%m-%d")
		except:
			error = 'somthing went wrong with getting game info'


    	return render_template(
	'editgame.html',
	title='Afterscrape - Edit game',
	gameinfo=gameinfo
	)

#settings
@app.route('/settings')
def settings():
	#get current values from config file
	try:
		current_server_ip = functions.get_config('server')['server_ip']
	except:
		current_server_ip = ''
	try:
		current_server_port = int(functions.get_config('server')['server_port'])
	except:
		current_server_port = ''
	try:
		current_server_debug = functions.get_config('server')['server_debug']
	except:
		current_server_debug = ''
	try:
		current_server_threaded = functions.get_config('server')['server_threaded']
	except:
		current_server_threaded = ''
	try:
		current_md_romspath = functions.get_config('metadata')['md_romspath']
	except:
		current_md_romspath = ''
	try:
		current_md_xmlpath = functions.get_config('metadata')['md_xmlpath']
	except:
		current_md_xmlpath = ''
	try:
		current_md_imgpath = functions.get_config('metadata')['md_imgpath']
	except:
		current_md_imgpath = ''
	return render_template(
		'settings.html',
		title='Afterscrape - Settings',
		shorttitle='settings',
		current_server_ip=current_server_ip,
		current_server_port=current_server_port,
		current_server_debug=current_server_debug,
		current_server_threaded=current_server_threaded,
		current_md_romspath=current_md_romspath,
		current_md_xmlpath=current_md_xmlpath,
		current_md_imgpath=current_md_imgpath
	 )

@app.route('/form', methods=['GET', 'POST'])
def form():
	post_config_options = []
	post_config_options.append({'section': 'server', 'name': 'server_ip', 'value': request.form.get('post_server_ip', '0.0.0.0')})
	post_config_options.append({'section': 'server', 'name': 'server_port', 'value': request.form.get('post_server_port', '80')})
	post_config_options.append({'section': 'server', 'name': 'server_debug', 'value': request.form.get('post_server_debug', 'False')})
	post_config_options.append({'section': 'server', 'name': 'server_threaded', 'value': request.form.get('post_server_threaded', 'False')})
	post_config_options.append({'section': 'metadata', 'name': 'md_romspath', 'value': request.form.get('post_md_romspath', '/home/pi/RetroPie/roms')}) #fallback to default value not working. <input type="text"> returns value when empty?
	post_config_options.append({'section': 'metadata', 'name': 'md_xmlpath', 'value': request.form.get('post_md_xmlpath', '/home/pi/.emulationstation/gamelists')}) #fallback to default value not working. ^
	post_config_options.append({'section': 'metadata', 'name': 'md_imgpath', 'value': request.form.get('post_md_imgpath', '/home/pi/.emulationstation/downloaded_images')}) #fallback to default value not working. ^
	functions.write_config(post_config_options)
	return render_template('form.html')

@app.route('/form_editgame', methods=['GET', 'POST'])
def form_editgame():
	game_tags = request.form if request.form else None
	get_system = request.form.get('post_system') if request.form.get('post_system') else ''
	get_game = request.form.get('post_game') if request.form.get('post_game') else ''
	functions.write_xml( get_system, game_tags)
	return render_template('form_editgame.html', system=get_system, game=get_game)

@app.route('/scrape', methods=['GET'])
def scrape():
	platforms = scrape_tgdb.get_platforms()
	return render_template('scrape.html', platforms=platforms)

###start server###
if __name__ == '__main__':
	#set options
	server_ip = functions.get_config('server')['server_ip']
	server_port = int(functions.get_config('server')['server_port'])
	server_debug = functions.get_config('server')['server_debug']
	server_threaded = functions.get_config('server')['server_threaded']

	#run server
	app.run(host=server_ip, port=server_port, debug=server_debug,  threaded=server_threaded)
