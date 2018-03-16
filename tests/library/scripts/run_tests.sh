set -x
set -e

ROOT_PATH=$PWD
KREM_PATH=$ROOT_PATH/krem
KREM_TESTS_PATH=$KREM_PATH/tests
JOB_OUTPUT_PATH=$KREM_TESTS_PATH/output/integration_testing

cd $KREM_PATH
./install.py
source ~/.bashrc


cd $KREM_TESTS_PATH
if [ -d "$JOB_OUTPUT_PATH" ]; then
  rm -r $JOB_OUTPUT_PATH/*
fi

krem run -j integration_testing

