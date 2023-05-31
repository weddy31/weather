const http = require('http');
const https = require('https');
const fs = require('fs');

const url = 'https://danepubliczne.imgw.pl/api/data/synop/';

https.get(url, (res) => {
  let body = '';

  res.on('data', (chunk) => {
    body += chunk;
  });

  res.on('end', () => {
    try {
      fs.writeFile('pogoda.json', body, (err) => {
        if (err) {
          console.error(err);
        }
      });
    } catch (error) {
      console.error(error.message);
    }
  }).on('error', (error) => {
    console.error(error.message);
  });
});

http.createServer(function (req, res) {
  if (req.url === '/') {
    fs.readFile('./pogoda.html', function (err, data) {
      res.writeHead(200, { 'Content-Type': 'text/html' });
      res.write(data);
      return res.end();
    });
  } else if (req.url === '/data') {
    fs.readFile('./pogoda.json', 'utf-8', (err, jsonString) => {
      if (err) {
        console.log('File read failed:', err);
        return;
      }
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(jsonString);
    });
  }
}).listen(8080);
