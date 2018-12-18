# Lustre-InfluxDB-Parser

This projects gets data from a slurm job's usage of the lustre filesystem from an influx databse. It is used on the taurus cluster at TU Dresden.

Only jobs submitted on the SCS5 system will be in the dabase.

## Installation

```
git clone https://github.com/NanoNabla/LustreInfluxParser.git

virtualenv -p python3 virtualenv
source virtualenv/bin/activate
pip -r requirements.txt

# edit login data in config.py
```

## Usage
If you ran on taurus load python 3:
```module load Python/3.6.6-foss-2018b ```

If you are not on taurus make sure python 3 is avaibale and you are able to connect to influxdb. At TU Dresden it is necessary to have an IP in the campus net.


```
source virtualenv/bin/activate
# configure the data want to receive in config.py

get_data_from_db.py" --jobid <JOB_ID> --user <USERNAME> --start <UNIX_TIMESTAMP> --end <UNIX_TIMESTAMP>
```
The necessary information can be gotten by:

```SLURM_TIME_FORMAT="%s" sacct -j <JOB_ID> -o start,end,user```

For running on taurus you can use the runscirpt which only needs the jobid

```
source virtualenv/bin/activate
./get_data_from_db.sh <JOB_ID>
```

## Possible databases
- lustremon_scratch2.autogen  (/scratch/)
- lustremon_highiops.autogen (/lustre/ssd/)

## Possible values to monitor
- lustre.close.samples
- lustre.crossdir_rename.samples
- lustre.getattr.samples
- lustre.getxattr.samples
- lustre.link.samples
- lustre.mkdir.samples
- lustre.mknod.samples
- lustre.open.samples
- lustre.punch.samples
- lustre.read_bytes.max
- lustre.read_bytes.min
- lustre.read_bytes.samples
- lustre.read_bytes.sum
- lustre.rename.samples
- lustre.rmdir.samples
- lustre.samedir_rename.samples
- lustre.setattr.samples
- lustre.setxattr.samples
- lustre.statfs.samples
- lustre.sync.samples
- lustre.unlink.samples
- lustre.write_bytes.max
- lustre.write_bytes.min
- lustre.write_bytes.samples
- lustre.write_bytes.sum

## Known bugs
- There is problem with timezone conversion and daylight saving time
- Run script for taurus (```sacct | tail -n2```)
