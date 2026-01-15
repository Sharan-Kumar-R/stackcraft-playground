# Testing the Redis Flask App

This guide will help you verify all the features of the application, including the new Leaderboard and Self-Destructing Message features.

## Prerequisites
1.  Ensure Redis is running (`redis-server` or via Services).
2.  Start the Flask app:
    ```bash
    python app.py
    ```

---

## 1. Basic Features (Strings & Counters)

| Feature | Action | URL to Visit | Expected Result |
| :--- | :--- | :--- | :--- |
| **Home Page** | Check connection | [http://localhost:5000/](http://localhost:5000/) | `Redis is running on Windows!` |
| **Visit Counter** | Increment count | [http://localhost:5000/visit](http://localhost:5000/visit) | `Total visits: X` (Increases on refresh) |
| **Set String** | Save a value | [http://localhost:5000/set/mykey/hello](http://localhost:5000/set/mykey/hello) | `Saved mykey = hello` |
| **Get String** | Retrieve value | [http://localhost:5000/get/mykey](http://localhost:5000/get/mykey) | `mykey = hello` |

---

## 2. 🏆 Leaderboard (Sorted Sets)

This feature uses Redis `Sorted Sets` to maintain a ranking of players.

### Step 1: Add Players
Visit these URLs to add players with different scores:
*   **Add Alice (100 pts)**: [http://localhost:5000/leaderboard/add/Alice/100](http://localhost:5000/leaderboard/add/Alice/100)
*   **Add Bob (500 pts)**: [http://localhost:5000/leaderboard/add/Bob/500](http://localhost:5000/leaderboard/add/Bob/500)
*   **Add Charlie (300 pts)**: [http://localhost:5000/leaderboard/add/Charlie/300](http://localhost:5000/leaderboard/add/Charlie/300)

### Step 2: View Leaderboard
*   **Check Rankings**: [http://localhost:5000/leaderboard](http://localhost:5000/leaderboard)
    *   **Expected Output**:
        1.  Bob: 500
        2.  Charlie: 300
        3.  Alice: 100

---

## 3. ⏳ Self-Destructing Message (TTL / Expiration)

This feature uses Redis `EXPIRE` to auto-delete data after 10 seconds.

### Step 1: Set the Secret
*   **Action**: Save a secret message.
*   **URL**: [http://localhost:5000/secret/MySuperSecretCode](http://localhost:5000/secret/MySuperSecretCode)
*   **Output**: `Secret message saved! It will self-destruct in 10 seconds.`

### Step 2: Retrieve Immediately
*   **Action**: Check if it's there (do this within 10 seconds).
*   **URL**: [http://localhost:5000/get_secret](http://localhost:5000/get_secret)
*   **Output**: `🤫 The secret is: MySuperSecretCode`

### Step 3: Wait and Verify
*   **Action**: Wait for **10 seconds**.
*   **Action**: Refresh the page: [http://localhost:5000/get_secret](http://localhost:5000/get_secret)
*   **Output**: `👻 This message has self-destructed (or never existed).`
