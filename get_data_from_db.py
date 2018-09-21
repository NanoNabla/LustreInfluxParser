import argparse
import datetime

import config
import file_writer
import numpy as np
import pytz
import visualize
from influxdb.client import InfluxDBClient


def main(jobid, slurm_start, slurm_end, user):
    # time adjust
    slurm_start = slurm_start
    slurm_end = slurm_end

    dataset = []
    for db in config.measurements_databases:
        # dataset.append({db: []})
        database = []
        for group in config.measurements:
            collection = {'unit': group['unit'], 'name': group['name'], 'database': db['name'], 'measurements': []}
            #            measurements = []
            for measurement in group['measurements']:
                table = db['entry'] + '."' + measurement['value'] + '"'
                data = getDataFromDb(slurm_start, slurm_end, user, table)
                data = filterDataByJobId(jobid, slurm_start, data, measurement['value'])
                collection['measurements'].append({'name': measurement['name'], 'value': data})
            database.append(collection)
        dataset.append(database)
    visualize.plot(jobid, dataset)
    file_writer.write_csv(jobid, dataset)


def getDataFromDb(slurm_start, slurm_end, user, database):
    """ Connecting to Influx database """
    start_date = encodeTime(slurm_start)
    end_date = encodeTime(slurm_end)

    client = InfluxDBClient(config.db_host, config.db_port, config.db_user, config.db_pass)

    qry_str = 'SELECT "value", "jobid" FROM ' + database + ' WHERE time > \'' + start_date + '\' AND time < \'' + end_date + '\' AND "user"=\'' + user + '\''
    qry_res = client.query(qry_str)

    return qry_res


# TODO rename bla
def filterDataByJobId(jobid, slurm_start, raw_data, bla):
    """ Filter job id from the data returned by the database since no native filtering for jobid is possible, returns 2d numpy array """
    measurements = raw_data.get_points(measurement=bla)
    size = len(list(measurements))
    filtered = np.zeros((size, 2), dtype=np.float)

    i = 0
    for measurement in raw_data.get_points(measurement=bla):
        if measurement['jobid'] == jobid:
            # if i == 0:
            #    time_zero = decodeTime(measurement['time'])
            # filtered[i][0] = decodeTime(measurement['time']) - time_zero
            filtered[i][0] = transTime(measurement['time'], slurm_start)
            filtered[i][1] = measurement['value']
        i += 1

    filtered.resize((i, 2), refcheck=False)

    return filtered


def encodeTime(timestamp):
    """Convert a unix timestamp to format used by the database"""
    tz_utc = pytz.timezone('UTC')
    # bla = datetime.datetime.fromtimestamp(int(timestamp))
    # bla = tz_utc.localize(bla)
    # return str(bla.strftime('%FT%T') + 'Z')
    return str(datetime.datetime.fromtimestamp(int(timestamp)).astimezone(tz_utc).strftime('%FT%T') + 'Z')


# TODO
def decodeTime(timestamp):
    """Convert database's timestamp to a unix timestamp"""
    tz_utc = pytz.timezone('UTC')
    bla = datetime.datetime.strptime(timestamp[:-1], '%Y-%m-%dT%H:%M:%S')
    return int(tz_utc.localize(bla).strftime('%s')) + 3600


#    return int(datetime.datetime.strptime(timestamp[:-1], '%Y-%m-%dT%H:%M:%S').strftime('%s'))


def transTime(timestamp, start_time):
    """Transpose a absolute timestamp to the seconds since the job began"""
    timestamp = decodeTime(timestamp)
    #    print("timestamp: "+ str(timestamp) + "   slurm: " + str(start_time))
    return timestamp - int(start_time)

    # tz_utc = pytz.timezone('UTC')
    # # date = datetime.datetime.strptime(timestamp[:-1], '%FT%T')
    # # start_time = datetime.datetime.fromtimestamp(int(start_time)).astimezone(tz_utc).strftime('%FT%T')
    #
    # date = datetime.datetime.strptime(timestamp[:-1], '%Y-%m-%dT%H:%M:%S')
    # start_time = datetime.datetime.fromtimestamp(int(start_time)).astimezone(tz_utc)
    #
    # print(
    #     "time " + str(date) + "   " + date.strftime("%s") + " start: " + str(start_time) + "   " + start_time.strftime(
    #         "%s"))
    #
    # return int(date.strftime("%s")) - int(start_time.strftime("%s"))


def parse_args():
    """Parse the args from main."""
    parser = argparse.ArgumentParser(
        description='get I/O data from InfluxDB')
    parser.add_argument('--jobid', type=int, required=True,
                        help='job id')
    parser.add_argument('--user', type=str, required=True,
                        help='user who submitted the job')
    parser.add_argument('--start', type=int, required=True,
                        help='unix timestamp when job started')
    parser.add_argument('--end', type=int, required=True,
                        help='unix timestamp when job finished')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    main(args.jobid, args.start, args.end, args.user)

# slurm_start = '1536078944'
# slurm_end = '1536079597'
# jobid = 1452958
# user = 's8916149'

# main(jobid, slurm_start, slurm_end, user)
