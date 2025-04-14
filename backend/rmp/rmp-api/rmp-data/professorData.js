const rmp = require("ratemyprofessor-api");

// Helper function to get average rating
async function getAvgRating(professorName, schoolId) {
  const data = await rmp.getProfessorRatingAtSchoolId(professorName, schoolId);
  return data?.avgRating;
}

// Helper function to get professor's RMP link
async function getProfessorLink(professorName, schoolId) {
  const data = await rmp.getProfessorRatingAtSchoolId(professorName, schoolId);
  return data?.link;
}

// Helper function to fetch and display a professor's info
async function displayProfessorInfo(profName, schoolId) {
  const rating = await getAvgRating(profName, schoolId);
  const link = await getProfessorLink(profName, schoolId);

  console.log(`\nProfessor: ${profName}`);
  console.log(`Rating: ${rating ?? "Not found"}`);
  console.log(`Link: ${link ?? "Not available"}`);
}

(async () => {
  const schoolSearchResults = await rmp.searchSchool("Drexel University");
  //Error is displayed if a school is not found
  if (!schoolSearchResults?.length) {
    console.log("School not found.");
    return;
  }

  const schoolId = schoolSearchResults[0].node.id;
  
  //Test the functionality of the API using CCI professors
  await displayProfessorInfo("Tammy Pirmann", schoolId);
  await displayProfessorInfo("Mark Boady", schoolId);
})();
