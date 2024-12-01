<script>
  import { navigate } from "svelte-routing";
  import { user } from "../App.svelte";

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
      console.error("There was a problem with the fetch operation:", error);
      errorMessage = "An error occurred while generating the recipe.";
    } finally {
      loading = false;
    }
  }

  async function generateRecipeFromFridge(ingredientsList) {

    const data = {
      fridge_ingredients: ingredientsList,
      dietary_concerns: selectedRestriction || "None",
    };

    loading = true;
    errorMessage = "";
    generatedRecipe = null;

    try {
      const response = await fetch(`${BACKEND_URL}/api/generate-recipe-from-fridge`, {
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
        errorMessage = recipe.error || "Failed to generate recipe from fridge ingredients";
      }
    } catch (error) {
      console.error("There was a problem with the fetch operation:", error);
      errorMessage = "An error occurred while generating the recipe.";
    } finally {
      loading = false;
    }
  }
</script>

<style>
  /* Your existing styles remain unchanged */
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
