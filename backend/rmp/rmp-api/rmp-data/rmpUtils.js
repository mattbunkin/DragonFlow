// rmpUtils.js
const rmp = require("ratemyprofessor-api");

async function getAvgRating(professorName, schoolId) {
  const data = await rmp.getProfessorRatingAtSchoolId(professorName, schoolId);
  return data?.avgRating;
}

module.exports = { getAvgRating };
// Export the function for use in other modulesq