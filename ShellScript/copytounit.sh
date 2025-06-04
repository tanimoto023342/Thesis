if [ -z "$1" ]; then
  echo "エラー: 第一引数が指定されていません。" >&2
  exit 1
fi

cp $1/test.py test.py
cp $1/testref.py testref.py