find evaluate -type d | while read -r dir
do
  echo -e "\nDirectory: $dir"
  before=$dir/problem.py
  after=$dir/problemref.py
  python judgeprog.py $before $after
done
