const rmp = require("ratemyprofessor-api");

(async () => {
  const school = await rmp.searchSchool("Drexel University");
  if (school !== undefined) {
    const schoolId = school[0].node.id;

    // to search for professors with a name and get all query results
    const DanielMoixSearchResults = await rmp.searchProfessorsAtSchoolId(
      "Daniel Moix",
      schoolId
    );
    
    //console.log(DanielMoixSearchResults);

    //This function will return the average rating of a professor at a specific school
    async function getavgRating(professorName, schoolId) {
        const ratingData = await rmp.getProfessorRatingAtSchoolId(professorName, schoolId);
        return {
            avgRating: ratingData.avgRating
        };
    }


    // This function will return the link to a professor's page at a specific school
    async function getProfessorLink(professorName, schoolId) {
        const ratingData = await rmp.getProfessorRatingAtSchoolId(professorName, schoolId);
        return ratingData.link;
    }
    
    

    // // to search for a professor with a specific name and get only the ratings and other relevant information
    // const DanielMoixRatings = await rmp.getProfessorRatingAtSchoolId(
    //   "Daniel Moix",
    //   schoolId
    // );
    // const boadyRatings =await rmp.getProfessorRatingAtSchoolId(
    //     "Mark Boady",
    //     schoolId
    // );

    
    const moixRating = await getavgRating("Daniel Moix", schoolId);
    const boadyRating = await getavgRating("Mark Boady", schoolId);
    const moixLink = await getProfessorLink("Daniel Moix", schoolId);
    const boadyLink = await getProfessorLink("Mark Boady", schoolId);

    //This is for testing the links and ratings, later we will remove the console logs
    console.log("Daniel Moix's link:");
    console.log(moixLink);
    console.log("Daniel Moix's Rating:");
    console.log(moixRating.avgRating);
    console.log("Mark Boady's link:");
    console.log(boadyLink);
    console.log("Mark Boady's rating:") // e.g., 4.5
    console.log(boadyRating.avgRating)  
} else {
    console.log("unknown school name");
  }
})();