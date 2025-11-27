# Aiogram bot template
by Arizel79

## Run
### Installation
```commandline
pip install -r requirements.txt
```
### Create DB and apply all migrations
```commandline
alembic upgrade head
```
### Create config template
```commandline
cp config.yaml.template config.yaml
```
Change bot token in `config.yaml` (`bot.token`)
### Start bot
```commandline
python main.py
```

### Migrations
Create migration
```commandline
alembic revision --autogenerate -m "Changes in this migration"
```
Migrate to last migration
```commandline
alembic upgrade head
```
Migrate to current migration
```commandline
alembic upgrade revision_id
```
Show current migration
```commandline
alembic current
```