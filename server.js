import express from "express";
import cors from "cors";
import dotenv from "dotenv";

import userRoutes from "./routes/users.js";
import messageRoutes from "./routes/messages.js";

dotenv.config();

const app = express();

app.use(cors());
app.use(express.json());

app.use("/users", userRoutes);
app.use("/messages", messageRoutes);

app.get("/", (req, res) => {
  res.send("SAZU Cloud Backend is Running");
});

const PORT = process.env.PORT || 5000;

app.listen(PORT, () => {
  console.log(`SAZU Cloud Server running on port ${PORT}`);
});
