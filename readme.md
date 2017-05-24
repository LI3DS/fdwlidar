# Foreign Data Wrappers for LI³DS

This repo includes [Multicorn](http://multicorn.org/)-based [Foreign Data
Wrappers](https://www.postgresql.org/docs/current/static/fdwhandler.html)
for exposing LI³DS data as PostgreSQL tables.

## Prerequisites

- python == 2.7
- numpy
- multicorn

### Install under Ubuntu

Install PostgreSQL 9.5 from PGDG repositories and Python

```sh
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
sudo apt-get install wget ca-certificates
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install python2.7 python2.7-dev python-setuptools python-pip python-numpy postgresql-9.5 postgresql-server-dev-9.5
```

Compile and install Multicorn
```sh
git clone git@github.com:Kozea/Multicorn.git
cd Multicorn
make
sudo make install
```

## Installation

Clone repository and install with:

	sudo pip install .

or install in editable mode (for development):

	sudo pip install -e .

## Testing

Load the pointcloud extension in order to have the pcpatch type available.

```sql
create extension if not exists pointcloud;
```

### Custom EchoPulse format

```sql
drop extension multicorn cascade;
create extension multicorn;

create server echopulse foreign data wrapper multicorn
    options (
        wrapper 'fdwli3ds.EchoPulse'
    );

-- create foreign table to retrieve the pointcloud schema dynamically
create foreign table myechopulse_schema (
    schema text
)
server echopulse
    options (
        directory 'data/echopulse'
        , metadata 'true'
    );

insert into pointcloud_formats(pcid, srid, schema)
select 1, -1, schema from myechopulse_schema;

create foreign table myechopulse (
    points pcpatch(1)
) server echopulse
    options (
        directory 'data/echopulse'
        , patch_size '400'
        , pcid '1'
    );

select * from myechopulse;
```

### Sbet files

```sql
create server sbetserver foreign data wrapper multicorn
    options (
        wrapper 'fdwli3ds.Sbet'
    );

create foreign table mysbet_schema (
    schema text
)
server sbeserver
 options (
    metadata 'true'
);

insert into pointcloud_formats (pcid, srid, schema)
select 2, 4326, schema from mysbet_schema;

create foreign table mysbet (
    points pcpatch(2)
) server sbetserver
    options (
        sources 'data/sbet/sbet.bin'
        , patch_size '100'
        , pcid '2'
);


select * from mysbet;

```


## Unit tests

Pytest is required to launch unit tests.

```
sudo apt-get install python-pytest
```

Or

```bash
pip install -e .[dev]
```

Launch tests:

```bash
py.test
```
