import os
import pickle


def read_and_save_tfrec_path(config, rootdir, filename_tfrec_pickle=None, dataset='0'):
    """
    Read all paths of tfrecords and save into the pickle files
    :param rootdir: type str: rootdir of saving tfrecords dataset
    :param filename_tfrec_pickle: type str: Filename of pickle which stores the paths of all tfrecords files.

    :return:
    """
    dirs = os.listdir(rootdir)
    if dirs==[]:
        print('Failed saving tfrecords files: No directories in the tfrecords rootdir!')
        return None
    lst_image = []
    lst_label = []
    if config['read_body_identification']:
        dir_patterns = {'images': '/*/image', 'labels': '/*/label_bi'}
        filename_tfrec_pickle=filename_tfrec_pickle+'_bi'
    else:
        dir_patterns = {'images': '/*/image', 'labels': '/*/label'}
    for d in dirs:
        dir_label = rootdir + dir_patterns['labels'].replace('*', d)
        dir_image = rootdir + dir_patterns['images'].replace('*', d)
        if not os.path.exists(dir_label) or not os.path.exists(dir_image):
            print(d, ' is not found in label dir or in image dir of tfrecords,this dataset is abandoned.')
            continue

        lst_image.append([dir_image + '/' + filename_image for filename_image in os.listdir(dir_image)])
        lst_label.append([dir_label + '/' + filename_label for filename_label in os.listdir(dir_label)])
    dictionary = {'image': lst_image, 'label': lst_label}
    if not os.path.exists(config['dir_list_tfrecord']):os.makedirs(config['dir_list_tfrecord'])

    pickle_filename = config['dir_list_tfrecord'] + '/' + filename_tfrec_pickle + '.pickle'
    if os.path.exists(pickle_filename):
        old_dict = pickle.load(open(pickle_filename, 'rb'))
        dictionary = {**old_dict, **dictionary}
    pickle.dump(dictionary, open( pickle_filename, 'wb'), protocol=pickle.HIGHEST_PROTOCOL)

