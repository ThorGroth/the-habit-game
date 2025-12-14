import { useEffect, useState } from "react";
import { getHabitsToday, completeHabit, getPlayerStatus } from "./api";
import "./styles.css";

export default function App() {
  const [habits, setHabits] = useState([]);
  const [player, setPlayer] = useState(null);

  async function loadData() {
    setHabits(await getHabitsToday());
    setPlayer(await getPlayerStatus());
  }

  async function handleComplete(id) {
    await completeHabit(id);
    loadData();
  }

  useEffect(() => {
    loadData();
  }, []);

  return (
    <div className="container">
      <h1>The Habit Game</h1>

      {player && (
        <div className="player">
          <p>Level: {player.level}</p>
          <p>XP: {player.xp}</p>
          <p>Streak: 🔥 {player.streak}</p>
        </div>
      )}

      <ul>
        {habits.map(h => (
          <li key={h.id} className={h.completed ? "done" : ""}>
            <strong>{h.title}</strong>
            <button
              disabled={h.completed}
              onClick={() => handleComplete(h.id)}
            >
              {h.completed ? "✔ erledigt" : "erledigen"}
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}
