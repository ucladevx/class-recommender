## Endpoints

Backend will now take in a file as multi-part form data, parse it, and then populate it into the db.
However, now you need a secrets.sh file that must be placed in this folder in order for it to work.

To test, run 

```
make
curl -F "file=@/path/to/pdf.pdf localhost:5000/extract
```

You should expect to see a json object returned to you, and the db should reflect the changes

https://us-west-2.console.aws.amazon.com/dynamodb/home?region=us-west-2#tables:selected=users
