var store = require('app-store-scraper');

store.reviews({
  appId: 'com.oceanwing.soundcore',
  country: 'it',
  lang: 'pt',
  num: 50
})
.then(console.log)
.catch(console.log);