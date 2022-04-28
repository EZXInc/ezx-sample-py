HOME=$(dirname `readlink -f "$0"`)/..
HOST="192.168.1.100"
PORT="2200"
SRC="$HOME/src/"
# Maven release builds project from VCS checkout and creates entirely parallel directory structure under target/checkout
RLS=$SRC
TRG="/home/iserver/ezx-pyapi/sample"
USR=iserver

# option r = release
while getopts ":h:p:r" opt; do
	case $opt in
	h) HOST="$OPTARG";;
	p) PORT="$OPTARG";;
	r) SRC=$RLS;;
	esac
done

echo HOST=$HOST
echo PORT=$PORT

DST=$USR@$HOST:$TRG
echo SRC=$SRC
echo DST=$DST
echo "synching dependencies from "$SRC" to "$DST""
rsync --exclude logs --exclude config --exclude tests --exclude __pycache__ --exclude CVS  -r --delete -v -u -e "ssh -p $PORT" "$SRC" "$DST" 


