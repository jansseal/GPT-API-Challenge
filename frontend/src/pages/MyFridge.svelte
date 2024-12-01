<script>
  import { navigate } from "svelte-routing";
  import { onMount } from "svelte";
  import { user } from "../stores/user";

  const BACKEND_URL = process.env.VITE_API_URL;
  let selectedIngredients = [];
  let generatedRecipe = null;
  let errorMessage = "";
  let loading = false;
  let newItem = "";

  // Fetch ingredients for the user's profile
  async function fetchIngredients() {
    if (!$user) {
      return; // Skip loading ingredients if the user is not signed in
    }
    try {
      const response = await fetch(`${BACKEND_URL}/ingredients`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
      });

      if (!response.ok) {
        throw new Error("Failed to load ingredients.");
      }

      items = await response.json();
    } catch (error) {
      console.error("Error fetching ingredients:", error);
      errorMessage = "Unable to load your fridge items. Please try again.";
    }
  }

  // Add a new ingredient to the fridge
  async function addItem() {
    if (newItem.trim() === "") {
      errorMessage = "Ingredient name cannot be empty.";
      return;
    }

    try {
      const response = await fetch(`${BACKEND_URL}/ingredients`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
        body: JSON.stringify({ ingredient_name: newItem }),
      });

      if (!response.ok) {
        throw new Error("Failed to add ingredient.");
      }

      const addedIngredient = await response.json();
      items = [...items, addedIngredient]; // Update the list locally
      newItem = "";
      errorMessage = "";
    } catch (error) {
      console.error("Error adding ingredient:", error);
      errorMessage = "Failed to add the ingredient. Please try again.";
    }
  }

  // Delete an ingredient from the fridge
  async function deleteItem(ingredientId) {
    try {
      const response = await fetch(`${BACKEND_URL}/ingredients/${ingredientId}`, {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
      });

      if (!response.ok) {
        throw new Error("Failed to delete ingredient.");
      }

      items = items.filter((item) => item.id !== ingredientId); // Remove locally
      errorMessage = "";
    } catch (error) {
      console.error("Error deleting ingredient:", error);
      errorMessage = "Failed to delete the ingredient. Please try again.";
    }
  }

  // Toggle ingredient selection
  function toggleSelect(index) {
    items = items.map((item, i) => {
      if (i === index) {
        const updatedItem = { ...item, selected: !item.selected };
        if (updatedItem.selected) {
          selectedIngredients = [...selectedIngredients, updatedItem.name];
        } else {
          selectedIngredients = selectedIngredients.filter(
            (name) => name !== updatedItem.name
          );
        }
        return updatedItem;
      }
      return item;
    });
  }

  // Generate recipe based on selected ingredients
  async function handleGenerateRecipe() {
    if (selectedIngredients.length === 0) {
      errorMessage = "Please select ingredients first.";
      return;
    }

    loading = true;
    errorMessage = "";
    generatedRecipe = null;

    try {
      const response = await fetch(`${BACKEND_URL}/api/generate-recipe-from-fridge`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
        body: JSON.stringify({
          fridge_ingredients: selectedIngredients,
          dietary_concerns: "None",
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to generate recipe.");
      }

      const recipe = await response.json();
      if (recipe.success) {
        generatedRecipe = recipe.recipe;
      } else {
        errorMessage = recipe.error || "Failed to generate recipe.";
      }
    } catch (error) {
      console.error("Error generating recipe:", error);
      errorMessage = "An error occurred while generating the recipe.";
    } finally {
      loading = false;
    }
  }

  // Load ingredients when the component mounts
  onMount(fetchIngredients);
</script>

<style>
  .sign-in-prompt {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background-color: #fff3cd; /* Light yellow background */
    color: #856404; /* Dark yellow text */
    padding: 20px;
    margin: 50px auto;
    border: 1px solid #ffeeba;
    border-radius: 10px;
    text-align: center;
    max-width: 500px;
    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
  }

  .sign-in-prompt h2 {
    font-size: 1.5em;
    margin-bottom: 15px;
  }

  .sign-in-btn {
    padding: 10px 20px;
    font-size: 1em;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s ease;
    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
  }

  .sign-in-btn:hover {
    background-color: #0056b3;
  }

  .container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  margin-left: 100px; /* Adjusted for sidebar */
  background-color: #C8E6C9; /* Light green background */
  border-radius: 10px;
}

  .grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 15px;
    margin: 20px;
  }

  .item {
    background-color: #ffffff;
    border-radius: 10px;
    padding: 20px;
    text-align: center;
    box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
    position: relative;
  }

  .item-icon {
    font-size: 3em;
  }

  .buttons {
    display: flex;
    justify-content: space-between;
    margin-top: 10px;
  }

  .delete-btn {
    background-color: #FF5252;
    color: white;
    border: none;
    padding: 5px 10px;
    border-radius: 5px;
    cursor: pointer;
  }

  .select-btn {
    background-color: #4CAF50;
    color: white;
    border: none;
    padding: 5px 10px;
    border-radius: 5px;
    cursor: pointer;
  }

  .selected {
    box-shadow: 0px 4px 8px rgba(255, 165, 0, 0.8);
  }

  .sidebar {
    position: fixed;
    left: 0;
    top: 0;
    bottom: 0;
    width: 80px;
    background-color: #388E3C;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20px 0;
  }

  .sidebar-button {
    margin: 10px 0;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 8px;
    width: 60px;
    height: 60px;
    font-size: 0.8em;
    cursor: pointer;
    box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
  }

  .sidebar-button:hover {
    background-color: #2E7D32;
  }

  .search-bar {
    margin-top: 20px;
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .search-input {
    padding: 0.7em;
    width: 300px;
    border: 1px solid #388E3C;
    border-radius: 8px;
    font-size: 1em;
  }

  .add-btn {
    margin-left: 10px;
    padding: 0.7em;
    font-size: 1em;
    border: none;
    border-radius: 8px;
    background-color: #007BFF;
    color: white;
    cursor: pointer;
    box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
  }

  .add-btn:hover {
    background-color: #0056b3;
  }

  .grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr); /* Default to 4 columns */
    gap: 15px;
    margin: 20px;
  }

  /* Adjust grid columns on medium screens */
  @media (max-width: 900px) {
    .grid {
      grid-template-columns: repeat(2, 1fr); /* 2 columns on medium screens */
    }
  }

  /* Adjust grid columns on small screens */
  @media (max-width: 600px) {
    .grid {
      grid-template-columns: repeat(1, 1fr); /* 1 column on small screens */
    }
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
  }

  .recipe-section {
    margin: 20px 0;
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

  .generate-button {
    margin-top: 20px;
    padding: 10px 20px;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-size: 1em;
  }

  .generate-button:disabled {
    background-color: #cccccc;
    cursor: not-allowed;
  }

  .loading {
    margin-top: 20px;
    color: #666;
    font-style: italic;
  }
</style>
<div class="container">
  {#if !$user}
    <!-- Styled prompt to sign in -->
    <div class="sign-in-prompt">
      <h2>Please sign in to use the My Fridge feature.</h2>
      <button class="sign-in-btn" on:click={() => navigate("/profile")}>Sign In</button>
    </div>
  {:else}
    <h1>My Fridge</h1>
    <div class="search-bar">
      <input
        type="text"
        class="search-input"
        bind:value={newItem}
        placeholder="Add to your Fridge?"
      />
      <button class="add-btn" on:click={addItem}>Add</button>
    </div>
    <div class="grid">
      {#each items as item, index}
        <div class="item {item.selected ? 'selected' : ''}">
          <p>{item.name}</p>
          <div class="buttons">
            <button class="delete-btn" on:click={() => deleteItem(item.id)}>Delete</button>
            <button class="select-btn" on:click={() => toggleSelect(index)}>
              {item.selected ? "Remove from List" : "Add to List"}
            </button>
          </div>
        </div>
      {/each}
    </div>
    <button
      class="generate-button"
      on:click={handleGenerateRecipe}
      disabled={selectedIngredients.length === 0}
    >
      Generate Recipe ({selectedIngredients.length} items selected)
    </button>
    {#if loading}
      <div class="loading">Generating recipe...</div>
    {/if}
    {#if generatedRecipe}
      <div class="recipe-placeholder">
        <h2>{generatedRecipe.recipe_name || "Generated Recipe"}</h2>
        <!-- Recipe content here -->
      </div>
    {:else if errorMessage}
      <div class="recipe-placeholder error">
        <h2>Error</h2>
        <p>{errorMessage}</p>
      </div>
    {/if}
  {/if}
</div>