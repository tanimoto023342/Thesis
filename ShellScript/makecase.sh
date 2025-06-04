if [ -z "$1" ]; then
  echo "エラー: 第一引数が指定されていません。" >&2
  exit 1
fi

mkdir $1; 
touch $1/exp.txt; 
touch $1/test.py; 
touch $1/testref.py