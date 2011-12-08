# DotCloud CLI

This is a beta version of the new DotCloud command line interface.

## What's New

This version of CLI is designed to work with the application directory
linked to the remote dotcloud application.

This allows you to avoid typing the same application names multiple
times, and reduce the possiblity of making typos and overwrite wrong
applications by repeating the command line history.

    # New CLI 
    > dotcloud2 push
    > dotcloud2 info
    > dotcloud2 ssh www

    # Old CLI
    > dotcloud push myapp .
    > dotcloud info myapp
    > dotcloud ssh myapp.www

The command line executable is installed as `dotcloud2` so that you
can keep using the existing version of the dotcloud command.

## Setup

First, you have to configure your CLI to work as a DotCloud REST API
consumer.

    > dotcloud2 setup
    Dotcloud Username: your-user-name
    Password: **********

You're asked to provide your username and password for DotCloud, to
register the new CLI client as a DotCloud REST API consumer. You can
also use email, instead of your username.

The CLI won't save this credentials locally - instead, it will save
the OAuth2 access token in the local disk. Once the setup is complete,
you can run the check command to see if everything is configured
correctly.

    > dotloud2 check
    --> Checking the authentication status
    OK: Client is authenticated as <your-username>

If this fails, try removing the directory `~/.dotcloud2` and start
over from the setup.

## Working with your application

    > cd ~/dev
    > mkdir myapp
    > (write some code)

### Create

Once you've done writing your awesome application, run the `create` command:

    > dotcloud2 create myapp
    --> Creating a new application called "myapp"
    Application "myapp" created.
    Connect the current directory to "myapp"? [Yn]: y
    --> Connecting with the application "myapp"
    --> Connected.

As you see, the CLI asks you if you want to connect the current
working directory to the remote application. This allows you to omit
typing the application name from now on.

### Running commands

To push the code to the DotCloud platform, simply type:

    > dotcloud2 push

and it will upload the code from the current directory to the
application. You can see the currently connected application by typing:

    > dotcloud2 app
    myapp

You can see the list of commands by running `dotcloud2 -h`.

If you typed `n` when asked to connect the current directory, the CLI
can't find the application name for the commands. You can specify the
application name in such case, using the `--application` (or `-A` for
short) option:

    > dotcloud2 -A myapp info

You can also use this option when you want to run commands against the
application that you don't have the working directory for.

### Connect

Similarly, if you already have a working directory *and* a dotcloud
remote application and want to connect them together, instead of
creating a new application, run the connect command:

    > cd ~/dev/myapp
    > dotcloud2 connect myapp

It will create your working directory with the (existing) dotcloud application `myapp`.

