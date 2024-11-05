<script>
  import { Router, Route, Link, navigate } from "svelte-routing";
  import Home from "./pages/Home.svelte";
  import MyFridge from "./pages/MyFridge.svelte";
  import Favorites from "./pages/Favorites.svelte";
  import Profile from "./pages/Profile.svelte";
</script>

<style>
  body {
    font-family: Arial, sans-serif;
    background-color: #A5D6A7;
    background: linear-gradient(135deg, #A5D6A7, #C8E6C9);
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
</style>

<div class="sidebar">
  <button class="sidebar-button" on:click={() => navigate("/")}>Home</button>
  <button class="sidebar-button" on:click={() => navigate("/my-fridge")}>My Fridge</button>
  <button class="sidebar-button" on:click={() => navigate("/profile")}>Profile</button>
  <button class="sidebar-button" on:click={() => navigate("/favorites")}>Favorites (Coming Soon)</button>
</div>

<div class="container">
  <Router>
    <Route path="/" component={Home} />
    <Route path="/my-fridge" component={MyFridge} />
    <Route path="/profile" component={Profile} />
    <Route path="/favorites" component={Favorites} />
  </Router>
</div>
