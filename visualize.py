
import fileinput
import random
import scipy.special
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import scipy.stats
from scipy.stats import beta
import pprint, pickle

def VisualizeTopics(phi, words, num_topics, viz_threshold=9e-3):
	# fontPath = "/usr/share/fonts/truetype/nanum/NanumGothic.ttf"
	fontPath = "c:/Windows/Fonts/malgun.ttf"
	fontprop = fm.FontProperties(fname = fontPath, size = 12)
	
	phi_viz = np.transpose(phi)
	words_to_display = ~np.all(phi_viz <= viz_threshold, axis=1)
	words_viz = [words[i] for i in range(len(words_to_display)) if words_to_display[i]]
	phi_viz = phi_viz[words_to_display]
	fig, ax = plt.subplots()
	heatmap = plt.pcolor(phi_viz, cmap=plt.cm.Blues, alpha=0.8)
	plt.colorbar()

	#fig.set_size_inches(8, 11)
	ax.grid(False)
	ax.set_frame_on(False)

	ax.set_xticks(np.arange(phi_viz.shape[1]) + 0.5, minor=False)
	ax.set_yticks(np.arange(phi_viz.shape[0]) + 0.5, minor=False)
	ax.invert_yaxis()
	ax.xaxis.tick_top()
	#plt.xticks(rotation=45)
	
	for t in ax.xaxis.get_major_ticks():
	    t.tick1On = False
	    t.tick2On = False
	for t in ax.yaxis.get_major_ticks():
	    t.tick1On = False
	    t.tick2On = False

	column_labels = words_viz	#['Word ' + str(i) for i in range(1,1000)]
	row_labels = ['Topic ' + str(i) for i in range(1,num_topics+1)]
	ax.set_xticklabels(row_labels, minor=False, fontproperties = fontprop)
	ax.set_yticklabels(column_labels, minor=False, fontproperties = fontprop)

	plt.show()

def VisualizeEvolution(psi):
	xs = np.linspace(0, 1, num=1000)
	fig, ax = plt.subplots()

	for i in range(len(psi)):
		ys = [math.pow(1-x, psi[i][0]-1) * math.pow(x, psi[i][1]-1) / scipy.special.beta(psi[i][0],psi[i][1]) for x in xs]
		ax.plot(xs, ys, label='Topic ' + str(i+1))

	ax.legend(loc='best', frameon=False)
	plt.show()

def main():
	resultspath = './results/'
	tot_pickle_path = resultspath + 'tot.pickle'

	tot_pickle = open(tot_pickle_path, 'rb')
	par = pickle.load(tot_pickle)
	VisualizeTopics(par['n'], par['word_token'], par['T'])
	VisualizeEvolution(par['psi'])

if __name__ == "__main__":
    main()
