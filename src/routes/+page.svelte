<script lang="ts">
  // List of college classes
  let classes = [
      "Introduction to Computer Science",
      "Data Structures and Algorithms",
      "Linear Algebra",
      "Introduction to Psychology",
      "Philosophy of Science",
      "Art History",
      "Introduction to Economics"
  ];

  // Initially selected class
  let selectedClass: string = "None";

  // To toggle dropdown visibility
  let dropdownOpen = false;

  // Function to handle class selection
  function selectClass(className: string) {
      selectedClass = className;
      dropdownOpen = false;  // Close the dropdown after selecting
  }
</script>

<!-- Dropdown Button -->
<div class="dropdown">
  <button class="dropdown-button" on:click={() => dropdownOpen = !dropdownOpen}>
      {dropdownOpen ? "Select a Class" : "Dropdown"}
  </button>

  <!-- Dropdown Menu -->
  {#if dropdownOpen}
      <ul class="dropdown-list">
          {#each classes as className}
              <li>
                  <button class="dropdown-item" on:click={() => selectClass(className)}>
                      {className}
                  </button>
              </li>
          {/each}
      </ul>
  {/if}
</div>

<style>
  .dropdown {
      position: relative;
      display: inline-block;
  }

  .dropdown-button {
      background-color: #4CAF50;
      color: white;
      padding: 10px 20px;
      font-size: 16px;
      border: none;
      border-radius: 5px;
      cursor: pointer;
      width: 200px;
  }

  .dropdown-button:hover {
      background-color: #45a049;
  }

  .dropdown-list {
      position: absolute;
      top: 100%;
      left: 0;
      right: 0;
      background-color: white;
      border: 1px solid #ddd;
      border-radius: 5px;
      box-shadow: 0px 8px 16px rgba(0, 0, 0, 0.2);
      z-index: 1;
      width: 100%;
      margin-top: 5px;
      list-style: none;
      padding: 0;
  }

  .dropdown-item {
      background-color: white;
      color: black;
      padding: 12px 16px;
      text-align: left;
      width: 100%;
      border: none;
      cursor: pointer;
  }

  .dropdown-item:hover {
      background-color: #ddd;
  }

  .dropdown-item:focus {
      outline: none;
  }
</style>