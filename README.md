# Swiss Tournament Mini-Program

This program will simulate rounds of a Swiss Tournament. In the first round
each player will be randomly assigned to another and a win or loss will be recorded.

This project is still in develepment. #AlphaVersion

###Install Virtualbox###
https://www.virtualbox.org/wiki/Downloads


###Install Vagrant###
https://www.vagrantup.com/downloads

Verify that Vagrant is installed and working by typing in the terminal:

    $ vagrant -v   # will print out the Vagrant version number

###Clone the Repository###
Once you are sure that VirtualBox and Vagrant are installed correctly execute the following:

    $ git clone https://github.com/gvalverde/swiss-tournament.git
    $ cd swiss-tournament

###Launch the Vagrant Box###

    $ vagrant up   #to launch and provision the vagrant environment

Optional: This VagrantFile installs a gui, you can login with the username and password "vagrant".

###Enter the Swiss Tournament###

    $ cd ~/swiss-tournament/tournament

###Initialize the database###

    $ psql
    vagrant=> \i tournament.sql
    vagrant=> \q


###Run the unit tests###

    $ python tournament_test.py

You should see these results:

    1. Old matches can be deleted.
    2. Player records can be deleted.
    3. After deleting, countPlayers() returns zero.
    4. After registering a player, countPlayers() returns 1.
    5. Players can be registered and deleted.
    6. Newly registered players appear in the standings with no matches.
    7. After a match, players have updated standings.
    8. After one match, players with one win are paired.
    Success!  All tests pass!

###Shutdown Vagrant machine###

    $ vagrant halt


###Destroy the Vagrant machine###

    $ vagrant destroy

