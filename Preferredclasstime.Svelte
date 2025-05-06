<script>
    let classTiming = '';
    let selectedDays = [];
    let unavailableDays = [];
    let errorMessage = '';
  
    const timings = ['Morning', 'Afternoon', 'Evening'];
    const daysOfWeek = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
  
    const submitPreferences = async () => {
      const preferences = {
        timing: classTiming,
        days: selectedDays,
        excludeDays: unavailableDays
      };
  
      const response = await fakeBackend(preferences);
  
      if (!response.success) {
        errorMessage = response.message;
      } else {
        errorMessage = '';
        alert('Preferences submitted successfully!');
      }
    };
  
    const fakeBackend = async (data) => {
      if (!data.timing || data.days.length === 0) {
        return { success: false, message: 'Please select timing and at least one day.' };
      }
  
      if (data.excludeDays.some(day => data.days.includes(day))) {
        return { success: false, message: 'You cannot select and exclude the same day.' };
      }
  
      return { success: true };
    };
  </script>
  
  <div class="container">
    <h2>Class Scheduling Preferences</h2>
  
    <div class="form-group">
      <label>Preferred Class Timing:</label>
      <select bind:value={classTiming}>
        <option value="" disabled>Select timing</option>
        {#each timings as time}
          <option value={time}>{time}</option>
        {/each}
      </select>
    </div>
  
    <div class="form-group">
      <label>Select Days:</label>
      <div class="checkbox-group">
        {#each daysOfWeek as day}
          <label>
            <input type="checkbox" bind:group={selectedDays} value={day}>
            {day}
          </label>
        {/each}
      </div>
    </div>
  
    <div class="form-group">
      <label>Exclude Days (No Class):</label>
      <div class="checkbox-group">
        {#each daysOfWeek as day}
          <label>
            <input type="checkbox" bind:group={unavailableDays} value={day}>
            {day}
          </label>
        {/each}
      </div>
    </div>
  
    {#if errorMessage}
      <div class="error-message">
        {errorMessage}
      </div>
    {/if}
  
    <button on:click={submitPreferences}>Submit Preferences</button>
  </div>
  
  <style>
    .container {
      max-width: 500px;
      margin: 50px auto;
      padding: 20px;
      background-color: #f9f9f9;
      border-radius: 10px;
      box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
      font-family: Arial, sans-serif;
    }
  
    h2 {
      text-align: center;
      color: #333;
      margin-bottom: 20px;
    }
  
    .form-group {
      margin-bottom: 15px;
    }
  
    label {
      display: block;
      font-weight: bold;
      margin-bottom: 8px;
      color: #555;
    }
  
    select,
    button {
      width: 100%;
      padding: 10px;
      border-radius: 5px;
      border: 1px solid #ccc;
    }
  
    .checkbox-group {
      display: flex;
      flex-wrap: wrap;
    }
  
    .checkbox-group label {
      flex: 1 0 45%;
      margin-bottom: 8px;
      font-weight: normal;
    }
  
    button {
      background-color: #4caf50;
      color: white;
      font-size: 16px;
      cursor: pointer;
      border: none;
    }
  
    button:hover {
      background-color: #45a049;
    }
  
    .error-message {
      background-color: #ffcccc;
      color: #a94442;
      padding: 10px;
      border-radius: 5px;
      margin-bottom: 15px;
      text-align: center;
    }
  </style>