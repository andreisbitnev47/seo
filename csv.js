const fs = require('fs'); 
const parse = require('csv-parse');
const filePath = '/home/andrei/projects/seo/ebay-sold.csv';

const csvData=[];
fs.createReadStream(filePath)
    .pipe(parse({delimiter: ','}))
    .on('data', function(csvrow) {
        console.log(csvrow);
        csvData.push(csvrow);        
    })
    .on('end',function() {
      console.log('asd');
    });

// csv.generate({seed: 1, columns: 2, length: 20}, function(err, data){
//   csv.parse(data, function(err, data){
//     csv.transform(data, function(data){
//       return data.map(function(value){return value.toUpperCase()});
//     }, function(err, data){
//       csv.stringify(data, function(err, data){
//         process.stdout.write(data);
//       });
//     });
//   });
// });