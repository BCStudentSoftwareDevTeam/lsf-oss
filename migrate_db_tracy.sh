#pip install peewee==3.9.6
#pip install peewee-migrations==0.3.18

rm -f migrations.json 2> /dev/null

pem init

if [[ "$OSTYPE" == "linux-gnu" ]]; then
        # ...
    sed -i 's/migrations/tracy_migrations/g' migrations.json
elif [[ "$OSTYPE" == "darwin"* ]]; then
        # Mac OSX
    sed -i '' 's/migrations/tracy_migrations/g' migrations.json
fi


pem add app.models.Tracy.studata.STUDATA
pem add app.models.Tracy.stustaff.STUSTAFF
pem add app.models.Tracy.stuposn.STUPOSN

pem watch

pem migrate
