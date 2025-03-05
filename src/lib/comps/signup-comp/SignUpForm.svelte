<script lang="ts">
  // bind these values to input so once they're sent they're what user inputted
  let inputData = {
    username: "",
    email: "",
    password: "",
    confirmed_password: "",

  }
  let responseMessage = ""

  // send data from sign-up form to backend 
  async function sendRegistrationData() {
    // try getting authorization from backend to send data
    try {
      // fetch from the localhost auth/register endpoint link; store it in response const
        const response = await fetch("http://127.0.0.1:5000/auth/register", 
          {
            method: "POST",
            headers : { 
              "Content-Type": "application/json"
            },
            // cookies
            credentials: "include", 
            body: JSON.stringify(inputData)
          }
        )
        if (!response.ok) {
          throw new Error(`HTTP while fetching error. Status:${response.status}`);
        }
        
        const responseData = await response.json();
        responseMessage = responseData.msg || "Login successful"; 

        // Show message if data successfully sent
        console.log(responseMessage)

      }
      // grab any error and display it in browser console (for now)
      catch(error){
        console.error(`Failed to fetch data: ${error}`);
      }
  }

</script>

<div class="flex flex-col justify-center items-center min-h-screen">
    <!-- Main Card Component -->
    <a href="/" class="text-4xl mt-8 mb-3 font-medium inline-flex animate-shine bg-[linear-gradient(110deg,#656565,45%,#1e2631,55%,#656565)] bg-[length:200%_100%] text-transparent bg-clip-text">
        DragonFlow
    </a>
    <p class="text-xl mb-10 font-light">
        We care about Your Success.
    </p>

    <div class="card flex flex-col gap-2 max-w-[750px] max-h-[700px] shadow-lg py-7 px-5">

    <h1 class="font-semibold text-lg">Create Your Account</h1>
      <p class="random font-light">This will be your display username</p>
      <label class="input input-bordered flex items-center gap-2">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 16 16"
          fill="currentColor"
          class="h-4 w-4 opacity-70">
          <path
            d="M8 8a3 3 0 1 0 0-6 3 3 0 0 0 0 6ZM12.735 14c.618 0 1.093-.561.872-1.139a6.002 6.002 0 0 0-11.215 0c-.22.578.254 1.139.872 1.139h9.47Z" />
        </svg>
        <input bind:value={inputData.username} type="text" class="grow" placeholder="Username" />
      </label>

      <p>Enter your drexel email</p>
      <label class="input input-bordered flex items-center gap-2">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 16 16"
          fill="currentColor"
          class="h-4 w-4 opacity-70">
          <path
            d="M2.5 3A1.5 1.5 0 0 0 1 4.5v.793c.026.009.051.02.076.032L7.674 8.51c.206.1.446.1.652 0l6.598-3.185A.755.755 0 0 1 15 5.293V4.5A1.5 1.5 0 0 0 13.5 3h-11Z" />
          <path
            d="M15 6.954 8.978 9.86a2.25 2.25 0 0 1-1.956 0L1 6.954V11.5A1.5 1.5 0 0 0 2.5 13h11a1.5 1.5 0 0 0 1.5-1.5V6.954Z" />
        </svg>
        <input bind:value={inputData.email} type="text" class="grow" placeholder="Email" />
      </label>

    <p>Password</p>
      <label class="input input-bordered flex items-center gap-2">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 16 16"
          fill="currentColor"
          class="h-4 w-4 opacity-70">
          <path
            fill-rule="evenodd"
            d="M14 6a4 4 0 0 1-4.899 3.899l-1.955 1.955a.5.5 0 0 1-.353.146H5v1.5a.5.5 0 0 1-.5.5h-2a.5.5 0 0 1-.5-.5v-2.293a.5.5 0 0 1 .146-.353l3.955-3.955A4 4 0 1 1 14 6Zm-4-2a.75.75 0 0 0 0 1.5.5.5 0 0 1 .5.5.75.75 0 0 0 1.5 0 2 2 0 0 0-2-2Z"
            clip-rule="evenodd" />
        </svg>
        <input bind:value={inputData.password} type="password" class="grow text-sm" placeholder="Must be at least 8 characters"/>
      </label>

      <p>Confirm Password</p>
      <label class="input input-bordered flex items-center gap-2">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 16 16"
          fill="currentColor"
          class="h-4 w-4 opacity-70">
          <path
            fill-rule="evenodd"
            d="M14 6a4 4 0 0 1-4.899 3.899l-1.955 1.955a.5.5 0 0 1-.353.146H5v1.5a.5.5 0 0 1-.5.5h-2a.5.5 0 0 1-.5-.5v-2.293a.5.5 0 0 1 .146-.353l3.955-3.955A4 4 0 1 1 14 6Zm-4-2a.75.75 0 0 0 0 1.5.5.5 0 0 1 .5.5.75.75 0 0 0 1.5 0 2 2 0 0 0-2-2Z"
            clip-rule="evenodd" />
        </svg>
        <input bind:value={inputData.confirmed_password} type="password" class="grow" />
      </label>

      <!-- Submit Info -->
        <button on:click={sendRegistrationData} class="bg-zinc-950 text-stone-100 
            px-6 py-2 rounded-3xl mt-2 hover:bg-zinc-900">
            Sign Up 
        </button>
    
    <p class="font-light mt-4">
        Already have an account? 
        <a href="/login" class="text-sky-400 font-light hover:text-sky-300">
            Sign In.
        </a> 
    </p> 
    </div>

</div>


<style>
    .card{
    border-color: rgba(210, 210, 210, 0.357);
    border-width: 2px;
    width: 26rem;
    height: 32rem;
    margin-bottom: 4rem;
    }  

</style>