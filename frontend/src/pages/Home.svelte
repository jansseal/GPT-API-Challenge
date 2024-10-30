<script>
  let searchQuery = "";

  function getRandomRecipe() {
    alert("Fetching a new random recipe!");
  }
</script>

<style>
  /* Main page layout */
  .page-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding-top: 20px;
    position: relative;
  }

  /* Website title styling */
  .title {
    font-size: 2.5em;
    font-weight: bold;
    margin-bottom: 20px;
    color: #388E3C;
  }

  /* Layout for the main content below the title */
  .content {
    display: flex;
    justify-content: flex-start;
    width: 100%;
    height: 70vh;
    padding-left: 50px;
  }

  /* Search Section Styling */
  .search-section {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: flex-start;
  }

  /* Prompt text styling */
  .prompt {
    font-size: 1.5em;
    font-weight: 500;
    margin-bottom: 10px;
  }

  /* Search input box styling */
  .search-input {
    padding: 0.7em;
    width: 300px;
    border: 1px solid #388E3C;
    border-radius: 8px;
    font-size: 1em;
    outline: none;
  }

  /* Recipe placeholder box styling */
  .recipe-placeholder {
    position: fixed;
    top: 20px;
    right: 20px;
    width: 250px;
    padding: 15px;
    border-radius: 8px;
    box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
    background-color: #fff;
    text-align: left;
  }

  /* Recipe placeholder title styling */
  .recipe-placeholder h2 {
    font-size: 1.2em;
    color: #388E3C;
    margin-bottom: 10px;
  }

  /* Placeholder description text styling */
  .recipe-placeholder p {
    font-size: 0.9em;
    color: #555;
  }

  /* Dice button styling */
  .dice-button {
    position: fixed;
    top: 170px; /* Increase this value to position it further below the recipe card */
    right: 20px;
    background-color: #388E3C;
    color: white;
    border: none;
    border-radius: 50%;
    width: 50px;
    height: 50px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
    font-size: 1.5em;
  }

  .dice-button:hover {
    background-color: #2E7D32;
  }
</style>

<div class="page-container">
  <!-- Website title centered at the top -->
  <div class="title">Fridge-Raider</div>

  <!-- Content area for search section -->
  <div class="content">
    <div class="search-section">
      <div class="prompt">What would you like to cook with today?</div>
      <input
        type="text"
        bind:value={searchQuery}
        class="search-input"
        placeholder="Search ingredients..."
      />
    </div>
  </div>

  <!-- Recipe Placeholder positioned in the top right -->
  <div class="recipe-placeholder">
    <h2>Random Recipe</h2>
    <p>Recipe name: Placeholder Recipe</p>
    <p>Ingredients: Avocado, Chicken, Corn</p>
    <p>Instructions: Mix ingredients and cook.</p>
  </div>

  <!-- Dice button positioned directly below the recipe placeholder -->
  <button class="dice-button" on:click={getRandomRecipe} title="Get a Random Recipe">
    🎲
  </button>
</div>
