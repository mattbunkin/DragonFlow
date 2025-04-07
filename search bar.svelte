<script>
    import { onMount } from 'svelte';
  
    let colleges = ['College of Engineering', 'LeBow College of Business', 'College of Computing & Informatics'];
    let selectedCollege = '';
    let classQuery = '';
    let filteredClasses = [];
  
    let classes = {
      'College of Engineering': ['ENGR 101', 'ENGR 102', 'CIVC 101'],
      'LeBow College of Business': ['FIN 301', 'MKTG 212', 'MGMT 210'],
      'College of Computing & Informatics': ['CS 164', 'CS 265', 'INFO 101']
    };
  
    function updateFilteredClasses() {
      if (selectedCollege && classQuery) {
        filteredClasses = classes[selectedCollege].filter(cls =>
          cls.toLowerCase().includes(classQuery.toLowerCase())
        );
      } else {
        filteredClasses = [];
      }
    }
  
    $: updateFilteredClasses();
  </script>
  
  <style>
    .container {
      max-width: 600px;
      margin: 2rem auto;
      padding: 2rem;
      background: #f0f4f8;
      border-radius: 1rem;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
      font-family: Arial, sans-serif;
    }
    h2 {
      margin-bottom: 1rem;
      text-align: center;
    }
    select, input {
      width: 100%;
      padding: 0.75rem;
      margin-bottom: 1rem;
      border: 1px solid #ccc;
      border-radius: 0.5rem;
      font-size: 1rem;
      box-sizing: border-box;
    }
    ul {
      list-style: none;
      padding: 0;
    }
    li {
      padding: 0.5rem;
      background: #fff;
      border: 1px solid #ddd;
      border-radius: 0.5rem;
      margin-bottom: 0.5rem;
    }
    p {
      text-align: center;
      font-style: italic;
    }
  </style>
  
  <div class="container">
    <h2>Search for Your Class</h2>
  
    <select bind:value={selectedCollege}>
      <option value="">-- Select a college --</option>
      {#each colleges as college}
        <option value={college}>{college}</option>
      {/each}
    </select>
  
    <input
      type="text"
      placeholder="Search for a class..."
      bind:value={classQuery}
      disabled={!selectedCollege}
    />
  
    {#if filteredClasses.length > 0}
      <ul>
        {#each filteredClasses as className}
          <li>{className}</li>
        {/each}
      </ul>
    {:else if selectedCollege && classQuery}
      <p>No classes found.</p>
    {/if}
  </div>