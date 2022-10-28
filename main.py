import requests
from bs4 import BeautifulSoup
import json
import matplotlib as mlp
import matplotlib.pyplot as plt


def nums_cumulative_sum(num_list):
	return [sum(num_list[:i+1]) for i in range(len(num_list))]


def get_data():
	base_url = 'https://understat.com/match/'
	match = str(input("Match ID: "))
	url = base_url + match

	response = requests.get(url)
	soup = BeautifulSoup(response.content, 'lxml')
	scripts = soup.find_all('script')

	strings = scripts[1].string

	ind_start = strings.index("('") + 2
	ind_end = strings.index("')")

	json_data = strings[ind_start:ind_end]
	json_data = json_data.encode('utf8').decode('unicode_escape')
	return json.loads(json_data)


def get_xg(data):
	data_home = data['h']
	data_away = data['a']

	xg_data = {
		'h_xg': [0],
		'a_xg': [0],
		'h_min': [0],
		'a_min': [0],
		'h_team': data_home[0]['h_team'],
		'a_team': data_away[0]['a_team']
	}

	for shot_event in data_home:
		xg_data['h_xg'].append(float(shot_event['xG']))
		xg_data['h_min'].append(int(shot_event['minute']))

	for shot_event in data_away:
		xg_data['a_xg'].append(float(shot_event['xG']))
		xg_data['a_min'].append(int(shot_event['minute']))

	xg_data['h_cumulative'] = nums_cumulative_sum(xg_data['h_xg'])
	xg_data['a_cumulative'] = nums_cumulative_sum(xg_data['a_xg'])

	xg_data['h_min'].append(90)
	xg_data['a_min'].append(90)
	xg_data['h_cumulative'].append(xg_data['h_cumulative'][-1])
	xg_data['a_cumulative'].append(xg_data['a_cumulative'][-1])

	return xg_data


def create_flowchart(xg_data):
	fig, ax = plt.subplots(figsize=(10,5))
	fig.set_facecolor('#3D4849')
	ax.patch.set_facecolor('#3D4849')
	plt.xticks([15, 30, 45, 60, 75, 90])
	plt.xlabel('Minute')
	plt.xlabel('xG')

	ax.step(x=xg_data['h_min'], y=xg_data['h_cumulative'], label=xg_data['h_team'], linewidth=3)
	ax.step(x=xg_data['a_min'], y=xg_data['a_cumulative'], label=xg_data['a_team'], linewidth=3)
	legend = plt.legend(loc="upper left",)
	frame = legend.get_frame()
	frame.set_facecolor('#3D4849')
	frame.set_edgecolor('#3D4849')

	ax.set_ylim(ymin=0)
	ax.set_xlim(xmin=0, xmax=90)
	plt.show()

	# Show goals
	# Arrange colours (hmmm)
	# Thicken line


def main():
	data = get_data()
	xg_data = get_xg(data)
	create_flowchart(xg_data)


main()