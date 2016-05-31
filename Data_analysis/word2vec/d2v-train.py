#!/usr/bin/env python3

import os, argparse, logging
# get cpu cores
import multiprocessing
# word segmentation
import jieba
# doc2vec
from gensim.models import Doc2Vec
from gensim.models.doc2vec import LabeledSentence
from gensim import utils
# array storage
import numpy
# random
from random import shuffle
# save model information
import pickle

logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s')

class LabeledLineSentence(object) :
    def __init__(self, file_list, logger=None, addlabel=True) :
        self.file_list = file_list
        self.sentences = []
        self.logger = logger
        self.addlabel = addlabel

    def __iter__(self) :

        for file_path in self.file_list :
            dic = eval(open(file_path, 'r').read())
            with open("/tmp2/b03902035/" + file_path[:3] + "_keylens.txt", "w") as fw:
                for key in dic.keys():
                    fw.write(key + ';' + str(len(dic[key]['msgs'])) + '\n')
            
            for i, key in enumerate(dic.keys()):
                if self.logger :
                    self.logger.info('parsing No.{:d}, key: {:s}'.format(i, key))
                key_idx = 0
                for msg in dic[key]['msgs']:
                    label = [key, '{:s}_{:d}'.format(key, key_idx), msg[1]]
                    if isinstance(msg[2], str) and len(msg[2]) > 0:
                        text = [w for w in jieba.cut(msg[2], cut_all=False) if w != ' ']           
                    else:
                        continue

                    key_idx += 1
                    yield LabeledSentence(words=text, tags=label)

    def to_array(self) :
        # wipe out the old data
        self.sentences = []

        if self.logger :
            self.logger.debug('calling internal iterator')
        for labeled_sent in self.__iter__() :
            self.sentences.append(labeled_sent)

        if self.logger :
            self.logger.debug('return a list of length {:d} as result'.format(len(self.sentences)))

        return self.sentences

    def sentences_perm(self) :
        shuffle(self.sentences)
        return self.sentences

    def get_sent_cnt(self) :
        return self.sent_cnt

def is_valid_infile(file_path, target_ext='.pro', logger=None) :
    ext = os.path.splitext(file_path)[-1].lower()
    if ext != '.pro' :
        if logger :
            logger.warning(file_path + ' is not ' + target_ext + ' file, IGNORED')
        return False
    else :
        return True

def get_args() :
    parser = argparse.ArgumentParser(description='Train the doc2vec model using pre-processed data.')
    parser.add_argument('--algo', '-a', dest='algo',
                        default='dbow',
                        help='training algorithm, DM (default) or DBOW')
    parser.add_argument('--dim', '-d', dest='dim', type=int,
                        default=400,
                        help='dimension of the feature vector')
    parser.add_argument('--mincount', '-m', dest='minc', type=int,
                        default=1,
                        help='min count of words, default to 1')
    parser.add_argument('--window', '-w', dest='window', type=int,
                        default=8,
                        help='max distance between the predicted word and context words within a doc')
    parser.add_argument('--sample', '-s', dest='sample', type=float,
                        default=1e-5,
                        help='sampling threshold, default to 1e-5')
    parser.add_argument('--workers', dest='n_workers', type=int,
                        default=multiprocessing.cpu_count(),
                        help='number of worker thread, default to all the cores')
    parser.add_argument('--epoch', '-e', dest='epochs', type=int,
                        default=30,
                        help='number of epoch trained')
    parser.add_argument('--addlabel', dest='addlabel', action='store_const',
                        const=True, default=False,
                        help='boolean for adding additional training label')
    parser.add_argument('--decay', dest='decay', action='store_const',
                        const=True, default=False,
                        help='boolean for decay learning rate over each epoch')
    parser.add_argument('--outdir', '-o', dest='out_dir',
                        default='/tmp2/b03902035',
                        help='destination directory for the model file')
    parser.add_argument('--verbose', '-v', dest='verbose',
                        action='count', default=0,
                        help='control the display level of output logs')
    parser.add_argument('in_file', nargs='+',
                        help='file to perform the training')

    return parser.parse_args()

if __name__ == '__main__' :
    # parse the command line arguments
    args = get_args()
    # get the logger object
    logger = logging.getLogger()
    # set the log level
    if args.verbose >= 2 :
        logger.setLevel(logging.DEBUG)
    elif args.verbose >= 1 :
        logger.setLevel(logging.INFO)
    else :
        logger.setLevel(logging.WARNING)

    # verify all the files are valid
    '''
    args.in_file[:] = [file_path for file_path in args.in_file
                       if is_valid_infile(file_path, logger=logger)]
    '''
    logger.info('loading data from {:d} files'.format(len(args.in_file)))
    for i, file_path in enumerate(args.in_file) :
        logger.info(' File {:d}, {:s}'.format(i+1, file_path))

    jieba.set_dictionary('dict.txt.big')
    jieba.load_userdict('userDict.txt')
    sentences = LabeledLineSentence(args.in_file, logger=logger, addlabel=args.addlabel)

    if args.algo == 'dm' :
        dm = 1
    elif args.algo == 'dbow' :
        dm = 0
    else :
        logger.error('invalid training algorithm "{:s}"'.format(args.algo))

    # build the vocabulary table

    if args.decay:
        alpha=0.002 + 0.001 * args.epochs
        min_alpha=alpha
    else:
        alpha=0.025
        min_alpha=0.0001
    model = Doc2Vec(min_count=args.minc,
                    dm=dm,
                    size=args.dim,
                    window=args.window,
                    sample=args.sample,
                    workers=args.n_workers,
                    alpha=alpha,
                    min_alpha=min_alpha)
    logger.info('start building the vocabulary')
    model.build_vocab(sentences.to_array())

    logger.info('begin doc2vec training')
    for epoch in range(args.epochs) :
        logger.info('... epoch {:d}, alpha = {:s}'.format(epoch, str(model.alpha)))
        model.train(sentences.sentences_perm())
        if args.decay:
            model.alpha -= 0.001
            model.min_alpha = model.alpha

    # save the model
    '''
    new_filename = '{:s}-d{:d}-m{:d}-w{:d}-e{:d}-s{:f}'.format(args.algo, args.dim, args.minc, args.window, args.epochs, args.sample)
    if args.decay:
        new_filename = new_filename + '-decay'
    if args.addlabel:
        new_filename = new_filename + '-label'
    '''
    new_filename = 'd2v-' + args.in_file[0][:3]
    if dm == 0:
        new_filename += '-dm'
    else:
        new_filename += '-dbow'
    new_filepath = os.path.join(args.out_dir, new_filename)
    model.save(new_filepath + '.mod')
    logger.info('model saved to {:s}.mod (.mif contains the info)'.format(new_filepath))

    # save relevant informations
    with open(new_filepath + '.mif', 'wb') as out_file :
        # the .pro used to train the doc2vec model
        pickle.dump(args.in_file, out_file)
        # the sentences
        pickle.dump(sentences.get_sent_cnt(), out_file)
        # the dimension of the model
        pickle.dump(args.dim, out_file)
