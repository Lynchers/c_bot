#!/usr/bin/env bash

PROGRAM=c_bot

EXEC=./$PROGRAM.py
RUN_DIR=./run
PID_FILE=$RUN_DIR/$PROGRAM.pid
LOG_DIR=./logs
LOG_FILE=$LOG_DIR/`date '+%Y%m%d%H%M%S'`.log

if [ ! -d "$RUN_DIR" ]; then
  mkdir $RUN_DIR
  echo "$RUN_DIR created"
fi

if [ ! -d "$LOG_DIR" ]; then
  mkdir $LOG_DIR
  echo "$LOG_DIR created"
fi

$EXEC > $LOG_FILE 2>&1 &
PID=$!
echo $PID > $PID_FILE
echo "$PROGRAM bot started, pid is: $PID, pid file: $PID_FILE, log file: $LOG_FILE"
