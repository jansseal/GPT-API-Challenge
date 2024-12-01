<script>
  import { navigate } from "svelte-routing";
  import { user } from "../stores/user";

  const BACKEND_URL = "http://127.0.0.1:5000"; // Replace with your actual backend URL

  // Form data for Sign In
  let signInEmail = "";
  let signInPassword = "";
  let signInErrorMessage = "";

  // Form data for Sign Up
  let signUpName = "";
  let signUpEmail = "";
  let signUpPassword = "";
  let confirmPassword = "";
  let signUpErrorMessage = "";

  // Form data for Edit Profile
  let editName = "";
  let editPassword = "";
  let editConfirmPassword = "";
  let editErrorMessage = "";

  // Handle Sign In
  async function handleSignIn() {
    if (!signInEmail || !signInPassword) {
      signInErrorMessage = "Please enter valid login credentials.";
      return;
    }

    try {
      const response = await fetch(`${BACKEND_URL}/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_email: signInEmail, user_password: signInPassword }),
      });

      const data = await response.json();
      if (response.ok) {
        user.set(data); // Update the user store
        sessionStorage.setItem("user", JSON.stringify(data)); // Save user to sessionStorage
        signInErrorMessage = "";
        alert("Login successful!");
        navigate("/");
      } else {
        signInErrorMessage = data.message || "Login failed.";
      }
    } catch (error) {
      console.error("Error during login:", error);
      signInErrorMessage = "An error occurred. Please try again.";
    }
  }

  // Handle Sign Up
  async function handleSignUp() {
    if (!signUpName || !signUpEmail || !signUpPassword || !confirmPassword) {
      signUpErrorMessage = "Please fill out all fields.";
      return;
    }

    if (signUpPassword !== confirmPassword) {
      signUpErrorMessage = "Passwords do not match!";
      return;
    }

    try {
      const response = await fetch(`${BACKEND_URL}/users`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_name: signUpName,
          user_email: signUpEmail,
          user_password: signUpPassword,
        }),
      });

      const data = await response.json();
      if (response.ok) {
        signUpErrorMessage = "";
        alert("Account created successfully! Please log in.");
        signInEmail = signUpEmail;
        signInPassword = signUpPassword;
      } else {
        signUpErrorMessage = data.message || "Sign-up failed.";
      }
    } catch (error) {
      console.error("Error during sign-up:", error);
      signUpErrorMessage = "An error occurred. Please try again.";
    }
  }

  // Handle Edit Profile
  async function handleEditProfile() {
    if (!editName || !editPassword || !editConfirmPassword) {
      editErrorMessage = "Please fill out all fields.";
      return;
    }

    if (editPassword !== editConfirmPassword) {
      editErrorMessage = "Passwords do not match!";
      return;
    }

    try {
      const response = await fetch(`${BACKEND_URL}/users`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_name: editName,
          new_user_password: editPassword,
          current_user_password: editPassword, // Assuming this is used for validation
        }),
      });

      const data = await response.json();
      if (response.ok) {
        alert("Profile updated successfully!");
        editErrorMessage = "";
        user.set({ ...$user, user_name: editName }); // Update user store
      } else {
        editErrorMessage = data.message || "Failed to update profile.";
      }
    } catch (error) {
      console.error("Error updating profile:", error);
      editErrorMessage = "An error occurred. Please try again.";
    }
  }

  // Handle Delete Profile
  async function handleDeleteProfile() {
    const confirmDelete = confirm("Are you sure you want to delete your profile? This action is irreversible.");
    if (!confirmDelete) return;

    try {
      const response = await fetch(`${BACKEND_URL}/users`, { method: "DELETE" });

      if (response.ok) {
        alert("Profile deleted successfully!");
        user.set(null); // Clear user store
        sessionStorage.removeItem("user");
        navigate("/");
      } else {
        alert("Failed to delete profile.");
      }
    } catch (error) {
      console.error("Error deleting profile:", error);
      alert("An error occurred. Please try again.");
    }
  }
</script>

<style>
  .error-message {
    color: red;
    font-size: 0.9em;
    margin-top: 10px;
  }

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
  {#if $user}
    <!-- Edit Profile Form -->
    <div class="form-box">
      <h2>Edit Profile</h2>
      <form on:submit|preventDefault={handleEditProfile}>
        <input type="text" bind:value={editName} placeholder="New Name" required />
        <input type="password" bind:value={editPassword} placeholder="New Password" required />
        <input type="password" bind:value={editConfirmPassword} placeholder="Confirm Password" required />
        <button type="submit">Update Profile</button>
        {#if editErrorMessage}
          <div class="error-message">{editErrorMessage}</div>
        {/if}
      </form>
      <button on:click={handleDeleteProfile} style="background-color: #FF5252;">Delete Profile</button>
    </div>
  {:else}
    <div class="form-box">
      <h2>Sign In</h2>
      <form on:submit|preventDefault={handleSignIn}>
        <input type="email" bind:value={signInEmail} placeholder="Email" required />
        <input type="password" bind:value={signInPassword} placeholder="Password" required />
        <button type="submit">Sign In</button>
        {#if signInErrorMessage}
          <div class="error-message">{signInErrorMessage}</div>
        {/if}
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
        {#if signUpErrorMessage}
          <div class="error-message">{signUpErrorMessage}</div>
        {/if}
      </form>
    </div>
  {/if}
</div>