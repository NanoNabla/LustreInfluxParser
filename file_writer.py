import numpy as np


def write_csv(jobid, dataset):
    jobid = str(jobid)

    for db in dataset:
        for group in db:
            for measurement in group['measurements']:
                np.savetxt(jobid + '_' + group['database'] + '_' + group['name'] + '_' + measurement['name'] + '.csv', measurement['value'],
                           delimiter=",")
