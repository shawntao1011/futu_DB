#!/bin/bash

# get absolute path to setenv.sh directory
if [ "-bash" = $0 ]; then
  dirpath="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
else
  dirpath="$(cd "$(dirname "$0")" && pwd)"
fi

export TORQHOME=${dirpath}
export FUTUAPPHOME=${TORQHOME}
export TORQDATAHOME=${TORQHOME}
export KDBCONFIG=${TORQHOME}/config
export KDBCODE=${TORQHOME}/code
export KDBTESTS=${TORQHOME}/tests
export KDBLOG=${TORQDATAHOME}/logs
export KDBHTML=${TORQHOME}/html
export KDBLIB=${TORQHOME}/lib
export KDBHDB=${TORQDATAHOME}/hdb
export KDBWDB=${TORQDATAHOME}/wdbhdb
export KDBDQCDB=${TORQDATAHOME}/dqe/dqcdb/database
export KDBDQEDB=${TORQDATAHOME}/dqe/dqedb/database
export KDBTPLOG=${TORQDATAHOME}/tplogs
export KDBTESTS=${TORQHOME}/tests

# set rlwrap and qcon paths for use in torq.sh qcon flag functions
export RLWRAP="rlwrap"
export QCON="qcon"
export QCMD="q" #set qcmd path

# set KDBBASEPORT to the default value for a TorQ Installation
export KDBBASEPORT=6000

# set TORQPROCESSES to the default process csv
export TORQPROCESSES=${KDBAPPCONFIG}/process.csv