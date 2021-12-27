// var store = require('app-store-scraper');
//
// store.reviews({
//   appId: 'com.oceanwing.SoundCore',
//   sort: store.sort.RECENT,
//   page: 9,
//   country: 'us'
// })
// .then(console.log)
// .catch(console.log);


// let store = require('app-store-scraper');
// var content = "";
// for(let i = 1; i < 10; i++) {
//   store.reviews({
//   appId: 'com.oceanwing.SoundCore',
//   country: 'us',
//   sort: store.sort.RECENT,
//   page: i
//   })
//   .then((body) => {
//     let reviews = JSON.stringify(body)
//
//     content += JSON.stringify(body)
//     console.log('============')
//     console.log(reviews)
//   })
// }

// let page = 10
// var num = 1
// var fs = require("fs")
// for (var i = 1; i <= page; i++) {
//     gplay = require('app-store-scraper')
//     gplay.reviews({
//     appId: 'com.roblox.robloxmobile',
//         lang: 'en',
//     country: 'us',
//     sort: gplay.sort.RECENT,
//     page: i
//     })
//     .then((body) => {
//         let fileName = "/Users/anker/MyProject/Python/TopApp/AppleStore/Test1.json"
//         let file = fileName.slice(0, fileName.length - 5) + "_test.json"
//         if ("[]" !== JSON.stringify(body)) {
//
//             console.log(file)
//            fs.writeFile(file, JSON.stringify(body), {flag: 'a'}, (err) => {
//             if (err) {
//                 console.error(err)
//             }
//         })
//         }
//         console.log(num)
//         num += 1
//         if (num === page) {
//             fs.rename(file, fileName, function(err)
//             {
//                 if (err) throw err;
//                 console.log('Successful modification,');
//             });
//         }
//     })
// }

var count = 1
var gplay = require('google-play-scraper')
var fs = require("fs")
function reviews(platform, app_id, lang, country, sort, num, file_name) {
    var page = num / 50
    if (page > 10)
        page = 10
    if (page < 1)
        page = 1
    if (platform === 'apple_store')
    {
        for (var i = 1; i <= page; i++) {
            gplay = require('app-store-scraper')
            gplay.reviews({
            appId: app_id,
            country: country,
            sort: sort,
            page: i
            })
            .then((body) => {
                let test_name = file_name.slice(0, file_name.length - 5) + "_test.json"
                if ("[]" !== JSON.stringify(body)) {
                    fs.writeFile(test_name, JSON.stringify(body), {flag: 'a'}, (err) => {
                        if (err) {
                            console.error(err)
                        }
                    })
                }
                count += 1
                if (count === page) {
                    fs.readFile(test_name, "utf8", function (err, data) {
                        let new_data = data.replaceAll('][', ', ')
                        if (err) {
                            console.log(err);
                        } else {
                            fs.writeFile(file_name, new_data, (err) => {
                                if (err) {
                                    console.error(err)
                                }
                            })
                        }
                    })
                }
            })
        }
    }
    else
    {
        gplay.reviews({
        appId: app_id,
        lang: lang,
        country: country,
        sort: sort,
        num: num
        })
        .then((body) => {
            fs.writeFile(file_name, JSON.stringify(body), (err) => {
                if (err) {
                    console.error(err)
                }
            })
        })
    }
}

reviews("apple_store", "com.roblox.robloxmobile", "en", "us", "mostRecent", 500, "/Users/anker/MyProject/Python/TopApp/Test.json")