const rmp = require("ratemyprofessor-api");

// Helper function to get professor info
async function getProfessorInfo(profName) {
  try {
    const schoolSearchResults = await rmp.searchSchool("Drexel University");
    
    if (!schoolSearchResults?.length) {
      return { error: "School not found" };
    }
    
    const schoolId = schoolSearchResults[0].node.id;
    const data = await rmp.getProfessorRatingAtSchoolId(profName, schoolId);
    
    if (!data) {
      return { error: "Professor not found" };
    }
    
    return {
      avgRating: data.avgRating || 0,
      link: data.link || "",
      department: data.department || ""
    };
  } catch (error) {
    return { error: error.message };
  }
}

// Get professor name from command line arguments
const professorName = process.argv[2];

if (professorName) {
  getProfessorInfo(professorName)
    .then(result => {
      // Output as JSON so Flask can parse it
      console.log(JSON.stringify(result));
    })
    .catch(error => {
      console.error(JSON.stringify({ error: error.message }));
    });
} else {
  console.log(JSON.stringify({ error: "No professor name provided" }));
}