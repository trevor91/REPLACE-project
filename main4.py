from tot import TopicsOverTime
import numpy as np
import pickle

def main():
	datapath = './Data/'
	resultspath = './results/'
	documents_path = datapath + 'titles.txt'
	timestamps_path = datapath + 'times.txt'
	stopwords_path = datapath + 'stopwords.txt'
	tot_topic_vectors_path = resultspath + 'tot_topic_vectors.csv'
	tot_topic_mixtures_path = resultspath + 'tot_topic_mixtures.csv'
	tot_topic_shapes_path = resultspath + 'tot_topic_shapes.csv'
	tot_pickle_path = resultspath + 'tot.pickle'

	tot = TopicsOverTime()
	documents, timestamps, dictionary = tot.GetPnasCorpusAndDictionary(documents_path, timestamps_path, stopwords_path)
	par = tot.InitializeParameters(documents, timestamps, dictionary)
	theta, phi, psi = tot.TopicsOverTimeGibbsSampling(par)
	np.savetxt(tot_topic_vectors_path, phi, delimiter=',')
	np.savetxt(tot_topic_mixtures_path, theta, delimiter=',')
	np.savetxt(tot_topic_shapes_path, psi, delimiter=',')
	tot_pickle = open(tot_pickle_path, 'wb')
	pickle.dump(par, tot_pickle)
	tot_pickle.close()

if __name__ == "__main__":
    main()
