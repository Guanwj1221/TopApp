var store = require('app-store-scraper');
var fs = require("fs")
fs.exists('/etc/passwd123', (exists) => {
  console.log(exists ? '存在' : '不存在');
  if (!exists) {
    return
  }
  console.log(123123)
});
