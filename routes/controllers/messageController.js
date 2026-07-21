import { db } from "../config.js";

export const getMessages = async (req, res) => {
  try {
    const messages = await db.collection("messages").get();

    const data = messages.docs.map((doc) => ({
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


export const sendMessage = async (req, res) => {
  try {
    const message = req.body;

    const result = await db.collection("messages").add({
      ...message,
      createdAt: new Date()
    });

    res.json({
      id: result.id,
      message: "Message sent successfully"
    });

  } catch (error) {
    res.status(500).json({
      error: error.message
    });
  }
};
