echo "*********************************"
echo "*                               *"
echo "*      Adding repositories      *"
echo "*                               *"
echo "*********************************"
sudo add-apt-repository ppa:webupd8team/sublime-text-3

echo "*********************************"
echo "*                               *"
echo "*     Updating and upgrading    *"
echo "*                               *"
echo "*********************************"
sudo apt-get -y update
sudo apt-get -y upgrade

echo "*********************************"
echo "*                               *"
echo "*        VBox Utilities         *"
echo "*                               *"
echo "*********************************"
sudo apt-get install -y virtualbox-guest-utils virtualbox-guest-x11 virtualbox-guest-dkms

echo "*********************************"
echo "*                               *"
echo "*        Installing Git         *"
echo "*                               *"
echo "*********************************"
sudo apt-get install -y git
git config --global color.ui true
cd ~
git clone https://github.com/magicmonty/bash-git-prompt.git ~/.bash-git-prompt
echo 'GIT_PROMPT_ONLY_IN_REPO=1' >> ~/.bashrc
echo 'GIT_PROMPT_SHOW_UNTRACKED_FILES=normal' >> ~/.bashrc
echo 'GIT_PROMPT_THEME=Single_line_Solarized' >> ~/.bashrc
echo 'source ~/.bash-git-prompt/gitprompt.sh' >> ~/.bashrc

echo "*********************************"
echo "*                               *"
echo "*        My GitHub Reps         *"
echo "*                               *"
echo "*********************************"
cd ~
git clone https://github.com/gustavovalverde/swiss-tournament.git ~/swiss-tournaments

echo "******************************************"
echo "*                                        *"
echo "*  Installing Python and dependencies    *"
echo "*                                        *"
echo "******************************************"
sudo apt-get install -qq -y python-software-properties software-properties-common
sudo apt-get install python
sudo apt-get -qq -y install postgresql python-psycopg2
sudo apt-get -qq -y install python-flask python-sqlalchemy
sudo apt-get remove python-pip
sudo -H  easy_install -U pip
sudo -H  pip install bleach
sudo -H  pip install oauth2client
sudo -H  pip install requests
sudo -H  pip install httplib2
sudo -H  pip install redis
sudo -H  pip install passlib
sudo -H  pip install itsdangerous
sudo -H  pip install flask-httpauth
sudo -H  pip install flake8
sudo su postgres -c 'createuser -dRS vagrant'
sudo su vagrant -c 'createdb'
sudo su vagrant -c 'createdb tournament'
sudo su vagrant -c 'psql \i /vagrant/swiss-tournament/tournament/tournament.sql'


echo "*********************************"
echo "*                               *"
echo "*     Installing Sublime 3      *"
echo "*                               *"
echo "*********************************"
git clone https://github.com/gustavovalverde/sublime-text-seed.git ~/.sublime-seed
cd ~/.sublime-seed
./setup.py

echo "*********************************"
echo "*                               *"
echo "*          redis-stable         *"
echo "*                               *"
echo "*********************************"
cd ~
sudo wget http://download.redis.io/redis-stable.tar.gz
sudo tar xvzf redis-stable.tar.gz
cd redis-stable
make
sudo make install

echo "******************************************"
echo "*                                        *"
echo "*          Installing Browser            *"
echo "*                                        *"
echo "******************************************"
sudo apt-get install -qq -y firefox

echo "*********************************"
echo "*                               *"
echo "*   Installing MATE Desktop     *"
echo "*                               *"
echo "*********************************"
sudo apt-get install -y ubuntu-mate-core ubuntu-mate-desktop

echo "*********************************"
echo "*                               *"
echo "*        Time to reboot         *"
echo "*                               *"
echo "*********************************"
  # have to reboot for drivers to kick in, but only the first time of course
if [ ! -f ~/runonce ]
then
  sudo reboot
  touch ~/runonce
fi
