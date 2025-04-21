// get_rating.js
const { getAvgRating } = require("./rmpUtils");

const DREXEL_ID = "U2Nob29sLTE1MTI="; // <- Drexel's school ID

(async () => {
  const profName = process.argv[2];
  if (!profName) {
    console.log(JSON.stringify({ error: "Missing professor name" }));
    return;
  }

  const rating = await getAvgRating(profName, DREXEL_ID);
  console.log(JSON.stringify({ rating: rating ?? "Not found" }));
})();
