#!/bin/sh

if [ "e$1" == "e" ] ; then
    echo "call $0 <JOBID>"
    exit
fi


export SLURM_TIME_FORMAT="%s"
DATA=`sacct -j $1 -o start,end,user | tail -n2`

if [ "$?" -ne 0 ] ; then
    echo "job not found?"
    exit
fi

START=`echo $DATA | awk '{print $1}'`
END=`echo $DATA | awk '{print $2}'`
USER=`echo $DATA | awk '{print $3}'`


python get_data_from_db.py --jobid $1 --user ${USER} --start ${START} --end ${END}