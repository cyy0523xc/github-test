#!/bin/bash

# 自定义bashrc
# 在~/.bashrc中被引用

alias ssh179='ssh root@112.124.47.179'
alias ssh195='ssh root@115.29.166.195'
alias ssh35='ssh root@42.120.21.35'

alias yuic="java -jar /home/code/ibbd/cyy-doc/tools/yuicompressor-2.4.7.jar "

# elasticsearch
alias es="/home/alex/programs/elasticsearch-1.2.2/bin/elasticsearch"

# es的get数据接口
# 用法：esget cafe order '{...}'
# 参数说明：
#   $1: index
#   $2: type
#   $3: json字符串
esget() {
    echo ""
    curl -XGET "http://localhost:9200/$1/$2/_search?search_type=count" -d "$3" | python -m json.tool
    echo ""
}

cd_github_code() {
    cd /home/code/github/
}

cd_ibbd_code() {
    cd /home/code/ibbd/ 
}

# gitlab: new project
# 参数说明：
#   $1: project name
#   $2: group name, the default value is "ibbd"
ibbd_git_init() {
    if [2 == $#]; then
        groupname=$2
    else
        groupname="ibbd"
    fi

    cd_github_code
    mkdir $1
    cd $1
    git init
    touch README
    git add README
    git commit -m 'first commit'
    git remote add origin git@git.ibbd.net:${groupname}/$1\.git
    git push -u origin master

    echo ""
    echo "project $1 is OK!"
}

