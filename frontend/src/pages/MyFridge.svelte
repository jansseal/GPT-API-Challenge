<script>
  import { navigate } from "svelte-routing";
  import { onMount } from 'svelte';
  let items = [

    { name: 'Avocado', icon: 'fa-avocado', selected: false },
    { name: 'Bottle', icon: 'fa-bottle', selected: false },
    { name: 'Chicken', icon: 'fa-chicken', selected: false },
    { name: 'Corn', icon: 'fa-corn', selected: false },
    { name: 'Cherry', icon: 'fa-cherry', selected: false },
    { name: 'Orange', icon: 'fa-orange', selected: false },
    { name: 'Apple', icon: 'fa-apple', selected: false },
  ];

  const BACKEND_URL = "http://127.0.0.1:5000";
  let selectedIngredients = [];
  let generatedRecipe = null;
  let errorMessage = "";
  let loading = false;

  function deleteItem(index) {
    items = items.filter((_, i) => i !== index);
  }

  function toggleSelect(index) {
    items = items.map((item, i) => {
      if (i === index) {
        const newItem = { ...item, selected: !item.selected };
        if (newItem.selected) {
          selectedIngredients = [...selectedIngredients, newItem.name];
        } else {
          selectedIngredients = selectedIngredients.filter(name => name !== newItem.name);
        }
        return newItem;
      }
      return item;
    });
  }

  function addItem() {
    if (newItem.trim() !== '') {
      items = [...items, { name: newItem, icon: 'fa-plus', selected: false }];
      newItem = '';
    }
  }

  let newItem = '';

  async function handleGenerateRecipe() {
    if (selectedIngredients.length === 0) {
      errorMessage = "Please select ingredients first";
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
        body: JSON.stringify({
          fridge_ingredients: selectedIngredients,
          dietary_concerns: "None"
        }),
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
</script>

<style>

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
  <h1>My Fridge</h1>
  <div class="search-bar">
    <input type="text" class="search-input" bind:value={newItem} placeholder="Add to your Fridge?" />
    <button class="add-btn" on:click={addItem}>Add</button>
  </div>
  <div class="grid">
    {#each items as item, index}
      <div class="item {item.selected ? 'selected' : ''}">
        <div class="item-icon"><i class="fa {item.icon}"></i></div>
        <p>{item.name}</p>
        <div class="buttons">
          <button class="delete-btn" on:click={() => deleteItem(index)}>Delete</button>
          <button class="select-btn" on:click={() => toggleSelect(index)}>
            {item.selected ? 'Remove from List' : 'Add to List'}
          </button>
        </div>
      </div>
    {/each}
  </div>
  <button 
    class="generate-button"
    on:click={handleGenerateRecipe}
    disabled={selectedIngredients.length === 0}>
    Generate Recipe ({selectedIngredients.length} items selected)
  </button>
  {#if loading}
    <div class="loading">Generating recipe...</div>
  {/if}
  {#if generatedRecipe}
    <div class="recipe-placeholder">
      <h2>{generatedRecipe.recipe_name || "Generated Recipe"}</h2>

      <div class="recipe-section">
        <h3>Cooking Time</h3>
        <p>{generatedRecipe.cooking_time} minutes</p>
      </div>

      <div class="recipe-section">
        <h3>Ingredients</h3>
        <ul>
          {#each generatedRecipe.ingredients as ingredient}
            <li>{ingredient.quantity} {ingredient.unit} {ingredient.ingredient}</li>
          {/each}
        </ul>
      </div>

      <div class="recipe-section">
        <h3>Instructions</h3>
        <ol>
          {#each generatedRecipe.instructions as step}
            <li>{step}</li>
          {/each}
        </ol>
      </div>

      <div class="recipe-section">
        <h3>Nutritional Information</h3>
        <ul>
          <li>Calories: {generatedRecipe.nutritional_info.calories}</li>
          <li>Protein: {generatedRecipe.nutritional_info.protein}</li>
          <li>Fat: {generatedRecipe.nutritional_info.fat}</li>
          <li>Carbohydrates: {generatedRecipe.nutritional_info.carbohydrates}</li>
        </ul>
      </div>

      <div class="recipe-section">
        <h3>Cooking Tips</h3>
        <p>{generatedRecipe.cooking_tips}</p>
      </div>

      <button class="new-recipe-button" on:click={() => {
        generatedRecipe = null;
      }}>
        Make New Recipe
      </button>
    </div>
  {:else if errorMessage}
    <div class="recipe-placeholder error">
      <h2>Error</h2>
      <p>{errorMessage}</p>
    </div>
  {/if}
</div>
