import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict


def load_node(path):
	name_to_id, id_to_name = {}, []
	type_to_node, node_to_type = defaultdict(list), []
	# type_to_node, node_to_type = {}, []
	node_id, type_id = 0, 0
	with open(path) as f:
		for line in f:
			line = line.rstrip().split('\t')
			name_to_id[line[0]] = node_id
			id_to_name.append(line[0])

			try:
				type_to_node[line[1]].append(node_id)
			except IndexError:
				print "error"

			node_to_type.append(line[1])
			node_id += 1
	type_to_node_copy = {}
	for type, ids in type_to_node.items():
		type_to_node_copy[type] = np.array(ids)

	type_id = 0
	type_to_id, id_to_type = {}, []
	for id, t in enumerate(type_to_node.keys()):
		type_to_id[t] = id
		id_to_type.append(t)
		type_id += 1
	return id_to_name, name_to_id, node_to_type, type_to_node_copy, id_to_type, type_to_id


def load_feature(path):
	feature = {}
	dim = -1
	with open(path) as f:
		for line in f:
			line = line.rstrip().split(',', 1)
			vector = list(map(float, line[1].split(',')))
			dim = len(vector)
			feature[line[0]] = np.array(vector)
	return feature, dim


def load_groups(paths):
	groups = []
	for path in paths:
		group = set()
		with open(path) as f:
			for line in f:
				group.add(line.rstrip())
		groups.append(group)
	return groups


def plot(data, plot_file):
	plt.figure()
	plt.plot(range(len(data)), data)
	plt.savefig(plot_file)
	plt.close()


def load_movie_genre(movie_path, genre_paths, genre_name_path):
	genres = {}
	with open(genre_name_path) as f:
		for line in f:
			line = line.rstrip().split()
			genres[line[0]] = line[1]

	id_to_movie, movie_to_id = {}, {}
	with open(movie_path) as f:
		for line in f:
			line = line.rstrip().split('\t')
			movie = '_'.join(line[1].split()[:-1])
			id_to_movie['m' + line[0]] = movie
			movie_to_id[movie] = 'm' + line[0]

	id_to_genre = defaultdict(list)
	for genre_path in genre_paths:
		genre = genres[genre_path.split('/')[-1].split('.')[0].split('_')[1]]
		with open(genre_path) as f:
			for line in f:
				id_to_genre[line.rstrip()].append(genre)

	return id_to_movie, movie_to_id, id_to_genre
