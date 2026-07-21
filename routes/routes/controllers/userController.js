import { db } from "../config.js";

export const getUsers = async (req, res) => {
  try {
    const users = await db.collection("users").get();

    const data = users.docs.map((doc) => ({
      id: doc.id,
      ...doc.data()
    }));

    res.json(data);

  } catch (error) {
    res.status(500).json({
      error: error.message
    });
  }
};
