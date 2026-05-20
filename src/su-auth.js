import {
  signInWithEmailAndPassword,
  onAuthStateChanged
} from "firebase/auth";

import { ref, get } from "firebase/database";

import {
  auth,
  db,
  STORE_ID
} from "./config/firebase.js";

const loginBtn = document.querySelector("button");

loginBtn?.addEventListener("click", async () => {
  const email =
    document.querySelector('input[type="text"]').value;

  const password =
    document.querySelector('input[type="password"]').value;

  try {
    await signInWithEmailAndPassword(
      auth,
      email,
      password
    );

    alert("Login successful");

    location.reload();

  } catch (err) {
    alert(err.message);
  }
});

onAuthStateChanged(auth, async (user) => {
  if (!user) return;

  const snap = await get(
    ref(
      db,
      `stores/${STORE_ID}/users/${user.uid}`
    )
  );

  const data = snap.val();

  if (!data || data.role !== "superadmin") {
    alert("Access denied");
    return;
  }

  console.log("Superadmin authenticated");
});
