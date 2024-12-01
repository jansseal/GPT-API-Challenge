<script>
  import { navigate } from "svelte-routing";
  import { user } from "../stores/user"; // Import user store

  // Check user login state
  $: signedIn = $user !== null;

  let searchQuery = "";
  let selectedRestriction = "No Dietary Restrictions";
  let generatedRecipe = null;
  let errorMessage = "";
  let loading = false;

  const restrictions = [
    "No Dietary Restrictions",
    "Gluten Free",
    "Low Calorie",
    "Keto",
    "Vegetarian",
    "Vegan",
    "Pescatarian",
    "Dairy Free",
    "Nut Free",
    "Paleo",
    "Low Carb"
  ];

  const BACKEND_URL = process.env.VITE_API_URL;

  async function searchRecipes() {

    const data = {
      ingredients: searchQuery,
      dietary_concerns: selectedRestriction || "None",
    };

    loading = true;
    errorMessage = "";
    generatedRecipe = null;

    try {
      const response = await fetch(`${BACKEND_URL}/api/generate-recipe`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        throw new Error("Network response was not ok");
      }

      const recipe = await response.json();
      if (recipe.success) {
        generatedRecipe = recipe.recipe;
      } else {
        errorMessage = recipe.error || "Failed to generate recipe";
      }
    } catch (error) {
      errorMessage = "An error occurred while generating the recipe.";
    } finally {
      loading = false;
    }
  }
</script>

<style>
  .page-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding-top: 20px;
    padding-bottom: 50px; /* Add extra space at the bottom */
    position: relative;
    min-height: 100vh; /* Ensures it covers at least the viewport height */
    box-sizing: border-box; /* Includes padding in height calculations */
  }
  .title {
    font-size: 2.5em;
    font-weight: bold;
    margin-bottom: 20px;
    color: #388e3c;
  }
  .content {
    display: flex;
    justify-content: flex-start;
    width: 100%;
    flex-direction: column;
    align-items: center;
    padding: 20px;
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
    padding: 0.8em;
    width: 300px;
    border: 1px solid #388e3c;
    border-radius: 8px;
    font-size: 1em;
    outline: none;
  }
  .restriction-dropdown {
    padding: 0.8em;
    border: 1px solid #388e3c;
    border-radius: 8px;
    font-size: 1em;
  }
  .search-button {
    padding: 0.7em;
    background-color: #388e3c;
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-size: 1em;
  }
  .search-button:hover {
    background-color: #2e7d32;
  }
  .sign-in-button {
    position: absolute;
    top: 20px;
    right: 20px;
    background-color: #007bff;
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
    width: 90%;
    max-width: 1200px;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
    background-color: #fff;
    text-align: left;
    line-height: 1.4;
    font-size: 1em;
    color: #333;
    border: 1px solid #ccc;
    height: auto; /* Ensure the height adjusts to content */
    overflow: visible; /* Prevent clipping or scrolling */
  }
  .recipe-placeholder ul, .recipe-placeholder ol {
    margin: 10px 0;
    padding-left: 20px;
    list-style-position: inside; /* Keep items within the container */
  }
  .recipe-placeholder ul {
    list-style-type: disc; /* Standard bullet points */
  }
  .recipe-placeholder ol {
    list-style-type: decimal; /* Numbered steps for instructions */
  }
  .loading {
    margin: 10px 0;
    font-size: 1em;
    color: #388e3c;
  }
  .new-recipe-button {
    margin-top: 20px;
    padding: 0.7em;
    background-color: #388e3c;
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-size: 1em;
  }
  .new-recipe-button:hover {
    background-color: #2e7d32;
  }
</style>


<div class="page-container">
  <!-- Sign-In Button -->
  {#if !signedIn}
    <button class="sign-in-button" on:click={() => navigate("/profile")}>
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
        <input
          type="text"
          bind:value={searchQuery}
          class="search-input"
          placeholder="Search ingredients..."
          aria-label="Search ingredients input"
        />
        <select
          bind:value={selectedRestriction}
          class="restriction-dropdown"
          aria-label="Dietary restriction selection"
        >
          {#each restrictions as restriction}
            <option value={restriction}>{restriction}</option>
          {/each}
        </select>
        <button
          class="search-button"
          on:click={searchRecipes}
          aria-label="Search recipes button"
        >
          Search
        </button>
      </div>
      {#if !signedIn}
        <div class="sign-in-message">
          Sign in to save ingredients for faster recipe suggestions.
        </div>
      {:else}
        <div class="sign-in-message">
          Welcome back! Ready to generate a recipe?
        </div>
      {/if}
    </div>

    {#if loading}
      <div class="loading">Loading...</div>
    {/if}

    {#if generatedRecipe}
      <div class="recipe-placeholder">
        <!-- Recipe content remains unchanged -->
      </div>
    {:else if errorMessage}
      <div class="recipe-placeholder error">
        <h2>Error</h2>
        <p>{errorMessage}</p>
      </div>
    {/if}
  </div>
</div>
