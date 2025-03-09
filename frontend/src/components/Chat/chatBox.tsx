import { Box, Button, Flex, Input, Text } from "@chakra-ui/react";
import { useState } from "react";

function ChatBox() {
  const [message, setMessage] = useState("");
  const [conversation, setConversation] = useState<string[]>([
    "Hi! 👋 How can I assist you today?\n\nFor example:\n- Provide a patient report to summarize.\n- Upload an X-ray image to interpret.",
  ]);

  const handleSend = () => {
    if (message.trim()) {
      setConversation((prev) => [...prev, `You: ${message}`]);
      setMessage("");
    }
  };

  return (
    <Flex
      direction="column"
      height="100vh"
      maxWidth="500px"
      ml="auto"
      border="3px solid black" // Adjusted border width to 3px
      borderRadius="20px" // Increased border radius for rounder corners (or use "2xl" for ~16px)
      boxShadow="lg"
      bg="white"
      p={4}
      position="relative"
      right={0}
    >
      <Box
        flex="1"
        overflowY="auto"
        p={4}
        bg="gray.50"
        borderBottom="2px solid #E2E8F0"
      >
        {conversation.map((msg, idx) => (
          <Text
            key={idx}
            mb={2}
            p={3}
            bg={msg.startsWith("You:") ? "teal.100" : "gray.100"}
            borderRadius="md"
            maxWidth="80%"
            alignSelf={msg.startsWith("You:") ? "flex-end" : "center"}
            textAlign="center"
            display="block"
            margin="auto"
          >
            {msg.split("\n").map((line, i) => (
              <span key={i}>
                {line}
                <br />
              </span>
            ))}
          </Text>
        ))}
      </Box>
      <Flex mt={2} align="center">
        <Input
          placeholder="Type your message..."
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyPress={(e) => e.key === "Enter" && handleSend()}
          mr={2}
          borderColor="gray.300"
          _hover={{ borderColor: "teal.300" }}
          _focus={{ borderColor: "teal.500", boxShadow: "outline" }}
          flex="1"
        />
        <Button
          onClick={handleSend}
          colorScheme="teal"
          px={6}
          disabled={!message.trim()}
          _disabled={{ opacity: 0.6, cursor: "not-allowed" }}
        >
          Send
        </Button>
      </Flex>
    </Flex>
  );
}

export default ChatBox;