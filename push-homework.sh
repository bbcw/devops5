#!bin/bash

DAY=$1
MSG=$2

# commit 本地信息
git add -A .
git commit -am "commit again"

# 删除本地标签
# git tag -d "$TAG"

# 删除远端标签
# git push origin :refs/tags/mingmings-day4


# 生成本地标签
git tag -a mingmings-day${DAY} -m ${MSG}

# 连同标签一起将本地 master 分支推送到远端 mingmings 分支上
git push origin master:mingmings --tags
