const API_URL = import.meta.env.VITE_API_URL;

export async function getHabitsToday() {
  const res = await fetch(`${API_URL}/habits/today?user_id=1`);
  return res.json();
}

export async function completeHabit(habitId) {
  const res = await fetch(`${API_URL}/habits/complete`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      user_id: 1,
      habit_id: habitId
    })
  });
  return res.json();
}

export async function getPlayerStatus() {
  const res = await fetch(`${API_URL}/player/status?user_id=1`);
  return res.json();
}

export async function createHabit(title, description, baseXp) {
  const res = await fetch(`${API_URL}/habits/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      title,
      description,
      base_xp: baseXp,
      user_id: 1
    })
  });

  return res.json();
}

export async function deleteHabit(habitId) {
  const res = await fetch(
    `${import.meta.env.VITE_API_URL}/habits/${habitId}?user_id=1`,
    {
      method: "DELETE"
    }
  );

  return res.json();
}