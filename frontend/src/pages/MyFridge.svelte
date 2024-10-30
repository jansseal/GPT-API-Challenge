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

  function deleteItem(index) {
    items = items.filter((_, i) => i !== index);
  }

  function toggleSelect(index) {
    items = items.map((item, i) => {
      if (i === index) {
        return { ...item, selected: !item.selected };
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
</div>
