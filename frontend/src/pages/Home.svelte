<script>
  import { navigate } from "svelte-routing";

  // State for sign-in status
  let signedIn = false;

  // User input and dietary restriction
  let searchQuery = "";
  let selectedRestriction = "";

  // Dietary restriction options
  const restrictions = ["None", "Gluten Free", "Low Calorie", "Keto"];

  // Handle sign-in button click
  function signIn() {
    signedIn = true;
    navigate("/my-fridge");
  }

  // Handle search button click
  function searchRecipes() {
    const data = {
      input: searchQuery,
      restriction: selectedRestriction || "None",
    };
    console.log("Sending to backend:", JSON.stringify(data));
    // Replace this with actual backend API call
    alert(`Searching with input: "${data.input}" and restriction: "${data.restriction}"`);
  }
</script>

<style>
  .page-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding-top: 20px;
    position: relative;
  }

  .title {
    font-size: 2.5em;
    font-weight: bold;
    margin-bottom: 20px;
    color: #388E3C;
  }

  .content {
    display: flex;
    justify-content: flex-start;
    width: 100%;
    height: 70vh;
    padding-left: 50px;
    flex-direction: column;
    align-items: flex-start;
  }

  .search-section {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
  }

  .prompt {
    font-size: 1.5em;
    font-weight: 500;
    margin-bottom: 10px;
  }

  .search-bar-container {
    display: flex;
    align-items: center;
    gap: 10px;
  }

  .search-input {
    padding: 0.7em;
    width: 300px;
    border: 1px solid #388E3C;
    border-radius: 8px;
    font-size: 1em;
    outline: none;
  }

  .search-button {
    padding: 0.7em;
    background-color: #388E3C;
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-size: 1em;
  }

  .search-button:hover {
    background-color: #2E7D32;
  }

  .restriction-dropdown {
    padding: 0.7em;
    border: 1px solid #388E3C;
    border-radius: 8px;
    font-size: 1em;
  }

  .sign-in-button {
    position: absolute;
    top: 20px;
    right: 20px;
    background-color: #007BFF;
    color: white;
    padding: 10px 20px;
    border-radius: 8px;
    border: none;
    cursor: pointer;
  }

  .sign-in-button:hover {
    background-color: #0056b3;
  }

  .sign-in-message {
    margin-top: 10px;
    font-size: 0.9em;
    color: #555;
  }

  .recipe-placeholder {
    margin-top: 20px;
    width: 370px;
    padding: 15px;
    border-radius: 8px;
    box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
    background-color: #fff;
    text-align: left;
    position: relative;
  }

  .dice-button {
    position: absolute;
    top: -20px;
    left: -20px;
    background-color: #388E3C;
    color: white;
    border: none;
    border-radius: 50%;
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
    font-size: 1.2em;
  }

  .dice-button:hover {
    background-color: #2E7D32;
  }
</style>

<div class="page-container">
  <!-- Sign-In Button -->
  {#if !signedIn}
    <button class="sign-in-button" on:click={() => navigate('/profile')}>
      Sign In
    </button>
  {/if}


  <!-- Website Title -->
  <div class="title">Fridge-Raider</div>

  <!-- Content Area -->
  <div class="content">
    <div class="search-section">
      <div class="prompt">What would you like to cook with today?</div>
      <div class="search-bar-container">
        <!-- Search Input -->
        <input
          type="text"
          bind:value={searchQuery}
          class="search-input"
          placeholder="Search ingredients..."
        />
        <!-- Restriction Dropdown -->
        <select bind:value={selectedRestriction} class="restriction-dropdown">
          {#each restrictions as restriction}
            <option value={restriction}>{restriction}</option>
          {/each}
        </select>
        <!-- Search Button -->
        <button class="search-button" on:click={searchRecipes}>Search</button>
      </div>
      <!-- Sign-In Message for Guests -->
      {#if !signedIn}
  <div class="sign-in-message">
    Sign in to save ingredients for faster recipe suggestions.
  </div>
{/if}
    </div>

    <!-- Recipe Placeholder -->
    <div class="recipe-placeholder">
      <button class="dice-button" title="Get a Random Recipe">🎲</button>
      <h2>Random Recipe</h2>
      <p>Recipe name: Placeholder Recipe</p>
      <p>Ingredients: Avocado, Chicken, Corn</p>
      <p>Instructions: Mix ingredients and cook.</p>
    </div>
  </div>
</div>
