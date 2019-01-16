*** Introduction ***

SkillStash uses two separate server processes, which we refer to as the front
end and the back end. The front end serves the application's pages to the
user's browser, and the back end handles the application logic and database
connectivity. These processes can run on either Linux or Windows. This guide
explains how to run on a Linux System.

Our project.tgz file contains a single folder called skillstash, which you
can simply extract to a convenient location on your machine. For simplicity
we will refer to this directory as $SKILLSTASH.



*** Installing the System Dependencies ***

Before you can run the server processes, some software needs to be installed on
your system. The back end is written in Python 3, which can be downloaded from:

	http://www.python.org/downloads/release/python-370/

SkillStash requires a number of Python packages. For convenience, we have
listed them in the file $SKILLSTASH/requirements.txt. You can install them
using pip3 as follows:

	cd $SKILLSTASH
	pip3 install -r requirements.txt

The front end requires Node.js. If it is not already installed on your system,
please download the appropriate version from the following website and follow
the installation instructions:

	https://nodejs.org/en/



*** Configuring the Database ***

After the necessary dependencies have been installed, the only manual
preparation required is to configure the database. SkillStash interacts with
the database entirely through Django, so it should be able to use any DBMS
that Django supports. We have tested it using SQLite and PostgreSQL.

SQLite is sufficient to run SkillStash and perform simple operations. However,
its lack of support for concurrency causes certain operations that require
multiple database updates, such as updating a user's skills, to fail. If you
try to update multiple skills at once, some of the changes will often fail
to save. PostgreSQL does not suffer from this problem and should therefore be
used if possible. If you need to install PostgreSQL, you can download it from:

	http://www.postgresql.org/

SkillStash's database connection is configured in the following section of
$SKILLSTASH/prototype/settings.py:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'OPTIONS': {
            'timeout': 20,
        }
    },
    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql_psycopg2',
    #     'NAME': 'skillstash',
    #     'USER': 'skillstash',
    #     'PASSWORD': '',
    #     'HOST': '',
    #     'PORT': '5432',
    # }
}

SQLite is enabled by default, because it has no external dependencies. If
you wish to use SQLite then no changes should be required.

If you wish to use PostgreSQL, comment out the sqlite3 section and uncomment
the postgresql_psycopg2 section. You will also have to set HOST and PORT
correctly for your PostgreSQL server. If the server is running on the same
machine as SkillStash then HOST can be left blank.

If you use PostgreSQL, you will have to create the skillstash database on
your server. This can be done with the following command:

   createdb skillstash



*** Setting up SkillStash with Demonstration Data ***

To make it easier to test SkillStash, we have provided some test skills,
users, and jobs to populate the database. There is a shell script called
setup_demo.sh to automate the setup. Please run it as follows:

   cd $SKILLSTASH
   ./setup_demo.sh

Note that you must be in the $SKILLSTASH directory when you run the script. If
you run it from another directory (for example by specifying an absolute path)
it will not work correctly.



*** Running the Back End ***

Once setup_demo.sh has finished, you should be able to run the back end
using the following commands:

	 cd $SKILLSTASH
	 python3 manage.py runserver 7999

By default SkillStash runs the back end on port 7999. If you wish to use a
different port, simply change 7999 to the port that you wish to use.



*** Running the Front End ***

The JavaScript code running in the user's browser needs to know
the URL to communicate with the back end server. This is set in
$SKILLSTASH/apps/frontend/build/webpack.dev.conf.js. By default it is
configured to connect to the back end at http://localhost:7999. If you run
the back end on port 7999 and run your browser on the same machine, you do
not have to change this setting.

If you run the back end on a different port, or run
your browser on a separate machine, you will need to edit
$SKILLSTASH/apps/frontend/build/webpack.dev.conf.js. Find the following
setting (at line 50) and change it to the host and port number that the back
end is running on:

   API_HOST: JSON.stringify("http://localhost:7999")

To start the front end, please execute the following commands:

   cd $SKILLSTASH/apps/frontend/
   npm run dev

By default the front end will run on port 8001. You can change this by editing
the port setting at line 17 of $SKILLSTASH/apps/frontend/config/index.js.



*** Using SkillStash ***

Once both the back and front ends are running, you should be able to connect
to SkillStash from your web browser. If you are running your browser on the
same machine as SkillStash, please enter the following into your address field:

	 http://127.0.0.1:8001

This should take you to the SkillStash home page, from where you can log
in by clicking on the "Sign In" link. If you are running your browser on a
separate machine, or using a different port, please change the IP address
and port appropriately.

The demonstration system includes the following user accounts, all of which
have the password "nopassword":

Candidates

b.fawlty@example.com
e.knerd@example.com
j.bond@example.com
j.dean@example.com
m.jones@example.com
m.kelly@example.com
m.monroe@example.com
s.jones@example.com

Employers

j.nerd@example.com
m.smart@example.com
n.kelly@example.com

Recruiters

e.idle@example.com
j.smith@example.com

Please see the SkillStash user manual for details of how to use the system.

If you experience any problems running SkillStash, or have any questions,
please call Chris on 0408-446-752. I will be happy to help.

