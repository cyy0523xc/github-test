#!/bin/bash

# 安装应用
# @param string $1  app name
install-app() {
    if 
        ! which $1
    then
        sudo apt-get install $1
    fi
}

# 配置vim之前，必须先安装nodejs，不然在编辑js文件时会报错
#sudo apt-get install nodejs
install-app nodejs

# begin 配置vim
wget -qO- https://raw.github.com/ma6174/vim/master/setup.sh | sh -x 

# 先安装pathogen.vim   https://github.com/tpope/vim-pathogen
mkdir -p ~/.vim/autoload ~/.vim/bundle && \
curl -LSso ~/.vim/autoload/pathogen.vim https://tpo.pe/pathogen.vim

# 再安装Tabular
mkdir -p ~/.vim/bundle
cd ~/.vim/bundle
git clone git://github.com/godlygeek/tabular.git

# end 配置vim

install-app curl

install-app gitk

install-app guake

install-app freemind

install-app gnome-do

install-app terminator

install-app tmux

# python代码检查
install-app pep8

# install git-flow

install-app git-flow

# ab测试工具
install-app apache2-utils

# install pinta
sudo add-apt-repository ppa:pinta-maintainers/pinta-stable

# install 视频播放器
install-app vlc 

# mycli mysql
curl https://packagecloud.io/gpg.key | apt-key add -
apt-get install -y apt-transport-https
echo "deb https://packagecloud.io/amjith/mycli/ubuntu/ trusty main" | sudo tee -a /etc/apt/sources.list

# update 
sudo apt-get update

# install 减少等待时间
install-app pinta
sudo apt-get install mycli



