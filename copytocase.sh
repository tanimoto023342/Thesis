if [ -z "$1" ]; then
  echo "エラー: 第一引数が指定されていません。" >&2
  exit 1
fi

cp test.py $1/test.py
cp testref.py $1/testref.py