import { Box, Button, Flex, Input, Text } from "@chakra-ui/react";
import { useState } from "react";
// import React from "react";
// make the necessary import to recognize Flex Box Text Input and stuff 



function ChatBox() {
  const [message, setMessage] = useState("");
  const [conversation, setConversation] = useState<string[]>([]);

  const handleSend = () => {
    // For now, just echo the message.
    // Later, you'll call your LLM backend API here.
    setConversation((prev) => [...prev, `You: ${message}`]);
    setMessage("");
  };

  return (
    <Flex direction="column" height="100%" p={4}>
      <Box flex="1" overflowY="auto" border="1px solid #ccc" p={2} mb={2}>
        {conversation.map((msg, idx) => (
          <Text key={idx}>{msg}</Text>
        ))}
      </Box>
      <Flex>
        <Input
          placeholder="Type your message..."
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          mr={2}
        />
        <Button onClick={handleSend}>Send</Button>
      </Flex>
    </Flex>
  );
}

export default ChatBox;
