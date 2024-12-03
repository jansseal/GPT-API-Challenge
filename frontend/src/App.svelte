<script>
  import { Router, Route, navigate } from "svelte-routing";
  import { user } from "./stores/user"; // Import user store
  import Home from "./pages/Home.svelte";
  import MyFridge from "./pages/MyFridge.svelte";
  import Favorites from "./pages/Favorites.svelte";
  import Profile from "./pages/Profile.svelte";

  // Load user from sessionStorage on app load
  if (sessionStorage.getItem("user")) {
    user.set(JSON.parse(sessionStorage.getItem("user")));
  }

  const disclaimerText = `
    Note: The recipes and suggestions provided by this app are AI-generated.
    Always verify the safety and suitability of ingredients and instructions
    according to your dietary needs, allergies, or preferences.
  `;

  function logout() {
    sessionStorage.removeItem("user");
    user.set(null);
    navigate("/");
    alert("Logged out successfully.");
  }
</script>

<style>
  :global(body) {
    font-family: Arial, sans-serif;
    background-color: #A5D6A7;
    background: linear-gradient(135deg, #A5D6A7, #C8E6C9);
  }

  .container {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20px;
    margin-left: 100px;
    background-color: #C8E6C9;
    border-radius: 10px;
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
  }

  .sidebar-button:hover {
    background-color: #2E7D32;
  }

  .disclaimer {
    margin-top: 20px;
    padding: 10px;
    font-size: 0.9em;
    color: #555;
    background-color: #f9f9f9;
    border-left: 4px solid #388E3C;
    max-width: 90%;
    text-align: center;
    border-radius: 8px;
    box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1);
  }
</style>

<div class="sidebar">
  {#if $user}
    <p>Welcome, {$user.user_name}</p>
    <button class="sidebar-button" on:click={logout}>Logout</button>
  {/if}
  <button class="sidebar-button" on:click={() => navigate("/")}>Home</button>
  <button class="sidebar-button" on:click={() => navigate("/my-fridge")}>My Fridge</button>
  <button class="sidebar-button" on:click={() => navigate("/profile")}>Profile</button>
  <button class="sidebar-button" on:click={() => navigate("/favorites")}>Favorites</button>
</div>

<div class="container">
  <Router>
    <Route path="/" component={Home} />
    <Route path="/my-fridge" component={MyFridge} />
    <Route path="/profile" component={Profile} />
    <Route path="/favorites" component={Favorites} />
  </Router>

  <div class="disclaimer">{disclaimerText}</div>
</div>
