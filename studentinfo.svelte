<script>
    let student = {
      name: '',
      major: '',
      year: ''
    };
  
    let errors = {
      name: '',
      major: '',
      year: ''
    };
  
    function validate() {
      errors = {
        name: student.name.trim() ? '' : 'Name is required.',
        major: student.major.trim() ? '' : 'Major is required.',
        year: /^\d{4}$/.test(student.year) ? '' : 'Enter a valid 4-digit year.'
      };
  
      const hasErrors = Object.values(errors).some(error => error !== '');
      if (!hasErrors) {
        alert(`✅ Submitted:\n${student.name} | ${student.major} | ${student.year}`);
      }
    }
  </script>
  
  <style>
    .wrapper {
      max-width: 480px;
      margin: 3rem auto;
      background: #f9fafb;
      padding: 2rem;
      border-radius: 1rem;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
      font-family: system-ui, sans-serif;
    }
  
    h2 {
      text-align: center;
      margin-bottom: 1.5rem;
      font-size: 1.5rem;
      color: #333;
    }
  
    label {
      display: block;
      margin-top: 1rem;
      font-weight: 600;
      color: #444;
    }
  
    input {
      width: 100%;
      padding: 0.7rem;
      margin-top: 0.4rem;
      border: 1px solid #ccc;
      border-radius: 0.5rem;
      font-size: 1rem;
      transition: border 0.2s;
    }
  
    input:focus {
      outline: none;
      border-color: #0070f3;
    }
  
    .error {
      color: #c00;
      font-size: 0.9rem;
      margin-top: 0.25rem;
    }
  
    button {
      margin-top: 2rem;
      width: 100%;
      padding: 0.9rem;
      background-color: #0070f3;
      color: white;
      border: none;
      border-radius: 0.5rem;
      font-size: 1rem;
      cursor: pointer;
      font-weight: bold;
    }
  
    button:hover {
      background-color: #0059c1;
    }
  </style>
  
  <div class="wrapper">
    <h2>Course Scheduler Validation</h2>
  
    <label for="name">Student Name</label>
    <input id="name" bind:value={student.name} placeholder="e.g. Sam Smith" />
    {#if errors.name}<div class="error">{errors.name}</div>{/if}
  
    <label for="major">Major</label>
    <input id="major" bind:value={student.major} placeholder="e.g. Cybersecurity" />
    {#if errors.major}<div class="error">{errors.major}</div>{/if}
  
    <label for="year">Year</label>
    <input id="year" bind:value={student.year} placeholder="e.g. 2027" />
    {#if errors.year}<div class="error">{errors.year}</div>{/if}
  
    <button on:click={validate}>Submit</button>
  </div>
  