import { useEffect, useState } from "react";
import {
  getHabitsToday,
  completeHabit,
  getPlayerStatus,
  createHabit,
  deleteHabit
} from "./api";
import "./styles.css";

export default function App() {
  // -------------------------
  // Bestehender State
  // -------------------------
  const [habits, setHabits] = useState([]);
  const [player, setPlayer] = useState(null);

  // -------------------------
  // NEU: Add-Habit State
  // -------------------------
  const [newTitle, setNewTitle] = useState("");
  const [newDescription, setNewDescription] = useState("");
  const [newXp, setNewXp] = useState(10);

  // -------------------------
  // Daten laden
  // -------------------------
  async function loadData() {
    setHabits(await getHabitsToday());
    setPlayer(await getPlayerStatus());
  }

  // -------------------------
  // Habit erledigen
  // -------------------------
  async function handleComplete(id) {
    await completeHabit(id);
    loadData();
  }

  // -------------------------
  // NEU: Habit hinzufügen
  // -------------------------
  async function handleAddHabit() {
    if (!newTitle.trim()) return;

    await createHabit(newTitle, newDescription, Number(newXp));

    setNewTitle("");
    setNewDescription("");
    setNewXp(10);

    loadData();
  }

  async function handleDelete(id) {
  const ok = window.confirm("Gewohnheit wirklich löschen?");
    if (!ok) return;

    await deleteHabit(id);
    loadData();
  }

  // -------------------------
  // Initialer Load
  // -------------------------
  useEffect(() => {
    loadData();
  }, []);

  // -------------------------
  // UI
  // -------------------------
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

      {/* --------- Add Habit --------- */}
      <h2>Neue Gewohnheit</h2>

      <input
        type="text"
        placeholder="Titel"
        value={newTitle}
        onChange={(e) => setNewTitle(e.target.value)}
      />

      <input
        type="text"
        placeholder="Beschreibung"
        value={newDescription}
        onChange={(e) => setNewDescription(e.target.value)}
      />

      <input
        type="number"
        value={newXp}
        onChange={(e) => setNewXp(e.target.value)}
      />

      <button onClick={handleAddHabit}>
        Gewohnheit hinzufügen
      </button>

      {/* --------- Habit Liste --------- */}
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

            <button
              onClick={() => handleDelete(h.id)}
              style={{ marginLeft: "8px" }}
            >
              🗑 löschen
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}
