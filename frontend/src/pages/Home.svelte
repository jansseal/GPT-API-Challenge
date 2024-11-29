<script>
  import { navigate } from "svelte-routing";

  // State for sign-in status
  let signedIn = false;

  // User input and dietary restriction
  let searchQuery = "";
  let selectedRestriction = "";
  let generatedRecipe = null;
  let errorMessage = "";
  let recipeName = ""; // New variable to store the recipe name

  // Dietary restriction options
  const restrictions = ["No Dietary Restrictions", "Gluten Free", "Low Calorie", "Keto"];

  // Handle sign-in button click
  function signIn() {
    signedIn = true;
    navigate("/my-fridge");
  }

  // Handle search button click
  async function searchRecipes() {
    const BACKEND_URL = 'http://localhost:5000';
    const data = {
      ingredients: searchQuery,
      dietary_concerns: selectedRestriction || "None",
    };
    console.log("Sending to backend:", JSON.stringify(data));

    try {
      const response = await fetch(`${BACKEND_URL}/api/generate-recipe`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const recipe = await response.json();
      if (recipe.success) {
        recipeName = recipe.recipe_name || 'Generated Recipe'; // Set recipe name
        generatedRecipe = recipe.recipe;
        errorMessage = "";
      } else {
        errorMessage = recipe.error || 'Failed to generate recipe';
        generatedRecipe = null;
      }
    } catch (error) {
      console.error('There was a problem with the fetch operation:', error);
      errorMessage = 'An error occurred while generating the recipe.';
      generatedRecipe = null;
    }
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
    width: 100%;
    max-width: 600px;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
    background-color: #fff;
    text-align: left;
    line-height: 1.6;
    font-size: 1.1em;
    color: #333;
  }

  .recipe-placeholder h3, .recipe-placeholder h4 {
    color: #388E3C;
    margin-bottom: 10px;
  }

  .recipe-placeholder p {
    margin-bottom: 10px;
  }

  .recipe-placeholder ul {
    list-style-type: disc;
    padding-left: 20px;
    margin-bottom: 10px;
  }

  .recipe-placeholder li {
    margin-bottom: 5px;
  }

  .new-recipe-button {
    margin-top: 20px;
    padding: 0.7em;
    background-color: #388E3C;
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-size: 1em;
  }

  .new-recipe-button:hover {
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
      <div class="prompt">What ingredients do you have to cook with today?</div>
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

    <!-- Recipe Display -->
    {#if generatedRecipe}
      <div class="recipe-placeholder">
        <h2>{recipeName || 'Generated Recipe'}</h2> <!-- Display recipe name -->
        {@html generatedRecipe}
        <button class="new-recipe-button" on:click={searchRecipes}>Make New Recipe</button>
      </div>
    {:else if errorMessage}
      <div class="recipe-placeholder">
        <h2>Error</h2>
        <p>{errorMessage}</p>
      </div>
    {/if}
  </div>
</div>