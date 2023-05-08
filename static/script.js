// const options = {
//   method: 'GET',
//   url: 'https://the-cocktail-db.p.rapidapi.com/random.php',
//   headers: {
//     'X-RapidAPI-Key': '1f4b3e251bmshb1df2538c036ddfp1c6675jsn19129a6f9614',
//     'X-RapidAPI-Host': 'the-cocktail-db.p.rapidapi.com'
//   }
// };

// axios.request(options).then(function (response) {
//   returnArr = {}
//   const val = response.data.drinks
//   for (let i=0; i<Object.keys(val[0]).length; i++) {
//     if (Object.values(val[0])[i] != null) {
//       returnArr[Object.keys(val[0])[i]] = Object.values(val[0])[i]
//     }
//   }

// 	console.log(returnArr);
// }).catch(function (error) {
// 	console.error(error);
// });

const options = {
  method: 'GET',
  url: 'https://the-cocktail-db.p.rapidapi.com/search.php',
  params: {s: 'Mojito'},
  headers: {
    'X-RapidAPI-Key': '1f4b3e251bmshb1df2538c036ddfp1c6675jsn19129a6f9614',
    'X-RapidAPI-Host': 'the-cocktail-db.p.rapidapi.com'
  }
};

axios.request(options).then(function (response) {
	console.log(response.data.drinks[0]);
}).catch(function (error) {
	console.error(error);
});