from __future__ import division
from nltk.util import everygrams
from collections import Counter


def fb_file_to_dict(filename):
    """ read in data """
    print 'converting %s to dict ...' % filename
    s = ''
    with open(filename, 'r') as f:
        for line in f:
            s += line
    print 'done.'
    return eval(s)


def build_one_chat_LM(fb_dict, max_len=3):
    """
        input: one chat room
        output: LM of that chatroom
    """
    for line in fb_dict['msgs']:
        line = line[2]
        grams_this_line = list(everygrams(line,
                                          max_len=max_len,
                                          pad_left=True,
                                          pad_right=True,
                                          left_pad_symbol='<s>',
                                          right_pad_symbol='<\s>'))

        Counter_LM = Counter(grams_this_line)
        total_count = sum(Counter_LM.values())
        total_count = float(total_count)
        for key in Counter_LM:
            Counter_LM[key] /= total_count

        return Counter_LM


def build_all_chat_LM(fb_dict, max_len=3):
    """
        input: fb_dict of all chat rooms
        output: LM corresponding to each chat room
    """
    all_LMs = {}
    count = 1
    total = len(fb_dict)
    for chatname, chatroom in fb_dict.iteritems():
        print '(%d/%d)building LM ...' % (count, total)
        all_LMs[chatname] = build_one_chat_LM(chatroom, max_len=max_len)
        count += 1

    return all_LMs


def build_vocab(all_LMs):
    print 'building vocabulary ...'
    vocab = set()
    for LM in all_LMs:
        for word in LM.iterkeys():
            vocab.add(word)

    print 'vocab size: %d' % len(vocab)
    return vocab

# def vectorize_LMs(all_LMs, vocab):
#   vectorized_result = {}
#   vocab_size = len(vocab)
#   for chatname, LM in all_LMs.iteritems():
#       tmp = np.zeros(vocab_size)


def inner_product(v1, v2):
    ret = 0.0
    for word, value in v1.iteritems():
        if word in v2:
            ret += value * v2[word]
    return ret


def similar_chat(all_LMs, target_name, you, show_top=10, alter=None):
    if alter is not None:
        base = alter
    else:
        base = '%s, %s' % (target_name, you)
        if base not in all_LMs:
            base = '%s, %s' % (you, target_name)
    if base not in all_LMs:
        print 'invalid input, you can try "all_LMs.keys()" to see which combinations available.'
        return []

    similarity = {}
    base_LM = all_LMs[base]
    for chatname, LM in all_LMs.iteritems():
        if chatname == base:
            continue
        similarity[chatname] = inner_product(base_LM, LM)

    sorted_LM = sorted(similarity, key=similarity.get, reverse=True)
    for i in xrange(show_top):
        print sorted_LM[i]

    return sorted_LM


def preparation(filename, max_len=4):
    fb_dict = fb_file_to_dict(filename)
    all_LMs = build_all_chat_LM(fb_dict, max_len=max_len)
    # vocab = build_vocab(all_LMs)
    return all_LMs
