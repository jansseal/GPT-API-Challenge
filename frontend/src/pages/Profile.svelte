<script>
  import { navigate } from "svelte-routing";

  // Form data for Sign In
  let signInEmail = "";
  let signInPassword = "";

  // Form data for Sign Up
  let signUpName = "";
  let signUpEmail = "";
  let signUpPassword = "";
  let confirmPassword = "";

  // Placeholder function for Sign In
  function handleSignIn() {
    // Simulating a successful login
    if (signInEmail && signInPassword) {
      console.log("Signing in with:", { signInEmail, signInPassword });
      // Replace with actual sign-in logic
      navigate("/profile");
    } else {
      alert("Please enter valid login credentials.");
    }
  }

  // Placeholder function for Sign Up
  function handleSignUp() {
    if (signUpPassword === confirmPassword) {
      console.log("Creating account with:", { signUpName, signUpEmail, signUpPassword });
      // Replace with actual sign-up logic
      navigate("/profile");
    } else {
      alert("Passwords do not match!");
    }
  }
</script>

<style>
  .form-container {
    display: flex;
    justify-content: center;
    gap: 30px;
    margin: 50px auto;
    padding: 20px;
    max-width: 800px;
  }

  .form-box {
    flex: 1;
    background: #ffffff;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
    text-align: center;
  }

  h2 {
    color: #388E3C;
    margin-bottom: 15px;
  }

  input {
    width: 100%;
    padding: 10px;
    margin: 10px 0;
    border: 1px solid #388E3C;
    border-radius: 5px;
  }

  button {
    width: 100%;
    padding: 10px;
    margin-top: 10px;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 1em;
  }

  button:hover {
    background-color: #2E7D32;
  }

  .separator {
    width: 2px;
    background-color: #C8E6C9;
  }
</style>

<div class="form-container">
  <!-- Sign In Form -->
  <div class="form-box">
    <h2>Sign In</h2>
    <form on:submit|preventDefault={handleSignIn}>
      <input type="email" bind:value={signInEmail} placeholder="Email" required />
      <input type="password" bind:value={signInPassword} placeholder="Password" required />
      <button type="submit">Sign In</button>
    </form>
  </div>

  <!-- Separator between forms -->
  <div class="separator"></div>

  <!-- Sign Up Form -->
  <div class="form-box">
    <h2>Create Account</h2>
    <form on:submit|preventDefault={handleSignUp}>
      <input type="text" bind:value={signUpName} placeholder="Name" required />
      <input type="email" bind:value={signUpEmail} placeholder="Email" required />
      <input type="password" bind:value={signUpPassword} placeholder="Password" required />
      <input type="password" bind:value={confirmPassword} placeholder="Confirm Password" required />
      <button type="submit">Create Account</button>
    </form>
  </div>
</div>
