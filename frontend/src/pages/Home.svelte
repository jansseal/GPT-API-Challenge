<script>
  let searchQuery = "";

  function getRandomRecipe() {
    alert("Fetching a new random recipe!");
  }

  function searchRecipes() {
    alert("Searching for recipes with: " + searchQuery);
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
    flex-direction: column;
    align-items: flex-start;
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

  /* Search button styling */
  .search-button {
    padding: 0.7em;
    margin-left: 10px;
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

  /* Recipe placeholder box styling */
  .recipe-placeholder {
    margin-top: 20px;
    width: 370px; /* Matches width of search input and button */
    padding: 15px;
    border-radius: 8px;
    box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
    background-color: #fff;
    text-align: left;
    position: relative;
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

  /* Dice button styling inside recipe placeholder */
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
  <!-- Website title centered at the top -->
  <div class="title">Fridge-Raider</div>

  <!-- Content area for search section -->
  <div class="content">
    <div class="search-section">
      <div class="prompt">What would you like to cook with today?</div>
      <div style="display: flex; align-items: center;">
        <input
          type="text"
          bind:value={searchQuery}
          class="search-input"
          placeholder="Search ingredients..."
        />
        <button class="search-button" on:click="{searchRecipes}">Search</button>
      </div>
    </div>

    <!-- Recipe Placeholder positioned below the search bar -->
    <div class="recipe-placeholder">
      <!-- Dice button in the top-left corner of recipe placeholder -->
      <button class="dice-button" on:click="{getRandomRecipe}" title="Get a Random Recipe">
        🎲
      </button>
      <h2>Random Recipe</h2>
      <p>Recipe name: Placeholder Recipe</p>
      <p>Ingredients: Avocado, Chicken, Corn</p>
      <p>Instructions: Mix ingredients and cook.</p>
    </div>
  </div>
</div>

