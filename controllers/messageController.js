import { db } from "../config.js";

export const sendMessage = async (req, res) => {
  try {
    const { senderId, receiverId, message } = req.body;

    const doc = await db.collection("messages").add({
      senderId,
      receiverId,
      message,
      createdAt: new Date()
    });

    res.json({
      success: true,
      id: doc.id
    });

  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
};

export const getMessages = async (req, res) => {
  try {
    const snapshot = await db.collection("messages").get();

    const messages = snapshot.docs.map(doc => ({
      id: doc.id,
      ...doc.data()
    }));

    res.json(messages);

  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
};
