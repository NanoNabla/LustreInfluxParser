import matplotlib as mpl

mpl.use('agg')
import matplotlib.pyplot as plt


def plot(jobid, dataset):

    jobid = str(jobid)

    i = 1
    for db in dataset:
        #        plt.subplot(len(dataset) * len(db), 1, i)
        for group in db:
            plt.figure(i)
            plt.title(group['name'] + ' on ' + group['database'] + ' for job: #' + jobid)
            plt.xlabel('time [s]')
            plt.ylabel(group['unit'])
            for measurement in group['measurements']:
                # TODO styling
                # plt.plot(data[:, 0], data[:, 1], '--b.', label='write')
                plt.plot(measurement['value'][:, 0], measurement['value'][:, 1], '--.', label=measurement['name'])
                # print(group['name'] + "  " + measurement['name'] + "   " + str(measurement['value'][:, 0]) + "     " + str(measurement['value'][:, 1]))
            plt.grid(color='gray', linestyle='-', linewidth=0.2)
            plt.legend()
            # plt.show()
            plt.savefig(jobid + '_' + group['database'] + '_' + group['name'] + '.png', dpi=300, facecolor='w',
                        orientation='portrait', transparent=False)
            i += 1

            # plt.savefig(jobid+'_' + group['name'] + '.png')
            # plt.close()

# plt.savefig(jobid+'.png')