set -x

PYTHON_VERSION=$1
OUTPUT_DIR=./output_$PYTHON_VERSION

set -e

mkdir ./output_$PYTHON_VERSION

cp krem/tests/library/scripts/Dockerfile_$PYTHON_VERSION ./Dockerfile

docker build -t krem_test_framework .

set +e
docker run --name test_krem krem_test_framework
test_rc=$?

docker cp test_krem:/usr/src/app/krem/tests/output $OUTPUT_DIR
output_rc=$?

docker rm -f test_krem
clean_img_rc=$?

docker rmi -f krem_test_framework
clean_cont_rc=$?

if [ $test_rc -eq 1 ] || [ $output_rc -eq 1 ] || [ $clean_img_rc -eq 1 ] || [ $clean_cont_rc -eq 1 ]
then
	exit 1
else
	exit 0
fi
