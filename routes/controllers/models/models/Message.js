class Message {
  constructor(id, senderId, receiverId, message, createdAt) {
    this.id = id;
    this.senderId = senderId;
    this.receiverId = receiverId;
    this.message = message;
    this.createdAt = createdAt;
  }
}

export default Message;
