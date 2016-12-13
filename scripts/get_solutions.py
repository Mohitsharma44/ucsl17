# ------
# Author: Mohit Sharma
# July 27, 2016
#
# pullsoln.py
#    Search for Solutions saved by the students in their
#    homedirectory under ucsl sub-directory and copy
#    to another location for TA to assess the solutions.
#
# -----

import os
import sys
import fnmatch
import csv
import time
from shutil import copy2 as copyfile

BASE_PATH   = '/home/cusp/'
# name of file for student's solutions
FILENAME    = "Challenge_1_Solutions.ipynb"
# csv file with student's first_name last_name and net_id
NET_ID_FILE = os.getenv("NETID_17")
# directory where solutions will be copied
TA_ID       = os.getenv("UCSL_TA")

def progress(count, total, status=''):
    """
    Fancy progress bar
    """
    bar_len    = 60
    filled_len = int(round(bar_len * count / float(total)))
    percents   = round(100.0 * count / float(total), 1)
    bar        = '=' * filled_len + '-' * (bar_len - filled_len)
    sys.stdout.write('\r [%s] %s%s ...%s' % (bar, percents, '%', status))
    sys.stdout.flush()
    
def find_solutions(student_net, pattern):
    """
    Search for solutions to challenges in
    the homedirectory/ucsl (see note) 
    subdirectory of students.

    Parameters
    ----------
    student_net : list
        List containing net id's of students
    pattern : str
        Pattern for filename to be matched

    Returns
    -------
    file_locations : dict
        Dictionary containing net id and 
        corresponding absolute path of
        the files matching the pattern

    .. note:: Files are supposed to be in ucsl 
        subdirectory but due to some confusion
        regarding where the notebooks should be
        stored, I will recursively look for ipynb
        files inside their homedirs.
    """

    file_locations = {}
    prg = 1
    ## I should really find a better way!
    ## or move to Python 3.5+ and use iglob
    ## with ** 
    for net_id in student_net:
        for root, dirname, fnames in os.walk(os.path.join(BASE_PATH, net_id)):
            for fname in fnmatch.filter(fnames, pattern):
                file_locations.update({net_id: os.path.abspath(os.path.join(root, fname))})
                progress(prg, len(student_net), status=" Searching Solutions")
                prg += 1
                time.sleep(0.1)
    # since we don't know how many files can be there..
    progress(100, len(student_net), status=" Searching Solutions")
    print "\n\nTotal Solutions Found: ",len(file_locations)
    print "\t".join([x for x in file_locations.keys()])
    print '\n'
    return file_locations


def copy_solutions(files, destination):
    """
    Copy list of files with absolute path 
    to destination.
    If destination doesn't exist, it will
    be created

    Parameters
    ----------
    files: Dict
        Dictionary containing student net_id as key
        and absolute paths of the files to be copied
        as values
    destination: str
        destination directory where the files
        needs to be copied to

    Returns
    ------
    None

    """
    prg = 1
    if not os.path.exists(os.path.abspath(destination)):
        os.makedirs(os.path.abspath(destination))
    count = len(files)

    for net_id in files.keys():
        copyfile(files[net_id], os.path.join(destination, net_id+"_"+os.path.basename(files[net_id])))
        progress(prg, count, status=" Copying Files")
        prg += 1
        time.sleep(0.1)

    print "\n"
    print "Copied all files to: ",os.path.abspath(destination)
    print "\n"

    
if __name__ == "__main__":
    with open(NET_ID_FILE, 'rb') as fh:
        reader = csv.reader(fh)
        students = list(reader)

    net_ids = [x[2] for x in students[1:]]
    # Testing --
    """
    for net_id in net_ids:
        os.chdir('/home/mohitsharma44/Documents/'+net_id)
        with open("file_%s.ipynb"%net_id, 'wb') as fout:
            fout.write(os.urandom(1024))

        os.chdir(os.pardir)
        
    """
    files = find_solutions(net_ids, FILENAME)
    copy_solutions(files, DESTINATION)
    
    # Information of students who submitted challenge
    names_submitted =  filter(lambda x: x if x[2] in files.keys() else False, students)
    with open(FILENAME[:-6]+"_students.csv", 'w') as fh:
        writer = csv.writer(fh, delimiter=',')
        writer.writerows(names_submitted)
